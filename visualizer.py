import tkinter as tk

class NetworkVisualizer:
    def __init__(self, routers):
        self.window = tk.Tk()
        self.window.title("Network Simulation")

        self.canvas = tk.Canvas(self.window, width=800, height=500)
        self.canvas.pack()

        self.positions = {
            "R1": (100, 250),
            "R2": (300, 100),
            "R3": (500, 100),
            "R4": (700, 250)
        }

        self.draw_network()

    def draw_network(self):
        # Draw routers
        for name, (x, y) in self.positions.items():
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightblue")
            self.canvas.create_text(x, y, text=name)

        # Draw connections
        connections = [("R1","R2"), ("R2","R3"), ("R3","R4"), ("R1","R4")]

        for r1, r2 in connections:
            x1, y1 = self.positions[r1]
            x2, y2 = self.positions[r2]
            self.canvas.create_line(x1, y1, x2, y2)

    def animate_packet(self, path):
        coords = [self.positions[r.name] for r in path]

        packet = self.canvas.create_oval(0,0,10,10, fill="red")

        def move(index):
            if index >= len(coords):
                return

            x, y = coords[index]
            self.canvas.coords(packet, x-5, y-5, x+5, y+5)

            self.window.after(800, move, index+1)

        move(0)

    def run(self):
        self.window.mainloop()