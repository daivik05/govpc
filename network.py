from vm import VM
from router import Router

def create_network():

    # VMs
    vm1 = VM("VM1", "10.0.0.2")
    vm2 = VM("VM2", "40.0.0.2")

    # Routers
    r1 = Router("R1")
    r2 = Router("R2")
    r3 = Router("R3")
    r4 = Router("R4")

    # Connect routers (BFS graph - no weights)
    r1.connect_router(r2)
    r2.connect_router(r1)

    r2.connect_router(r3)
    r3.connect_router(r2)

    r3.connect_router(r4)
    r4.connect_router(r3)

    r1.connect_router(r4)
    r4.connect_router(r1)

    # Connect VMs
    vm1.connect_router(r1)
    vm2.connect_router(r4)

    r1.add_interface("10.0.0.1", vm1)
    r4.add_interface("40.0.0.1", vm2)

    return vm1, vm2, r1