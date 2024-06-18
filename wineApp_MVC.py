import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkintermapview import TkinterMapView
from wine_locations_data import DO_VINOS

ICON_WHITE_WINE = Image.open("images/blanco.webp").resize((50, 50))
ICON_RED_WINE = Image.open("images/tinto.webp").resize((50, 50))


class WineAppModel:
    def __init__(self):
        self.wines_location_info = DO_VINOS


class WineAppView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#202020")

        self.frame_side_bar = ttk.Frame(self.root, style="TFrame", width=150)
        self.frame_btns = ttk.Frame(self.frame_side_bar, style="TFrame")
        self.frame_content = ttk.Frame(self.root, style="TFrame")

        self.frame_side_bar.pack(side="left", fill="y")
        self.frame_btns.pack(side="left")
        self.frame_content.pack(side="left", fill="both", expand=True)

        self.map_widget = TkinterMapView(self.frame_content)
        self.map_widget.pack(fill="both", expand=True, padx=20, pady=20)

    def create_btns(self, wines_locations_infos):
        for key, value in wines_locations_infos.items():
            vine_location_btn = ttk.Button(
                self.frame_btns,
                text=key,
                cursor="hand2",
                command=lambda value=value: self.controller.display_wine_marker(value)
            )
            vine_location_btn.pack(fill="x", padx=20, pady=8)


class WineAppController:
    def __init__(self, root):
        self.root = root
        self.model = WineAppModel()
        self.view = WineAppView(root, self)
        self.set_up_buttons()
        self.zoom_on_location(40.416775, -3.703790, 6)

    def zoom_on_location(self, latitude, longitude, zoom):
        self.view.map_widget.set_position(latitude, longitude)
        self.view.map_widget.set_zoom(zoom)

    def set_up_buttons(self):
        wines_locations_infos = self.model.wines_location_info
        self.view.create_btns(wines_locations_infos)

    def display_wine_marker(self, wine_location_info):
        latitude = wine_location_info[0][0]
        longitude = wine_location_info[0][1]

        wine_icon = ImageTk.PhotoImage(ICON_RED_WINE) if wine_location_info[1] == "Tinto" else ImageTk.PhotoImage(
            ICON_WHITE_WINE)

        self.view.map_widget.set_marker(latitude, longitude, icon=wine_icon)
        self.zoom_on_location(latitude, longitude, 7)


def main():
    root = tk.Tk()
    root.title("Vinos Ibericos - DocString Challenge")
    root.geometry("1000x800")

    app = WineAppController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
