from hwt.doc_markers import internal
from hwt.hdl.constants import INTF_DIRECTION
from hwt.synthesizer.unit import Unit
from hwtSimApi.hdlSimulator import HdlSimulator


@internal
def autoAddAgents(unit: Unit, sim: HdlSimulator):
    """
    Walk all interfaces on unit and instantiate agent for every interface.

    :return: all monitor/driver functions which should be added to simulation
         as processes
    """
    for intf in unit._interfaces:
        assert intf._isExtern, intf

        intf._initSimAgent(sim)
        assert intf._ag is not None, intf


@internal
def collect_processes_from_sim_agents(unit: Unit):
    proc = []
    for intf in unit._interfaces:
        a = intf._ag
        if not intf._isExtern or a is None:
            continue

        if intf._direction == INTF_DIRECTION.MASTER:
            agProcs = a.getMonitors()
        elif intf._direction == INTF_DIRECTION.SLAVE:
            agProcs = a.getDrivers()
        else:
            raise NotImplementedError(f"intf._direction {intf._direction} for {intf}")

        proc.extend(agProcs)

    return proc

