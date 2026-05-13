import tkinter as tk


class NetworkVisualizer:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(
            "Enterprise Network Simulator"
        )

        self.root.geometry("1200x700")

        self.canvas = tk.Canvas(

            self.root,

            width=1200,
            height=700,

            bg="white"
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        self.positions = {}

    # ====================================
    # DRAW TOPOLOGY
    # ====================================

    def draw_topology(

        self,

        topology_data,

        devices
    ):

        self.canvas.delete("all")

        self.positions.clear()

        routers = topology_data["routers"]

        switches = topology_data["switches"]

        vms = topology_data["vms"]

        connections = topology_data["connections"]

        self.draw_routers(
            routers,
            devices
        )

        self.draw_switches(
            switches,
            devices
        )

        self.draw_vms(
            vms,
            devices
        )

        self.draw_connections(
            connections
        )

        self.root.update()

    # ====================================
    # ROUTERS
    # ====================================

    def draw_routers(

        self,

        routers,

        devices
    ):

        start_x = 180
        y = 120

        spacing = 170

        for i, router_name in enumerate(routers):

            x = start_x + (i * spacing)

            self.positions[router_name] = (
                x,
                y
            )

            router = devices[router_name]

            # SMALL ROUTER

            self.canvas.create_oval(

                x - 22,
                y - 22,

                x + 22,
                y + 22,

                fill="skyblue",

                width=2
            )

            self.canvas.create_text(

                x,
                y,

                text=router_name,

                font=(
                    "Arial",
                    8,
                    "bold"
                )
            )

            # SIDE TEXT

            info = (

                f"{router.ip}\n"

                f"{router.mac}"
            )

            self.canvas.create_text(

                x + 55,
                y,

                text=info,

                anchor="w",

                font=("Arial", 7)
            )

    # ====================================
    # SWITCHES
    # ====================================

    def draw_switches(

        self,

        switches,

        devices
    ):

        start_x = 250
        y = 300

        spacing = 250

        for i, switch_name in enumerate(switches):

            x = start_x + (i * spacing)

            self.positions[switch_name] = (
                x,
                y
            )

            switch = devices[switch_name]

            self.canvas.create_rectangle(

                x - 28,
                y - 18,

                x + 28,
                y + 18,

                fill="orange",

                width=2
            )

            self.canvas.create_text(

                x,
                y,

                text=switch_name,

                font=(
                    "Arial",
                    8,
                    "bold"
                )
            )

            info = (

                f"{switch.ip}\n"

                f"{switch.mac}"
            )

            self.canvas.create_text(

                x + 60,
                y,

                text=info,

                anchor="w",

                font=("Arial", 7)
            )

    # ====================================
    # VMS
    # ====================================

    def draw_vms(

        self,

        vms,

        devices
    ):

        start_x = 140
        y = 520

        spacing = 190

        for i, vm_data in enumerate(vms):

            vm_name = vm_data["name"]

            x = start_x + (i * spacing)

            self.positions[vm_name] = (
                x,
                y
            )

            vm = devices[vm_name]

            self.canvas.create_rectangle(

                x - 30,
                y - 18,

                x + 30,
                y + 18,

                fill="lightgreen",

                width=2
            )

            self.canvas.create_text(

                x,
                y,

                text=vm_name,

                font=(
                    "Arial",
                    8,
                    "bold"
                )
            )

            info = (

                f"{vm.ip}\n"

                f"{vm.mac}\n"

                f"VLAN {vm.vlan}"
            )

            self.canvas.create_text(

                x + 70,
                y,

                text=info,

                anchor="w",

                font=("Arial", 7)
            )

    # ====================================
    # CONNECTIONS
    # ====================================

    def draw_connections(

        self,

        connections
    ):

        for conn in connections:

            d1 = conn[0]
            d2 = conn[1]

            if (
                d1 not in self.positions
                or
                d2 not in self.positions
            ):

                continue

            x1, y1 = self.positions[d1]
            x2, y2 = self.positions[d2]

            self.canvas.create_line(

                x1,
                y1,

                x2,
                y2,

                width=2
            )

    # ====================================
    # PACKET ANIMATION
    # ====================================

    def animate_packet(

        self,

        path
    ):

        if len(path) < 2:

            return

        print("\nVISUAL PATH:")

        print(" -> ".join(path))

        for i in range(len(path) - 1):

            node1 = path[i]
            node2 = path[i + 1]

            if (
                node1 not in self.positions
                or
                node2 not in self.positions
            ):

                continue

            x1, y1 = self.positions[node1]
            x2, y2 = self.positions[node2]

            # SMALL PACKET

            packet = self.canvas.create_oval(

                x1 - 5,
                y1 - 5,

                x1 + 5,
                y1 + 5,

                fill="red"
            )

            self.root.update()

            steps = 30

            dx = (x2 - x1) / steps
            dy = (y2 - y1) / steps

            for _ in range(steps):

                self.canvas.move(
                    packet,
                    dx,
                    dy
                )

                self.root.update()

                self.root.after(20)

            self.canvas.delete(packet)

    # ====================================
    # RUN
    # ====================================

    def run(self):

        self.root.mainloop()