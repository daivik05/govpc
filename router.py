import random


class Router:

    def __init__(self, name):

        self.name = name

        self.ip = None

        self.mac = self.generate_mac()

        self.neighbors = []

    # ====================================
    # GENERATE MAC
    # ====================================

    def generate_mac(self):

        return ":".join(

            f"{random.randint(0,255):02x}"

            for _ in range(6)
        )

    # ====================================
    # CONNECT ROUTERS
    # ====================================

    def connect_router(

        self,

        router
    ):

        if router not in self.neighbors:

            self.neighbors.append(router)

    # ====================================
    # FORWARD PACKET
    # ====================================

    def forward_packet(

        self,

        packet
    ):

        print(

            f"{self.name} forwarding packet"
        )