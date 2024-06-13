import tkinter as tk
from PIL import Image, ImageTk
import tkintermapview
from wine_locations_data import DO_VINOS

ICON_WHITE_WINE = Image.open("images/blanco.webp").resize((50,50))
ICON_RED_WINE = Image.open("images/tinto.webp").resize((50,50))

def display_wine_marker(value):
    wine_icon = ImageTk.PhotoImage(ICON_RED_WINE) if value[1] == "Tinto" else ImageTk.PhotoImage(ICON_WHITE_WINE)
    map_widget.set_marker(value[0][0], value[0][1], icon=wine_icon)


root = tk.Tk()
root.geometry("900x700")
root.title("Vinos Ibericos - Docstring Challenge")

frame_side_bar = tk.Frame(root, bg="#202020", width=150)
frame_side_bar.pack(side="left", fill="y")

frame_btns = tk.Frame(frame_side_bar, bg="#202020")
frame_btns.pack(side="left")

for key, value in DO_VINOS.items():
    vine_location_btn = tk.Button(
        frame_btns,
        text=key,
        bg="#ED413E",
        fg="white",
        relief="ridge",
        cursor="hand2",
        command=lambda value=value: display_wine_marker(value)
    )
    vine_location_btn.pack(fill="x", padx=20, pady=8)

content_frame = tk.Frame(root, bg="#202020")
content_frame.pack(side="left", fill="both", expand=True)

map_widget = tkintermapview.TkinterMapView(content_frame)
map_widget.pack(fill="both", expand=True, padx=20, pady=20)

map_widget.set_address("spain")
map_widget.set_zoom(6)

root.mainloop()