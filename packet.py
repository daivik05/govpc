class Packet:
    def __init__(self, src_ip, dest_ip, message, ttl=8):
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.message = message
        self.trace = []
        self.ttl = ttl
        self.visited = set()