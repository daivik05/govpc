class VM:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.router = None

    def connect_router(self, router):
        self.router = router

    def receive_packet(self, packet):
        print(f"\nPacket reached {self.name} ({self.ip})")
        print(f"Message: {packet.message}")

        full_path = [packet.src_ip] + packet.trace + [packet.dest_ip]
        print("Trace:", " -> ".join(full_path))