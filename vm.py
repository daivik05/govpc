class VM:

    def __init__(self, name, ip, mac):

        self.name = name
        self.ip = ip
        self.mac = mac

        self.router = None
        self.switch = None

    def connect_router(self, router):
        self.router = router

    def connect_switch(self, switch):
        self.switch = switch

    def receive_packet(self, packet):

        print(f"\nPacket reached {self.name}")
        print(f"Destination IP: {self.ip}")

        print(f"Message: {packet.message}")

        full_trace = [packet.src_ip] + packet.trace + [self.ip]

        print("Trace:", " -> ".join(full_trace))