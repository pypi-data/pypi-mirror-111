

from copy import deepcopy
from functools import reduce
from itertools import compress
from operator import and_
from typing import List, Tuple, Dict, Optional, Callable, Set

from hwt.doc_markers import internal
from hwt.hdl.operatorUtils import replace_input_in_expr
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.statements.statement import HdlStatement
from hwt.hdl.statements.utils.comparison import  statementsAreSame, isSameStatementList
from hwt.hdl.statements.utils.ioDiscovery import HdlStatement_discover_enclosure_for_statements
from hwt.hdl.statements.utils.reduction import HdlStatement_merge_statement_lists, \
    HdlStatement_try_reduce_list, is_mergable_statement_list
from hwt.hdl.statements.utils.signalCut import HdlStatement_cut_off_drivers_of_list
from hwt.serializer.utils import RtlSignal_sort_key
from hwt.synthesizer.rtlLevel.fill_stm_list_with_enclosure import fill_stm_list_with_enclosure
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.walkers import discover_sensitivity_of_sig


class IfContainer(HdlStatement):
    """
    Structural container of if statement for hdl rendering

    :ivar ~._ifTrue_enclosed_for: set of signals for which if ifTrue branch enclosed
            (has not branch where signal is not assignment)
    :ivar ~._elIfs_enclosed_for: list of sets of enclosed signals for each elif
    :ivar ~._ifFalse_enclosed_for: set of enclosed signals for ifFalse branch
    """
    _DEEPCOPY_SHALLOW_ONLY = (*HdlStatement._DEEPCOPY_SHALLOW_ONLY, '_ifTrue_enclosed_for', '_elIfs_enclosed_for', '_ifFalse_enclosed_for')
    _DEEPCOPY_SKIP = (*HdlStatement._DEEPCOPY_SKIP, 'cond', 'elIfs')

    def __init__(self, cond: RtlSignalBase, ifTrue=None, ifFalse=None, elIfs=None,
                 parentStm=None, event_dependent_from_branch: Optional[int]=None):
        """
        :param cond: RtlSignal as conditions for this if
        :param ifTrue: list of statements which should be active if cond.
            is met
        :param elIfs: list of tuples (list of conditions, list of statements)
        :param ifFalse: list of statements which should be active if cond.
            and any other cond. in elIfs is met
        """
        assert isinstance(cond, RtlSignalBase)
        self.cond = cond
        super(IfContainer, self).__init__(
            parentStm,
            event_dependent_from_branch=event_dependent_from_branch)

        if ifTrue is None:
            ifTrue = []
        self.ifTrue: List[HdlStatement] = ifTrue

        if elIfs is None:
            elIfs = []
        self.elIfs: List[Tuple[RtlSignalBase, List[HdlStatement]]] = elIfs

        self.ifFalse: Optional[List[HdlStatement]] = ifFalse
        self._ifTrue_enclosed_for: Optional[Set[RtlSignalBase]] = None
        self._elIfs_enclosed_for: Optional[Set[RtlSignalBase]] = None
        self._ifFalse_enclosed_for: Optional[Set[RtlSignalBase]] = None

    def __deepcopy__(self, memo: dict):
        result = super(IfContainer, self).__deepcopy__(memo)
        result.cond = self.cond
        result.elIfs = [(c, deepcopy(stms, memo)) for c, stms in self.elIfs]
        return result

    @internal
    def _collect_io(self):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._collect_io`
        """
        if isinstance(self.cond, RtlSignalBase):
            self._inputs.append(self.cond)
        for c, _ in self.elIfs:
            if isinstance(c, RtlSignalBase):
                self._inputs.append(c)
        super(IfContainer, self)._collect_io()

    @internal
    def _collect_inputs(self) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._collect_inputs`
        """
        if isinstance(self.cond, RtlSignalBase):
            self._inputs.append(self.cond)
        for c, _ in self.elIfs:
            if isinstance(c, RtlSignalBase):
                self._inputs.append(c)
        super(IfContainer, self)._collect_inputs()

    @internal
    def _clean_signal_meta(self):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._clean_signal_meta`
        """
        self._sensitivity = None
        self._ifTrue_enclosed_for = None
        self._elIfs_enclosed_for = None
        self._ifFalse_enclosed_for = None
        HdlStatement._clean_signal_meta(self)

    @internal
    def _cut_off_drivers_of(self, sig: RtlSignalBase):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._cut_off_drivers_of`
        """
        if self._sensitivity is not None or self._enclosed_for is not None:
            raise NotImplementedError(
                    "Sensitivity and enclosure has to be cleaned first")

        if len(self._outputs) == 1 and sig in self._outputs:
            # this statement has only this output, eject this statement from its parent
            self.parentStm = None  # because new parent will be asigned immediately after cutting of
            return self

        sig.drivers.discard(self)
        # try to cut off all statements which are drivers of specified signal
        # in all branches
        child_keep_mask = []

        newIfTrue = []
        all_cut_off = True
        all_cut_off &= HdlStatement_cut_off_drivers_of_list(
            sig, self.ifTrue, child_keep_mask, newIfTrue)
        self.ifTrue = list(compress(self.ifTrue, child_keep_mask))

        newElifs = []
        anyElifHit = False
        for cond, stms in self.elIfs:
            newCase = []
            child_keep_mask.clear()
            all_cut_off &= HdlStatement_cut_off_drivers_of_list(
                sig, stms, child_keep_mask, newCase)

            _stms = list(compress(stms, child_keep_mask))
            stms.clear()
            stms.extend(_stms)

            if newCase:
                anyElifHit = True
            newElifs.append((cond, newCase))

        newIfFalse = None
        if self.ifFalse:
            newIfFalse = []
            child_keep_mask.clear()
            all_cut_off &= HdlStatement_cut_off_drivers_of_list(
                sig, self.ifFalse, child_keep_mask, newIfFalse)
            self.ifFalse = list(compress(self.ifFalse, child_keep_mask))

        assert not all_cut_off, "everything was cut of but this should be already known at the start"

        if newIfTrue or newIfFalse or anyElifHit or newIfFalse:
            # parts were cut off
            # generate new statement for them
            cond_sig = self.cond
            n = self.__class__(cond_sig, newIfTrue)
            for c_sig, stms in newElifs:
                n.Elif(c_sig, stms)
            if newIfFalse is not None:
                n.Else(newIfFalse)

            if self.parentStm is None:
                ctx = n._get_rtl_context()
                ctx.statements.add(n)

            self._cut_off_drivers_of_regenerate_io(sig, n)

            return n

    @internal
    def _discover_enclosure(self):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._discover_enclosure`
        """
        outputs = self._outputs
        self._ifTrue_enclosed_for = HdlStatement_discover_enclosure_for_statements(
            self.ifTrue, outputs)

        elif_encls = self._elIfs_enclosed_for = []
        for _, stms in self.elIfs:
            e = HdlStatement_discover_enclosure_for_statements(
                stms, outputs)
            elif_encls.append(e)

        self._ifFalse_enclosed_for = HdlStatement_discover_enclosure_for_statements(
            self.ifFalse, outputs)

        assert self._enclosed_for is None
        encl = self._enclosed_for = set()

        for s in self._ifTrue_enclosed_for:
            enclosed = True

            for elif_e in elif_encls:
                if s not in elif_e:
                    enclosed = False
                    break

            if enclosed and s in self._ifFalse_enclosed_for:
                encl.add(s)

    @internal
    def _discover_sensitivity(self, seen: set) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._discover_sensitivity`
        """
        assert self._sensitivity is None, self
        ctx = self._sensitivity = SensitivityCtx()

        discover_sensitivity_of_sig(self.cond, seen, ctx)
        if ctx.contains_ev_dependency:
            return

        for stm in self.ifTrue:
            stm._discover_sensitivity(seen)
            ctx.extend(stm._sensitivity)

        # elifs
        for cond, stms in self.elIfs:
            if ctx.contains_ev_dependency:
                break

            discover_sensitivity_of_sig(cond, seen, ctx)
            if ctx.contains_ev_dependency:
                break

            for stm in stms:
                if ctx.contains_ev_dependency:
                    break

                stm._discover_sensitivity(seen)
                ctx.extend(stm._sensitivity)

        if self.ifFalse:
            assert not ctx.contains_ev_dependency, "can not negate event"
            # else
            for stm in self.ifFalse:
                stm._discover_sensitivity(seen)
                ctx.extend(stm._sensitivity)

    @internal
    def _fill_enclosure(self, enclosure: Dict[RtlSignalBase, Callable[[], HdlStatement]]) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._fill_enclosure`
        """
        enc = []
        outputs = self._outputs
        for e in sorted(enclosure.keys(), key=RtlSignal_sort_key):
            if e in outputs and e not in self._enclosed_for:
                enc.append(e)

        if not enc:
            return
        fill_stm_list_with_enclosure(self, self._ifTrue_enclosed_for,
                                     self.ifTrue, enc, enclosure)

        for (_, stms), e in zip(self.elIfs, self._elIfs_enclosed_for):
            fill_stm_list_with_enclosure(self, e, stms, enc, enclosure)

        self.ifFalse = fill_stm_list_with_enclosure(self, self._ifFalse_enclosed_for,
                                                    self.ifFalse, enc, enclosure)

        self._enclosed_for.update(enc)

    def _iter_stms(self):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._iter_stms`
        """
        yield from self.ifTrue
        for _, stms in self.elIfs:
            yield from stms
        if self.ifFalse is not None:
            yield from self.ifFalse

    @internal
    def _try_reduce(self) -> Tuple[bool, List[HdlStatement]]:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._try_reduce`
        """
        # flag if IO of statement has changed
        io_change = False

        self.ifTrue, rank_decrease, _io_change = HdlStatement_try_reduce_list(
            self.ifTrue)
        self.rank -= rank_decrease
        io_change |= _io_change

        new_elifs = []
        for cond, statements in self.elIfs:
            _statements, rank_decrease, _io_change = HdlStatement_try_reduce_list(
                statements)
            self.rank -= rank_decrease
            io_change |= _io_change
            new_elifs.append((cond, _statements))
        self.elIfs = new_elifs

        if self.ifFalse is not None:
            self.ifFalse, rank_decrease, _io_update_required = HdlStatement_try_reduce_list(
                self.ifFalse)
            self.rank -= rank_decrease
            io_change |= _io_change

        reduce_self = not self._condHasEffect(
            self.ifTrue, self.ifFalse, self.elIfs)

        if reduce_self:
            res = self.ifTrue
        else:
            res = [self, ]

        self._on_reduce(reduce_self, io_change, res)

        # try merge nested ifs as elifs
        if self.ifFalse is not None and len(self.ifFalse) == 1:
            child = self.ifFalse[0]
            if isinstance(child, IfContainer):
                self._merge_nested_if_from_else(child)

        return res, io_change

    @internal
    def _merge_nested_if_from_else(self, ifStm: "IfContainer"):
        """
        Merge nested IfContarner form else branch to this IfContainer
        as elif and else branches
        """
        self.elIfs.append((ifStm.cond, ifStm.ifTrue))
        self.elIfs.extend(ifStm.elIfs)

        self.ifFalse = ifStm.ifFalse

    @internal
    def _is_mergable(self, other: HdlStatement) -> bool:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._is_mergable`
        """
        if not isinstance(other, IfContainer):
            return False

        if (self.cond is not other.cond
                or not is_mergable_statement_list(self.ifTrue, other.ifTrue)):
            return False

        if len(self.elIfs) != len(other.elIfs):
            return False

        for (a_c, a_stm), (b_c, b_stm) in zip(self.elIfs, other.elIfs):
            if a_c is not b_c or not is_mergable_statement_list(a_stm, b_stm):
                return False

        if not is_mergable_statement_list(self.ifFalse, other.ifFalse):
            return False
        return True

    @internal
    def _merge_with_other_stm(self, other: "IfContainer") -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._merge_with_other_stm`
        """
        merge = HdlStatement_merge_statement_lists
        self.ifTrue = merge(self.ifTrue, other.ifTrue)

        new_elifs = []
        for ((c, elifA), (_, elifB)) in zip(self.elIfs, other.elIfs):
            new_elifs.append((c, merge(elifA, elifB)))
        self.elIfs = new_elifs

        self.ifFalse = merge(self.ifFalse, other.ifFalse)

        other.ifTrue = []
        other.elIfs = []
        other.ifFalse = None

        self._on_merge(other)

    @internal
    @staticmethod
    def _condHasEffect(ifTrue, ifFalse, elIfs):
        stmCnt = len(ifTrue)
        # [TODO] condition in empty if stm
        if ifFalse is not None \
                and stmCnt == len(ifFalse) \
                and reduce(and_,
                           [len(stm) == stmCnt
                            for _, stm in elIfs],
                           True):
            for stms in zip(ifTrue, ifFalse, *map(lambda x: x[1], elIfs)):
                if not statementsAreSame(stms):
                    return True
            return False
        return True

    def isSame(self, other: HdlStatement) -> bool:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement.isSame`
        """
        if self is other:
            return True

        if self.rank != other.rank:
            return False

        if isinstance(other, IfContainer):
            if self.cond is other.cond:
                if len(self.ifTrue) == len(other.ifTrue) \
                        and ((self.ifFalse is None and other.ifFalse is None) or
                             len(self.ifFalse) == len(other.ifFalse)) \
                        and len(self.elIfs) == len(other.elIfs):
                    if not isSameStatementList(self.ifTrue,
                                               other.ifTrue) \
                            or not isSameStatementList(self.ifFalse,
                                                       other.ifFalse):
                        return False
                    for (ac, astms), (bc, bstms) in zip(self.elIfs,
                                                        other.elIfs):
                        if not (ac == bc) or\
                                not isSameStatementList(astms, bstms):
                            return False
                    return True
        return False

    @internal
    def _replace_input(self, toReplace: RtlSignalBase, replacement: RtlSignalBase):
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._replace_input`
        """
        isTopStm = self.parentStm is None
        if isTopStm:
            self.cond = replace_input_in_expr(self, self.cond, toReplace,
                                              replacement, isTopStm)

        for stm in self.ifTrue:
            stm._replace_input(toReplace, replacement)

        new_elifs = []
        for (cond, stms) in self.elIfs:
            new_cond = replace_input_in_expr(self, cond, toReplace, replacement, isTopStm)
            for stm in stms:
                stm._replace_input(toReplace, replacement)
            new_elifs.append((new_cond, stms))
        self.elIfs = new_elifs

        if self.ifFalse is not None:
            for stm in self.ifFalse:
                stm._replace_input(toReplace, replacement)

        self._replace_input_update_sensitivity_and_enclosure(toReplace, replacement)

    @internal
    def _replace_child_statement(self, stm:HdlStatement,
            replacement:List[HdlStatement],
            update_io:bool) -> None:
        """
        :see: :meth:`hwt.hdl.statements.statement.HdlStatement._replace_child_statement`
        """

        if update_io:
            raise NotImplementedError()
        for branch_list in (self.ifTrue, *(elif_stms for _, elif_stms in self.elIfs), self.ifFalse):
            if branch_list is None:
                continue
            try:
                i = branch_list.index(stm)
            except ValueError:
                # not in list
                continue

            self.rank -= stm.rank
            branch_list[i:i + 1] = replacement
            for rstm in replacement:
                rstm._set_parent_stm(self)
            # reset IO because it was shared with this statement
            stm._destroy()
            return

        raise ValueError("Statement", stm, "not found in ", self)

