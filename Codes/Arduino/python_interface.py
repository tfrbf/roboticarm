import tkinter as tk
from tkinter import ttk
import math

def update_servo(angle, servo_number):
    print("Servo {} angle: {}".format(servo_number, angle))

class CircularScale(tk.Canvas):
    def __init__(self, master, servo_number, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.servo_number = servo_number
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.drag_to_scroll)
        self.draw_scale()

    def draw_scale(self):
        center_x = self.winfo_width() / 2
        center_y = self.winfo_height() / 2
        radius = min(center_x, center_y) - 5
        self.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="#c0c0c0")
        for angle in range(-90, 91, 10):
            x1 = center_x + (radius - 5) * math.cos(math.radians(angle))
            y1 = center_y + (radius - 5) * math.sin(math.radians(angle))
            x2 = center_x + radius * math.cos(math.radians(angle))
            y2 = center_y + radius * math.sin(math.radians(angle))
            self.create_line(x1, y1, x2, y2, fill="#c0c0c0")

    def start_drag(self, event):
        self._start_x = event.x
        self._start_y = event.y

    def drag_to_scroll(self, event):
        center_x = self.winfo_width() / 2
        center_y = self.winfo_height() / 2
        angle = math.degrees(math.atan2(event.y - center_y, event.x - center_x))
        if angle < -90:
            angle = -90
        elif angle > 90:
            angle = 90
        update_servo(angle, self.servo_number)

def main():
    root = tk.Tk()
    root.title("Robot Arm Control")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Helvetica", 12))

    servo_labels = ["Servo 1", "Servo 2", "Servo 3", "Servo 4", "Servo 5", "Servo 6"]
    for i, label in enumerate(servo_labels):
        ttk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5)
        scale = CircularScale(root, i+1, width=100, height=100, bg="#d9d9d9", highlightthickness=0)
        scale.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

    root.mainloop()

if __name__ == "__main__":
    main()
