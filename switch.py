import random


class Switch:

    def __init__(self, name):

        self.name = name

        self.ip = None

        self.mac = self.generate_mac()

        self.devices = []

        self.mac_table = {}

    # ====================================
    # GENERATE MAC
    # ====================================

    def generate_mac(self):

        return ":".join(

            f"{random.randint(0,255):02x}"

            for _ in range(6)
        )

    # ====================================
    # CONNECT DEVICE
    # ====================================

    def connect_device(

        self,

        device
    ):

        if device not in self.devices:

            self.devices.append(device)

    # ====================================
    # FORWARD FRAME
    # ====================================

    def forward_frame(

        self,

        packet
    ):

        print(

            f"{self.name} forwarding frame"
        )