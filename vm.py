import random


class VM:

    def __init__(

        self,

        name,

        ip,

        mac=None,

        vlan_id=1
    ):

        self.name = name

        self.ip = ip

        self.vlan = vlan_id

        # AUTO MAC

        if mac:

            self.mac = mac

        else:

            self.mac = self.generate_mac()

    # ====================================
    # GENERATE MAC
    # ====================================

    def generate_mac(self):

        return ":".join(

            f"{random.randint(0,255):02x}"

            for _ in range(6)
        )

    # ====================================
    # RECEIVE PACKET
    # ====================================

    def receive_packet(self, packet):

        print(

            f"\n{self.name} "

            f"received packet"
        )

        print(

            f"Message: "

            f"{packet.message}"
        )