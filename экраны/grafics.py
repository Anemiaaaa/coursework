from pathlib import Path
from tkinter import Frame, Canvas, Button, PhotoImage
from экраны.obshakPust import Obshiy
from экраны.dohodPustoi import DohodPustoi
from экраны.rashodPustoi import RashodPustoi

class Grafics(Frame):
    def __init__(self, parent, assets_path, logged_in_user):
        super().__init__(parent)  # Указываем родителя в базовом классе
        self.assets_path = assets_path
        self.logged_in_user = logged_in_user
        self.images = {}  # Словарь для хранения изображений
        self.create_widgets()
        self.setup_frame()
        self.load_content(self.open_obshakPust_window)

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def setup_frame(self):
        self.frame = Frame(self, bg="#000000", width=700, height=370)
        self.frame.place(x=30.0, y=250.0)

    def clear_frame(self):
        # Очистить текущий фрейм
        for widget in self.frame.winfo_children():
            widget.destroy()

    def load_content(self, content_loader):
        self.clear_frame()
        content_loader()

    def open_obshakPust_window(self):
        def obshakPust_content():
            assets_path = Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame obshakPust")
            obsh = Obshiy(self.frame, assets_path, self.logged_in_user)
            obsh.place(x=0, y=0, relwidth=1, relheight=1)
        self.load_content(obshakPust_content)

    def open_dohodPustoi_window(self):
        def dohodPustoi_content():
            assets_path = Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame dohodPustoi")
            dohod = DohodPustoi(self.frame, assets_path, self.logged_in_user)
            dohod.place(x=0, y=0, relwidth=1, relheight=1)
        self.load_content(dohodPustoi_content)

    def open_rashodPustoi_window(self):
        def rashodPustoi_content():
            assets_path = Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame rashodPustoi")
            rashod = RashodPustoi(self.frame, assets_path, self.logged_in_user)
            rashod.place(x=0, y=0, relwidth=1, relheight=1)
        self.load_content(rashodPustoi_content)

    def create_widgets(self):
        self.canvas = Canvas(
            self,
            bg="#C4E0A6",
            height=637,
            width=762,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(
            -2.0,
            123.0,
            761.9999901050287,
            125.99999999027409,
            fill="#000000",
            outline=""
        )

        self.images["image_1"] = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(381.0, 188.0, image=self.images["image_1"])

        self.images["image_2"] = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(196.0, 68.0, image=self.images["image_2"])

        self.images["button_1"] = PhotoImage(file=self.relative_to_assets("button_1.png"))
        Button(
            self,
            image=self.images["button_1"],
            borderwidth=0,
            highlightthickness=0,
            command=self.open_obshakPust_window,
            relief="flat"
        ).place(x=43.0, y=158.0, width=193.0, height=60.0)

        self.images["button_2"] = PhotoImage(file=self.relative_to_assets("button_2.png"))
        Button(
            self,
            image=self.images["button_2"],
            borderwidth=0,
            highlightthickness=0,
            command=self.open_dohodPustoi_window,
            relief="flat"
        ).place(x=284.0, y=159.0, width=193.0, height=60.0)

        self.images["button_3"] = PhotoImage(file=self.relative_to_assets("button_3.png"))
        Button(
            self,
            image=self.images["button_3"],
            borderwidth=0,
            highlightthickness=0,
            command=self.open_rashodPustoi_window,
            relief="flat"
        ).place(x=526.0, y=158.0, width=191.0, height=60.0)



