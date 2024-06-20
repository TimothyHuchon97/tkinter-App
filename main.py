import tkinter as tk
from tkinter import Toplevel, ttk
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
        self.style.configure("TCheckbutton", background="#202020", foreground="white", font=("Helvetica", 14))

        self.frame_side_bar = ttk.Frame(self.root, style="TFrame", width=150)
        self.frame_btns = ttk.Frame(self.frame_side_bar, style="TFrame")
        self.frame_content = ttk.Frame(self.root, style="TFrame")
        self.frame_bottom_bar = ttk.Frame(self.frame_content, style="TFrame")

        self.frame_side_bar.pack(side="left", fill="y")
        self.frame_btns.pack(side="left")
        self.frame_content.pack(side="left", fill="both", expand=True)
        self.frame_bottom_bar.pack(side="bottom", fill="x")

        self.map_widget = TkinterMapView(self.frame_content)
        self.map_widget.pack(fill="both", expand=True, padx=15, pady=(15, 0))

        self.check_red_wine = tk.BooleanVar()
        self.check_white_wine = tk.BooleanVar()

        self.check_btn_red_wine = ttk.Checkbutton(self.frame_bottom_bar, text="Tinto", style="TCheckbutton", 
                                                  variable=self.check_red_wine, onvalue=True, offvalue=False, 
                                                  command=self.controller.display_wine_markers_by_category)
        self.check_btn_white_wine = ttk.Checkbutton(self.frame_bottom_bar, text="Blanco", style="TCheckbutton", 
                                                  variable=self.check_white_wine, onvalue=True, offvalue=False, 
                                                  command=self.controller.display_wine_markers_by_category)

        self.check_btn_red_wine.grid(column=0, row=0, pady=15)
        self.check_btn_white_wine.grid(column=1, row=0, pady=15)

        self.frame_bottom_bar.columnconfigure(0, weight=1)
        self.frame_bottom_bar.columnconfigure(1, weight=1)

    def create_btns(self, wines_locations_infos):
        for key, value in wines_locations_infos.items():
            wine_location_btn = ttk.Button(
                self.frame_btns,
                text=key,
                cursor="hand2",
                command=lambda value=value, key=key: self.controller.display_wine_marker(value, key)
            )
            wine_location_btn.pack(fill="x", padx=20, pady=8)

    def set_up_info_window(self, key, value):
        info_window = Toplevel()
        info_window.title(key)
        info_window.geometry("900x700")

        style = ttk.Style()
        style.configure("vert.TFrame", background="#202020")
        style.configure("title.TLabel", font=("Helvetica", 16), foreground="white", background="#202020")

        frame_title = ttk.Frame(info_window, style="vert.TFrame", height=237)
        frame_image = ttk.Frame(info_window, style="yellow.TFrame", height=237)

        image_location = Image.open(f"images/zones/{key}.png").resize((850, 650))
        image_tk_location = ImageTk.PhotoImage(image_location)

        frame_title.pack(fill="both", expand=True)
        frame_image.pack(fill="both", expand=True)

        label_title = ttk.Label(frame_title,style="title.TLabel", text=key)
        label_image = ttk.Label(frame_image, image=image_tk_location)

        label_title.pack(expand=True, pady=(20, 10))
        label_image.pack(expand=True, padx=40, pady=(10, 20))

        info_window.mainloop()


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

    def display_wine_marker(self, wine_location_info, wine_location_key):
        latitude = wine_location_info[0][0]
        longitude = wine_location_info[0][1]

        wine_icon = ImageTk.PhotoImage(ICON_RED_WINE) if wine_location_info[1] == "Tinto" \
            else ImageTk.PhotoImage(
            ICON_WHITE_WINE)

        self.view.map_widget.set_marker(latitude, longitude, icon=wine_icon,
                                        command=lambda value=wine_location_info, key=wine_location_key: self.view.set_up_info_window(key, value))
        self.zoom_on_location(latitude, longitude, 7)

    def display_wine_markers_by_category(self):
        red_wine = self.view.check_red_wine.get()
        white_wine = self.view.check_white_wine.get()

        self.view.map_widget.delete_all_marker()
        for key, value in self.model.wines_location_info.items():
            if (red_wine and value[1] == "Tinto") or (white_wine and value[1] == "Blanco"):
                wine_icon = ImageTk.PhotoImage(ICON_RED_WINE) if value[1] == "Tinto" \
                    else ImageTk.PhotoImage(ICON_WHITE_WINE)
                wine_marker = self.view.map_widget.set_marker(value[0][0], value[0][1], icon=wine_icon, 
                                                              command=lambda value=value, key=key: self.view.set_up_info_window(key, value))
                wine_marker.set_text(key)
                self.zoom_on_location(40.416775, -3.703790, 6)


def main():
    root = tk.Tk()
    root.title("Vinos Ibericos - DocString Challenge")
    root.geometry("1000x800")

    app = WineAppController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
