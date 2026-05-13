class Packet:

    def __init__(

        self,

        src_ip,
        dest_ip,

        message,

        src_mac,
        dest_mac,

        vlan_id=None
    ):

        # ====================================
        # LAYER 3
        # ====================================

        self.src_ip = src_ip

        self.dest_ip = dest_ip

        # ====================================
        # LAYER 2
        # ====================================

        self.src_mac = src_mac

        self.dest_mac = dest_mac

        # ====================================
        # PAYLOAD
        # ====================================

        self.message = message

        # ====================================
        # VLAN
        # ====================================

        self.vlan_id = vlan_id

        # ====================================
        # PACKET TRACING
        # ====================================

        self.trace = []

        # ====================================
        # LOOP DETECTION
        # ====================================

        self.visited = set()

        # ====================================
        # TTL
        # ====================================

        self.ttl = 10

    # ====================================
    # DISPLAY PACKET
    # ====================================

    def show_packet(self):

        print("\n===== PACKET =====")

        print(

            f"SRC IP: {self.src_ip}"
        )

        print(

            f"DST IP: {self.dest_ip}"
        )

        print(

            f"SRC MAC: {self.src_mac}"
        )

        print(

            f"DST MAC: {self.dest_mac}"
        )

        print(

            f"VLAN: {self.vlan_id}"
        )

        print(

            f"TTL: {self.ttl}"
        )

        print(

            f"MESSAGE: {self.message}"
        )

        print("===================")