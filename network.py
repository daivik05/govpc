from vm import VM
from router import Router
from switch import Switch

def create_network():

    # ======================
    # VMs
    # ======================

    vm1 = VM(
        "VM1",
        "10.0.0.2",
        "AA:AA:AA:AA:AA:01",
        10
    )

    vm2 = VM(
        "VM2",
        "40.0.0.2",
        "AA:AA:AA:AA:AA:02",
        10
    )

    vm3 = VM(
        "VM3",
        "20.0.0.2",
        "AA:AA:AA:AA:AA:03",
        20
    )

    vm4 = VM(
        "VM4",
        "30.0.0.2",
        "AA:AA:AA:AA:AA:04",
        20
    )

    # ======================
    # SWITCHES
    # ======================

    s1 = Switch("S1")
    s2 = Switch("S2")

    # ======================
    # ROUTERS
    # ======================

    r1 = Router("R1")
    r2 = Router("R2")
    r3 = Router("R3")
    r4 = Router("R4")

    # ======================
    # ROUTER CONNECTIONS
    # ======================

    r1.connect_router(r2)
    r2.connect_router(r1)

    r2.connect_router(r3)
    r3.connect_router(r2)

    r3.connect_router(r4)
    r4.connect_router(r3)

    # ======================
    # SWITCH CONNECTIONS
    # ======================

    s1.connect_device(vm1)
    s1.connect_device(vm3)
    s1.connect_device(r1)

    s2.connect_device(vm2)
    s2.connect_device(vm4)
    s2.connect_device(r4)

    # ======================
    # VM → SWITCH
    # ======================

    vm1.connect_switch(s1)
    vm2.connect_switch(s2)
    vm3.connect_switch(s1)
    vm4.connect_switch(s2)

    # ======================
    # ROUTER INTERFACES
    # ======================

    r1.add_interface("10.0.0.1", vm1)
    r2.add_interface("20.0.0.1", vm3)

    r3.add_interface("30.0.0.1", vm4)
    r4.add_interface("40.0.0.1", vm2)

    return vm1, vm2, vm3, vm4, s1, s2, r1