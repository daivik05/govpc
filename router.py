import ipaddress
import random
from collections import deque


class Router:

    def __init__(self, name):

        self.name = name

        # interface_ip -> connected device
        self.interfaces = {}

        # neighbor_name -> router_object
        self.neighbors = {}

    # ====================================
    # ADD INTERFACE
    # ====================================

    def add_interface(self, ip, device):

        self.interfaces[ip] = device

    # ====================================
    # CONNECT ROUTERS
    # ====================================

    def connect_router(self, router):

        if router.name not in self.neighbors:

            self.neighbors[router.name] = router

    # ====================================
    # BFS PATH FINDING
    # ====================================

    def get_path(self, destination_name):

        visited = set()

        queue = deque([
            (self, [self])
        ])

        while queue:

            current, path = queue.popleft()

            # destination reached
            if current.name == destination_name:
                return path

            visited.add(current)

            # explore neighbors
            for neighbor in current.neighbors.values():

                if neighbor not in visited:

                    queue.append(
                        (
                            neighbor,
                            path + [neighbor]
                        )
                    )

        return None

    # ====================================
    # FIND ROUTER PATH TO DESTINATION VM
    # ====================================

    def get_path_to_destination_ip(self, dest_ip):

        visited = set()

        queue = deque([
            (self, [self])
        ])

        while queue:

            current, path = queue.popleft()

            if current in visited:
                continue

            visited.add(current)

            # check directly connected devices
            for interface_ip, device in current.interfaces.items():

                if hasattr(device, "ip"):

                    if device.ip == dest_ip:
                        return path

            # continue BFS
            for neighbor in current.neighbors.values():

                if neighbor not in visited:

                    queue.append(
                        (
                            neighbor,
                            path + [neighbor]
                        )
                    )

        return None

    # ====================================
    # FORWARD PACKET
    # ====================================

    def forward_packet(self, packet):

        # ====================================
        # PACKET LOSS SIMULATION
        # ====================================

        if random.random() < 0.1:

            print(f"\nPacket lost at {self.name}")

            print(
                "Trace:",
                " -> ".join(
                    [packet.src_ip] + packet.trace
                )
            )

            return

        # ====================================
        # LOOP DETECTION
        # ====================================

        if self.name in packet.visited:

            print(f"\nPacket dropped at {self.name}")

            print("Reason: Routing loop detected")

            print(
                "Trace:",
                " -> ".join(
                    [packet.src_ip] + packet.trace
                )
            )

            return

        packet.visited.add(self.name)

        # ====================================
        # TTL CHECK
        # ====================================

        packet.ttl -= 1

        if packet.ttl <= 0:

            print(f"\nPacket dropped at {self.name}")

            print("Reason: TTL expired")

            print(
                "Trace:",
                " -> ".join(
                    [packet.src_ip] + packet.trace
                )
            )

            return

        # ====================================
        # ADD TRACE
        # ====================================

        packet.trace.append(self.name)

        print(f"{self.name} processing packet")

        # ====================================
        # DIRECT DELIVERY
        # ====================================

        for interface_ip, device in self.interfaces.items():

            if hasattr(device, "ip"):

                if device.ip == packet.dest_ip:

                    print(
                        f"\n{self.name} directly "
                        f"connected to destination"
                    )

                    device.receive_packet(packet)

                    return

        # ====================================
        # HOST NOT FOUND
        # ====================================

        for interface_ip, device in self.interfaces.items():

            if hasattr(device, "ip"):

                network = ipaddress.ip_network(
                    interface_ip + "/24",
                    strict=False
                )

                if (
                    ipaddress.ip_address(packet.dest_ip)
                    in network
                ):

                    print(
                        f"\nPacket dropped at {self.name}"
                    )

                    print(
                        "Reason: Destination host "
                        "not found"
                    )

                    print(
                        "Trace:",
                        " -> ".join(
                            [packet.src_ip]
                            + packet.trace
                        )
                    )

                    return

        # ====================================
        # FIND PATH USING BFS
        # ====================================

        path = self.get_path_to_destination_ip(
            packet.dest_ip
        )

        # ====================================
        # NO ROUTE FOUND
        # ====================================

        if not path:

            print(f"\nNo route from {self.name}")

            return

        # ====================================
        # NEXT HOP
        # ====================================

        current_index = path.index(self)

        # already final router
        if current_index == len(path) - 1:

            print(
                f"\n{self.name} is final router "
                f"but destination missing"
            )

            return

        next_hop = path[current_index + 1]

        print(
            f"{self.name} -> forwarding "
            f"to {next_hop.name}"
        )

        next_hop.forward_packet(packet)