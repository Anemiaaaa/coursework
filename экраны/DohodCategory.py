from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage
import sys
import subprocess


if len(sys.argv) > 1:
    logged_in_user = sys.argv[1]
else:
    logged_in_user = None

print(f"Logged in user: {logged_in_user}")

class Application:
    def __init__(self, root):
        self.window = root
        self.window.geometry("542x511")
        self.window.configure(bg="#C4E0A6")
        self.canvas = self.create_canvas()
        self.assets_path = Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame DohodCategory")
        self.setup_buttons()
        self.setup_images()
        self.create_rectangle()
        self.Type = "Income"

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
        # Define button details in a list: (image filename, position x, position y, action)
        button_details = [
            ("button_1.png", 383.0, 310.0, 6),
            ("button_2.png", 214.0, 310.0, 5),
            ("button_3.png", 45.0, 310.0, 4),
            ("button_4.png", 383.0, 160.0, 3),
            ("button_5.png", 214.0, 160.0, 1),
            ("button_6.png", 45.0, 160.0, 2)
        ]
        for img_file, x, y, category in button_details:
            self.create_button(img_file, x, y, category)

    def create_button(self, img_file, x, y, category):
        button_image = PhotoImage(file=self.relative_to_assets(img_file))
        button = Button(
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_summ_opisanie_window(category),
            relief="flat"
        )
        button.image = button_image  # Keep a reference to the image
        button.place(x=x, y=y, width=113.9390640258789, height=117.91368865966797)

    def setup_images(self):
        image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(260.0, 56.0, image=image_image_1)
        self.canvas.image = image_image_1  # Keep a reference to the image

    def create_rectangle(self):
        self.canvas.create_rectangle(
            -6.499937485792088,
            89.73707292562653,
            549.0001250284158,
            101.26293562568912,
            fill="#63BD03",
            outline=""
        )

def main():
    root = Tk()
    app = Application(root)
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()
