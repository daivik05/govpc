class Packet:

    def __init__(
        self,
        src_ip,
        dest_ip,
        message,
        src_mac,
        dest_mac,
        ttl=8
    ):

        self.src_ip = src_ip
        self.dest_ip = dest_ip

        self.src_mac = src_mac
        self.dest_mac = dest_mac

        self.message = message

        self.ttl = ttl

        self.trace = []
        self.visited = set()