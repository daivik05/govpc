from packet import Packet
from network import create_network
from visualizer import NetworkVisualizer
import ipaddress

# Create network
vm1, vm2, r1 = create_network()

# Start visualizer
visual = NetworkVisualizer([r1])

print("\nNetwork ready. Start sending packets.\n")

while True:
    dest = input("Enter destination IP (or 'exit'): ")

    if dest.lower() == "exit":
        print("Exiting...")
        break

    # Validate IP
    try:
        ipaddress.ip_address(dest)
    except ValueError:
        print("Invalid IP address\n")
        continue

    msg = input("Enter message: ")

    # Create packet
    packet = Packet(vm1.ip, dest, msg, ttl=8)

    print("\n--- TEXT SIMULATION ---\n")
    r1.forward_packet(packet)

    print("\n--- VISUAL SIMULATION ---\n")

    # Get path for animation
    path = r1.get_path(dest)

    if path:
        print("Path:", " -> ".join([r.name for r in path]))
        visual.animate_packet(path)
    else:
        print("No path found for visualization")

    print("\n-----------------------\n")

# Run Tkinter window
visual.run()