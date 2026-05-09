import tkinter as tk
import time

class NetworkVisualizer:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Network Packet Simulator")

        self.canvas = tk.Canvas(
            self.root,
            width=1000,
            height=600,
            bg="white"
        )

        self.canvas.pack()

        # =========================
        # NODE POSITIONS
        # =========================

        self.positions = {

            "VM1": (100, 100),
            "VM3": (100, 300),

            "S1": (250, 200),

            "R1": (400, 200),
            "R2": (550, 200),
            "R3": (700, 200),
            "R4": (850, 200),

            "S2": (850, 400),

            "VM2": (700, 500),
            "VM4": (950, 500),
        }

        # =========================
        # CONNECTIONS
        # =========================

        self.connections = [

            ("VM1", "S1"),
            ("VM3", "S1"),

            ("S1", "R1"),

            ("R1", "R2"),
            ("R2", "R3"),
            ("R3", "R4"),

            ("R4", "S2"),

            ("S2", "VM2"),
            ("S2", "VM4"),
        ]

        self.draw_network()

    # =========================
    # DRAW NETWORK
    # =========================

    def draw_network(self):

        # Draw links
        for a, b in self.connections:

            x1, y1 = self.positions[a]
            x2, y2 = self.positions[b]

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                width=3
            )

        # Draw nodes
        for node, (x, y) in self.positions.items():

            color = "lightblue"

            if node.startswith("R"):
                color = "orange"

            elif node.startswith("S"):
                color = "lightgreen"

            elif node.startswith("VM"):
                color = "pink"

            self.canvas.create_oval(
                x - 30,
                y - 30,
                x + 30,
                y + 30,
                fill=color
            )

            self.canvas.create_text(
                x,
                y,
                text=node,
                font=("Arial", 12, "bold")
            )

    # =========================
    # ANIMATE PACKET
    # =========================

    def animate_packet(self, path):

        print("\nVISUAL PATH:")
        print(" -> ".join(path))

        packet = None

        for i in range(len(path) - 1):

            start = path[i]
            end = path[i + 1]

            x1, y1 = self.positions[start]
            x2, y2 = self.positions[end]

            steps = 40

            dx = (x2 - x1) / steps
            dy = (y2 - y1) / steps

            # Remove previous packet
            if packet:
                self.canvas.delete(packet)

            # Create packet
            packet = self.canvas.create_oval(
                x1 - 10,
                y1 - 10,
                x1 + 10,
                y1 + 10,
                fill="red"
            )

            # Animate movement
            for _ in range(steps):

                self.canvas.move(packet, dx, dy)

                self.root.update()

                time.sleep(0.03)

        # Keep final packet visible
        self.root.update()

    # =========================
    # RUN GUI
    # =========================

    def run(self):

        self.root.mainloop()