import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkintermapview import TkinterMapView
from wine_locations_data import DO_VINOS

ICON_WHITE_WINE = Image.open("images/blanco.webp").resize((50,50))
ICON_RED_WINE = Image.open("images/tinto.webp").resize((50,50))

class TkApp(tk.Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.geometry("1000x800")
        self.configure_style("TFrame", "#202020")
        self.create_side_bar_btns()
        self.frame_content = self.create_frame_content()
        self.map_widget = self.create_map(self.frame_content)
        self.mainloop()

    def configure_style(self, style_name, bg_color):
        style = ttk.Style()
        style.configure(style_name, background=bg_color)

    def create_side_bar_btns(self):
        frame_side_bar = ttk.Frame(self, style="TFrame", width=150)
        frame_btns = ttk.Frame(frame_side_bar, style="TFrame")

        frame_side_bar.pack(side="left", fill="y")
        frame_btns.pack(side="left")

        self.create_btns(frame_btns)

    def create_frame_content(self):
        frame_content = ttk.Frame(self, style="TFrame")
        frame_content.pack(side="left", fill="both", expand=True)
        return frame_content

    def create_map(self, frame_content):
        map_widget = TkinterMapView(frame_content)
        map_widget.pack(fill="both", expand=True, padx=20, pady=20)
        self.initialize_map(map_widget, "spain", 6)
        return map_widget

    def initialize_map(self, map_widget, address, zoom):
        map_widget.set_address(address)
        map_widget.set_zoom(zoom)

    def create_btns(self, frame_btns):
        for key, value in DO_VINOS.items():
            vine_location_btn = ttk.Button(
                frame_btns,
                text=key,
                cursor="hand2",
                command= lambda value=value: self.display_wine_marker(value)
            )
            vine_location_btn.pack(fill="x", padx=20, pady=8)

    def display_wine_marker(self, value):
        wine_icon = ImageTk.PhotoImage(ICON_RED_WINE) if value[1] == "Tinto" else ImageTk.PhotoImage(ICON_WHITE_WINE)
        self.map_widget.set_marker(value[0][0], value[0][1], icon=wine_icon)


if __name__ == "__main__":
    TkApp("Vinos Ibericos - DocString Challenge")