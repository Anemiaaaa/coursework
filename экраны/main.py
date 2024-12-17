from tkinter import *
from pathlib import Path
import sys
from glavnaya import Application
from settings import Settings
from istoria import HistoryFrame
from categories import Categories
from grafics import Grafics

class App:
    def __init__(self, root, assets_path, logged_in_user):
        self.root = root
        self.assets_path = assets_path
        self.logged_in_user = logged_in_user
        self.setup_window()
        self.setup_canvas()
        self.setup_frame()
        self.setup_buttons()

    def relative_to_assets(self, path: str) -> Path:
        return self.assets_path / Path(path)

    def setup_window(self):
        self.root.geometry("1080x637")
        self.root.configure(bg="#C4E0A6")

    def setup_canvas(self):
        self.canvas = Canvas(
            self.root,
            bg="#C4E0A6",
            height=637,
            width=1093,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=1.5)
        self.canvas.create_rectangle(
            1.0,
            121.0,
            314.9999960580535,
            123.99999995112421,
            fill="#000000",
            outline=""
        )
        self.canvas.create_rectangle(
            307.0,
            -10.0,
            317.9999999884383,
            637.0000110260298,
            fill="#63BD03",
            outline=""
        )

    def setup_frame(self):
        self.frame = Frame(self.root, bg="#000000", width=775, height=637)
        self.frame.place(x=318.0, y=0.0)

    def setup_buttons(self):
        button_images = [
            ("button_1.png", self.open_settings_window, 25.0, 568.0, 50.0, 51.0),
            ("button_2.png", self.open_categories_window, 27.0, 445.0, 269.0, 62.0),
            ("button_3.png", self.open_grafics_window, 25.0, 356.0, 266.0, 68.0),
            ("button_4.png", self.open_istoria_window, 27.0, 265.0, 264.0, 73.0),
            ("button_5.png", self.open_glavnaya_window, 24.0, 181.0, 268.0, 64.0),
            ("button_6.png", lambda: print("button_6 clicked"), 0.0, 0.0, 302.0, 116.0)
        ]

        for image, command, x, y, width, height in button_images:
            button_image = PhotoImage(file=self.relative_to_assets(image))
            button = Button(
                image=button_image,
                borderwidth=0,
                highlightthickness=0,
                command=command,
                relief="flat"
            )
            button.image = button_image  # Сохраняем ссылку на изображение
            button.place(x=x, y=y, width=width, height=height)

    def clear_frame(self):
        # Очистить текущий фрейм
        for widget in self.frame.winfo_children():
            widget.destroy()

    def load_content(self, content_loader):
        self.clear_frame()
        content_loader()

    def open_glavnaya_window(self):
        def glavnaya_content():
            assets_path = Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame glavnaya")
            Application(self.frame, assets_path, self.logged_in_user)
        self.load_content(glavnaya_content)

    def open_settings_window(self):
        def settings_content():
            assets_path = Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame settings")
            Settings(self.frame, assets_path, self.logged_in_user)
        self.load_content(settings_content)

    def open_istoria_window(self):
        def istoria_content():
            assets_path = Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame istoria")
            history = HistoryFrame(self.frame, assets_path, self.logged_in_user)
            history.place(x=0, y=0, relwidth=1, relheight=1)
        self.load_content(istoria_content)

    def open_categories_window(self):
        def categories_content():
            assets_path = Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame categories")
            categories = Categories(self.frame, assets_path, self.logged_in_user)
            categories.place(x=0, y=0, relwidth=1, relheight=1)  # Размещаем Categories в self.frame
        self.load_content(categories_content)

    def open_grafics_window(self):
        def grafics_content():
            assets_path = Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame grafics")
            grafics = Grafics(self.frame, assets_path, self.logged_in_user)
            grafics.place(x=0, y=0, relwidth=1, relheight=1)  # Размещаем Grafics в self.frame
        self.load_content(grafics_content)


if __name__ == "__main__":
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\amiri\PycharmProjects\kursach\frames\frame main")

    logged_in_user = sys.argv[1] if len(sys.argv) > 1 else None
    if not logged_in_user:
        print("Ошибка: Не передано имя пользователя.")
        sys.exit(1)

    root = Tk()
    app = App(root, ASSETS_PATH, logged_in_user)

    # Открыть главный экран сразу после создания экземпляра приложения
    app.open_glavnaya_window()
    root.resizable(False, False)
    root.mainloop()
