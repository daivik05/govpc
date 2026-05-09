import ipaddress
from packet import Packet
from network import create_network
from visual import NetworkVisualizer

# =========================
# CREATE NETWORK
# =========================

(
    vm1,
    vm2,
    vm3,
    vm4,
    s1,
    s2,
    r1
) = create_network()

# =========================
# CREATE VISUALIZER
# =========================

visual = NetworkVisualizer()

print("\nNetwork Ready\n")

# =========================
# VM MAP
# =========================

vm_map = {

    vm1.ip: vm1,
    vm2.ip: vm2,
    vm3.ip: vm3,
    vm4.ip: vm4
}

# =========================
# MAIN LOOP
# =========================

while True:

    dest = input(
        "\nEnter destination IP (or exit): "
    )

    if dest.lower() == "exit":
        break

    # =========================
    # VALIDATE IP
    # =========================

    try:
        ipaddress.ip_address(dest)

    except ValueError:

        print("Invalid IP address")
        continue

    # =========================
    # CHECK VM EXISTS
    # =========================

    if dest not in vm_map:

        print("Unknown destination VM")
        continue

    msg = input("Enter message: ")

    dest_vm = vm_map[dest]

    # =========================
    # CREATE PACKET
    # =========================

    packet = Packet(

        vm1.ip,
        dest_vm.ip,

        msg,

        vm1.mac,
        dest_vm.mac
    )

    # =========================
    # SWITCHING
    # =========================

    print("\n===== SWITCHING =====")

    s1.forward_frame(packet)

    # =========================
    # ROUTING
    # =========================

    print("\n===== ROUTING =====")

    r1.forward_packet(packet)

    # =========================
    # VISUAL PATH
    # =========================

    if dest_vm.name == "VM3":

        visual_path = [
            "VM1",
            "S1",
            "VM3"
        ]

    elif dest_vm.name == "VM2":

        visual_path = [
            "VM1",
            "S1",
            "R1",
            "R2",
            "R3",
            "R4",
            "S2",
            "VM2"
        ]

    elif dest_vm.name == "VM4":

        visual_path = [
            "VM1",
            "S1",
            "R1",
            "R2",
            "R3",
            "R4",
            "S2",
            "VM4"
        ]

    else:

        visual_path = [
            "VM1",
            "S1"
        ]

    # =========================
    # ANIMATE PACKET
    # =========================

    visual.animate_packet(visual_path)

    print("\n========================")

# =========================
# RUN GUI
# =========================

visual.run()