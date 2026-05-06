import ipaddress
import random
from collections import deque

class Router:
    def __init__(self, name):
        self.name = name
        self.interfaces = {}
        self.neighbors = []

    def add_interface(self, ip, device):
        self.interfaces[ip] = device

    def connect_router(self, router):
        if router not in self.neighbors:
            self.neighbors.append(router)

    def get_path(self, dest_ip):
        visited = set()
        queue = deque([(self, [self])])

        while queue:
            current, path = queue.popleft()

            if current in visited:
                continue
            visited.add(current)

            for ip, device in current.interfaces.items():
                if hasattr(device, 'ip') and device.ip == dest_ip:
                    return path

            for neighbor in current.neighbors:
                queue.append((neighbor, path + [neighbor]))

        return None

    def forward_packet(self, packet):

        if random.random() < 0.1:
            print(f"\nPacket lost at {self.name}")
            return

        if self.name in packet.visited:
            print(f"\nLoop detected at {self.name}")
            return

        packet.visited.add(self.name)

        packet.ttl -= 1
        if packet.ttl <= 0:
            print(f"\nTTL expired at {self.name}")
            return

        packet.trace.append(self.name)

        for ip, device in self.interfaces.items():
            if hasattr(device, 'ip') and device.ip == packet.dest_ip:
                device.receive_packet(packet)
                return

        path = self.get_path(packet.dest_ip)

        if path and len(path) > 1:
            next_hop = path[1]
            print(f"{self.name} -> {next_hop.name}")
            next_hop.forward_packet(packet)
        else:
            print(f"\nNo route from {self.name}")