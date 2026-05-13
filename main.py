import json
import ipaddress

from collections import deque

from packet import Packet
from visual import NetworkVisualizer

from router import Router
from switch import Switch
from vm import VM

# ====================================
# LOAD TOPOLOGY
# ====================================

with open("topology.json", "r") as f:

    topology_data = json.load(f)

# ====================================
# CREATE DEVICES
# ====================================

devices = {}

ip_counter = 1

# ====================================
# GENERATE IP
# ====================================

def generate_ip():

    global ip_counter

    ip = f"10.0.0.{ip_counter}"

    ip_counter += 1

    return ip

# ====================================
# CREATE ROUTERS
# ====================================

for router_name in topology_data["routers"]:

    router = Router(router_name)

    router.ip = generate_ip()

    devices[router_name] = router

# ====================================
# CREATE SWITCHES
# ====================================

for switch_name in topology_data["switches"]:

    switch = Switch(switch_name)

    switch.ip = generate_ip()

    devices[switch_name] = switch

# ====================================
# CREATE VMS
# ====================================

for vm_data in topology_data["vms"]:

    vm_name = vm_data["name"]

    vlan = vm_data["vlan"]

    vm = VM(

        vm_name,

        generate_ip(), None,

        vlan_id=vlan
    )

    devices[vm_name] = vm

# ====================================
# CONNECT DEVICES
# ====================================

for conn in topology_data["connections"]:

    d1 = conn[0]
    d2 = conn[1]

    if (
        d1 not in devices
        or
        d2 not in devices
    ):

        continue

    dev1 = devices[d1]
    dev2 = devices[d2]

    # ROUTER ↔ ROUTER

    if (
        isinstance(dev1, Router)
        and
        isinstance(dev2, Router)
    ):

        dev1.connect_router(dev2)

        dev2.connect_router(dev1)

    # SWITCH CONNECTIONS

    elif isinstance(dev1, Switch):

        dev1.connect_device(dev2)

    elif isinstance(dev2, Switch):

        dev2.connect_device(dev1)

# ====================================
# SHOW DEVICES
# ====================================

print("\n===== DEVICES =====")

for name, device in devices.items():

    print(f"\nNAME: {name}")

    print(
        f"TYPE: "
        f"{device.__class__.__name__}"
    )

    print(f"IP: {device.ip}")

    print(f"MAC: {device.mac}")

    if hasattr(device, "vlan"):

        print(
            f"VLAN: "
            f"{device.vlan}"
        )

print("\n====================")

# ====================================
# BFS PATH FINDER
# ====================================

def find_path(

    topology_data,

    start,

    end
):

    graph = {}

    # BUILD GRAPH

    for conn in topology_data["connections"]:

        a = conn[0]
        b = conn[1]

        if a not in graph:

            graph[a] = []

        if b not in graph:

            graph[b] = []

        graph[a].append(b)

        graph[b].append(a)

    # BFS

    queue = deque()

    queue.append(
        (start, [start])
    )

    visited = set()

    while queue:

        current, path = queue.popleft()

        if current == end:

            return path

        visited.add(current)

        for neighbor in graph.get(current, []):

            if neighbor not in visited:

                queue.append(

                    (
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None

# ====================================
# CREATE VISUALIZER
# ====================================

visual = NetworkVisualizer()

visual.draw_topology(

    topology_data,

    devices
)

visual.root.update()

# ====================================
# MAIN LOOP
# ====================================

while True:

    source_ip = input(
        "\nEnter source IP (or exit): "
    )

    if source_ip.lower() == "exit":

        break

    dest_ip = input(
        "Enter destination IP: "
    )

    # ====================================
    # VALIDATE IPS
    # ====================================

    try:

        ipaddress.ip_address(source_ip)

        ipaddress.ip_address(dest_ip)

    except ValueError:

        print("\nInvalid IP address")

        continue

    # ====================================
    # FIND SOURCE VM
    # ====================================

    source_vm = None
    dest_vm = None

    for device in devices.values():

        if (
            hasattr(device, "ip")
            and
            device.ip == source_ip
        ):

            source_vm = device

        if (
            hasattr(device, "ip")
            and
            device.ip == dest_ip
        ):

            dest_vm = device

    # ====================================
    # CHECK DEVICES
    # ====================================

    if not source_vm:

        print("\nSource device not found")

        continue

    if not dest_vm:

        print("\nDestination device not found")

        continue

    # ====================================
    # VLAN CHECK
    # ====================================

    if (
        hasattr(source_vm, "vlan")
        and
        hasattr(dest_vm, "vlan")
    ):

        if source_vm.vlan != dest_vm.vlan:

            print("\n===== VLAN CHECK =====")

            print(
                f"{source_vm.name} "
                f"is in VLAN "
                f"{source_vm.vlan}"
            )

            print(
                f"{dest_vm.name} "
                f"is in VLAN "
                f"{dest_vm.vlan}"
            )

            print("\nPacket blocked")

            print(
                "Reason: VLAN mismatch"
            )

            blocked_path = [
                source_vm.name
            ]

            visual.animate_packet(
                blocked_path
            )

            continue

    # ====================================
    # MESSAGE
    # ====================================

    msg = input("Enter message: ")

    # ====================================
    # CREATE PACKET
    # ====================================

    packet = Packet(

        source_vm.ip,

        dest_vm.ip,

        msg,

        source_vm.mac,

        dest_vm.mac,

        source_vm.vlan
    )

    # ====================================
    # FIND REAL PATH
    # ====================================

    visual_path = find_path(

        topology_data,

        source_vm.name,

        dest_vm.name
    )

    if not visual_path:

        print("\nNo route found")

        continue

    # ====================================
    # PRINT PACKET INFO
    # ====================================

    print("\n===== PACKET =====")

    print(
        f"SRC IP: "
        f"{packet.src_ip}"
    )

    print(
        f"DST IP: "
        f"{packet.dest_ip}"
    )

    print(
        f"SRC MAC: "
        f"{packet.src_mac}"
    )

    print(
        f"DST MAC: "
        f"{packet.dest_mac}"
    )

    print(
        f"VLAN: "
        f"{packet.vlan_id}"
    )

    # ====================================
    # PRINT PATH
    # ====================================

    print("\nPATH FOUND:")

    print(
        " -> ".join(visual_path)
    )

    # ====================================
    # VISUAL ANIMATION
    # ====================================

    visual.animate_packet(
        visual_path
    )

    print("\n====================")

# ====================================
# RUN GUI
# ====================================

visual.run()