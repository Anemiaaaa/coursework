import subprocess
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import sys

# Get the username passed as a command-line argument
if len(sys.argv) > 1:
    logged_in_user = sys.argv[1]
else:
    logged_in_user = None

print(f"Logged in user: {logged_in_user}")

class MainWindow:
    def __init__(self, root):
        self.window = root
        self.window.geometry("542x511")
        self.window.configure(bg="#C4E0A6")
        self.canvas = self.create_canvas()
        self.assets_path = Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame RashodCategory")
        self.setup_buttons()
        self.setup_image()
        self.create_rectangle()
        self.Type = "Expense"

    def create_canvas(self):
        canvas = Canvas(
            self.window,
            bg="#C4E0A6",
            height=511,
            width=542,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        canvas.place(x=0, y=0)
        return canvas

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def open_summ_opisanie_window(self, category):
        self.window.destroy()
        subprocess.Popen(["python", r"C:\\Users\\amiri\\PycharmProjects\\kursach\\экраны\\SummaOpisanie.py",  str(category), logged_in_user, self.Type])

    def setup_buttons(self):
        # Define button details
        button_details = [
            ("button_1.png", 6, 360.35, 304.45),
            ("button_2.png", 5, 212.14, 304.45),
            ("button_3.png", 4, 63.0, 304.45),
            ("button_4.png", 3, 360.35, 160.0),
            ("button_5.png", 2, 212.14, 160.0),
            ("button_6.png", 1, 63.94, 160.0)
        ]

        for img_file, category, x, y in button_details:
            self.create_button(img_file, category, x, y)

    def create_button(self, img_file, category, x, y):
        button_image = PhotoImage(file=self.relative_to_assets(img_file))
        button = Button(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_summ_opisanie_window(category),
            relief="flat"
        )
        button.image = button_image  # Keep a reference to the image
        button.place(x=x, y=y, width=114.65, height=118.65)

    def setup_image(self):
        image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(260.0, 56.0, image=image_image_1)
        self.canvas.image = image_image_1  # Keep a reference to the image

    def create_rectangle(self):
        self.canvas.create_rectangle(
            -6.5,
            89.74,
            549.0,
            101.26,
            fill="#63BD03",
            outline=""
        )

def main():
    root = Tk()
    app = MainWindow(root)
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()
