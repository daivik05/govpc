class Switch:

    def __init__(self, name):

        self.name = name

        self.devices = []

        # MAC → device
        self.mac_table = {}

    def connect_device(self, device):

        self.devices.append(device)

    def show_mac_table(self):

        print(f"\n=== {self.name} MAC TABLE ===")

        if not self.mac_table:
            print("Empty")

        for mac, device in self.mac_table.items():

            print( 
                f"MAC: {mac} " 
                f"→ DEVICE: {device.name}"
            )

        print("====================")

    def forward_frame(self, packet):

        print(f"\n{self.name} received frame")

        # LEARN SOURCE MAC
        sender = None

        for device in self.devices:

            if hasattr(device, 'mac'):
                if device.mac == packet.src_mac:
                    sender = device

        if sender:
            self.mac_table[packet.src_mac] = sender

            print(
                f"{self.name} LEARNED:\n"
                f"{packet.src_mac} -> {sender.name}"
            )

        self.show_mac_table()

        # DESTINATION KNOWN
        if packet.dest_mac in self.mac_table:

            target = self.mac_table[packet.dest_mac]

            print(
                f"{self.name} forwarding frame "
                f"to {target.name}"
            )

            if hasattr(target, 'receive_packet'):
                target.receive_packet(packet)

            elif hasattr(target, 'forward_packet'):
                target.forward_packet(packet)

        # UNKNOWN DESTINATION
        else:

            print(
                f"{self.name} does not know "
                f"{packet.dest_mac}"
            )

            print(f"{self.name} BROADCASTING FRAME")

            for device in self.devices:

                if hasattr(device, 'mac'):

                    if device.mac == packet.dest_mac:

                        print(
                            f"{self.name} found "
                            f"destination device"
                        )

                        self.mac_table[packet.dest_mac] = device

                        self.show_mac_table()

                        device.receive_packet(packet)

                elif hasattr(device, 'forward_packet'):

                    device.forward_packet(packet)