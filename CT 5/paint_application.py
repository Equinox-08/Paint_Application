import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk

# 1. PREMIUM STUDIO COLOR PALETTE AND TYPOGRAPHY
BG_PRIMARY = "#12151C"       # deep obsidian-slate window background
PANEL_BG = "#1B202C"         # elevated charcoal-slate toolbar surface
BUTTON_BG = "#252C3D"        # sleek button surface
BUTTON_HOVER = "#343E54"     # hovered / pressed button surface
ACCENT_GOLD = "#D4AF37"      # warm champagne-gold accent for active/highlight states
ACCENT_HOVER = "#E5C158"     # lighter gold hover state
TEXT_PRIMARY = "#F3EFE6"     # crisp warm ivory text
TEXT_MUTED = "#A6AEBE"       # subtle slate-silver label text
BORDER_ACCENT = "#3A4256"    # refined subtle border around canvas

FONT_MAIN = ("Segoe UI", 9, "bold")
FONT_LABEL = ("Segoe UI", 9)

QUICK_COLORS = ["black", "red", "blue", "green", "yellow", "purple"]

# 2. MAIN WINDOW AND CANVAS SETTINGS
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 500

root = tk.Tk()
root.title("Atelier — Studio Paint")
root.geometry("1140x740")
root.configure(bg=BG_PRIMARY)

canvas_frame = tk.Frame(root, bg=BORDER_ACCENT, padx=2, pady=2)
canvas_frame.pack(padx=20, pady=(14, 8))

canvas = tk.Canvas(
    canvas_frame,
    width=CANVAS_WIDTH,
    height=CANVAS_HEIGHT,
    bg="white",
    cursor="cross",
    highlightthickness=0,
)
canvas.pack()

# Pillow image stores the drawing so it can be saved
image = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")
draw = ImageDraw.Draw(image)
canvas_image = None
undo_stack = []
MAX_UNDO = 30

# 3. DRAWING SETTINGS
current_color = "black"
brush_size = 5
tool = "brush"
fill_shapes = False
start_x = start_y = None
last_x = last_y = None
preview_shape = None


def save_undo_state():
    """Save a copy of the current image onto the undo stack."""
    if len(undo_stack) >= MAX_UNDO:
        undo_stack.pop(0)
    undo_stack.append(image.copy())


def undo():
    """Revert to the previous drawing state."""
    global image, draw, preview_shape
    if not undo_stack:
        messagebox.showinfo("Undo", "Nothing left to undo.")
        return
    image = undo_stack.pop()
    draw = ImageDraw.Draw(image)
    preview_shape = None
    refresh_canvas()


# 4. COLOR AND TOOL FUNCTIONS
def set_color(new_color):
    """Set the active drawing color immediately."""
    global current_color, tool
    current_color = new_color
    if tool == "eraser":
        tool = "brush"
    color_button.config(bg=current_color)


def choose_color():
    """Open the color chooser and update the drawing color."""
    selected = colorchooser.askcolor(title="Choose a color", initialcolor=current_color)
    if selected[1] is not None:
        set_color(selected[1])


def set_tool(selected_tool):
    """Change the active drawing tool."""
    global tool
    tool = selected_tool


def toggle_fill():
    """Toggle whether shapes are filled with the current color."""
    global fill_shapes
    fill_shapes = not fill_shapes
    fill_button.config(
        text=f"Fill: {'ON' if fill_shapes else 'OFF'}",
        bg=ACCENT_GOLD if fill_shapes else BUTTON_BG,
        fg=BG_PRIMARY if fill_shapes else TEXT_PRIMARY,
    )


def change_brush_size(value):
    """Update the brush size using the slider."""
    global brush_size
    brush_size = int(float(value))


def get_triangle_points(x1, y1, x2, y2):
    """Return three vertices for a triangle within the bounding box."""
    top_x = (x1 + x2) // 2
    return [(top_x, y1), (x1, y2), (x2, y2)]


def draw_pillow_stroke(x1, y1, x2, y2, color, size):
    """Draw a smooth stroke on the Pillow image matching Tkinter round caps."""
    draw.line((x1, y1, x2, y2), fill=color, width=size)
    radius = size / 2
    draw.ellipse((x1 - radius, y1 - radius, x1 + radius, y1 + radius), fill=color, outline=color)
    draw.ellipse((x2 - radius, y2 - radius, x2 + radius, y2 + radius), fill=color, outline=color)


# 5. FREEHAND AND SHAPE DRAWING
def start_drawing(event):
    """Save undo state and record the starting mouse position."""
    global last_x, last_y, start_x, start_y
    save_undo_state()
    last_x, last_y = event.x, event.y
    start_x, start_y = event.x, event.y


def draw_motion(event):
    """Draw while the left mouse button is held."""
    global last_x, last_y
    color = "white" if tool == "eraser" else current_color
    if tool in ("brush", "eraser"):
        canvas.create_line(
            last_x, last_y, event.x, event.y,
            fill=color, width=brush_size, capstyle=tk.ROUND, smooth=True,
        )
        draw_pillow_stroke(last_x, last_y, event.x, event.y, color, brush_size)
        last_x, last_y = event.x, event.y
    else:
        preview_shape_drawing(event)


def preview_shape_drawing(event):
    """Show a temporary shape while the mouse is dragged."""
    global preview_shape
    if preview_shape is not None:
        canvas.delete(preview_shape)

    shape_fill = current_color if fill_shapes else ""

    if tool == "line":
        preview_shape = canvas.create_line(
            start_x, start_y, event.x, event.y,
            fill=current_color, width=brush_size,
        )
    elif tool == "rectangle":
        preview_shape = canvas.create_rectangle(
            start_x, start_y, event.x, event.y,
            outline=current_color, fill=shape_fill, width=brush_size,
        )
    elif tool == "oval":
        preview_shape = canvas.create_oval(
            start_x, start_y, event.x, event.y,
            outline=current_color, fill=shape_fill, width=brush_size,
        )
    elif tool == "triangle":
        pts = get_triangle_points(start_x, start_y, event.x, event.y)
        preview_shape = canvas.create_polygon(
            pts, outline=current_color, fill=shape_fill, width=brush_size,
        )


def finish_drawing(event):
    """Store the completed shape in the Pillow image."""
    global preview_shape
    shape_fill = current_color if fill_shapes else None

    if tool == "line":
        draw.line(
            (start_x, start_y, event.x, event.y),
            fill=current_color, width=brush_size,
        )
    elif tool == "rectangle":
        draw.rectangle(
            (start_x, start_y, event.x, event.y),
            outline=current_color, fill=shape_fill, width=brush_size,
        )
    elif tool == "oval":
        draw.ellipse(
            (start_x, start_y, event.x, event.y),
            outline=current_color, fill=shape_fill, width=brush_size,
        )
    elif tool == "triangle":
        pts = get_triangle_points(start_x, start_y, event.x, event.y)
        draw.polygon(
            pts, outline=current_color, fill=shape_fill, width=brush_size,
        )

    if tool in ("line", "rectangle", "oval", "triangle"):
        preview_shape = None
        refresh_canvas()


# 6. CANVAS MANAGEMENT
def refresh_canvas():
    """Display the current Pillow image on the Tkinter canvas."""
    global canvas_image
    canvas.delete("all")
    canvas_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=canvas_image)


def clear_canvas():
    """Ask for confirmation before clearing the canvas to blank white."""
    global image, draw, preview_shape
    confirm = messagebox.askyesno(
        "Confirm Clear",
        "Are you sure you want to clear the entire canvas?",
    )
    if confirm:
        save_undo_state()
        image = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "white")
        draw = ImageDraw.Draw(image)
        preview_shape = None
        refresh_canvas()


# 7. OPEN AND SAVE IMAGE
def open_image():
    """Open an image and resize it to fit the canvas."""
    global image, draw
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if file_path:
        try:
            save_undo_state()
            opened_image = Image.open(file_path).convert("RGB")
            opened_image = opened_image.resize((CANVAS_WIDTH, CANVAS_HEIGHT))
            image = opened_image
            draw = ImageDraw.Draw(image)
            refresh_canvas()
        except Exception as error:
            messagebox.showerror("Error", f"Could not open image:\n{error}")


def save_image():
    """Save the current drawing as an image file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("Bitmap Image", "*.bmp"),
        ],
    )
    if file_path:
        try:
            image.save(file_path)
            messagebox.showinfo("Saved", "Your drawing has been saved!")
        except Exception as error:
            messagebox.showerror("Error", f"Could not save image:\n{error}")


# 8. TOOLBARS
def make_button(parent, text, command, bg=BUTTON_BG, fg=TEXT_PRIMARY):
    """Create a sleek studio button."""
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground=BUTTON_HOVER,
        activeforeground=TEXT_PRIMARY,
        font=FONT_MAIN,
        relief="flat",
        padx=9,
        pady=4,
        cursor="hand2",
    )


toolbar = tk.Frame(root, bg=PANEL_BG, padx=10, pady=7)
toolbar.pack(pady=(2, 5))

color_button = make_button(toolbar, "Choose Color", choose_color)
color_button.pack(side="left", padx=3)

make_button(toolbar, "Brush", lambda: set_tool("brush")).pack(side="left", padx=3)
make_button(toolbar, "Eraser", lambda: set_tool("eraser")).pack(side="left", padx=3)
make_button(toolbar, "Line", lambda: set_tool("line")).pack(side="left", padx=3)
make_button(toolbar, "Rectangle", lambda: set_tool("rectangle")).pack(side="left", padx=3)
make_button(toolbar, "Oval", lambda: set_tool("oval")).pack(side="left", padx=3)
make_button(toolbar, "Triangle", lambda: set_tool("triangle")).pack(side="left", padx=3)

fill_button = make_button(toolbar, "Fill: OFF", toggle_fill)
fill_button.pack(side="left", padx=3)

tk.Label(
    toolbar, text="Brush Size:", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL
).pack(side="left", padx=(10, 3))

size_slider = tk.Scale(
    toolbar,
    from_=1,
    to=100,
    orient="horizontal",
    command=change_brush_size,
    length=110,
    bg=PANEL_BG,
    fg=TEXT_PRIMARY,
    troughcolor=BUTTON_BG,
    activebackground=ACCENT_GOLD,
    highlightthickness=0,
)
size_slider.set(5)
size_slider.pack(side="left", padx=3)

make_button(toolbar, "Undo", undo).pack(side="left", padx=3)
make_button(toolbar, "Clear", clear_canvas).pack(side="left", padx=3)
make_button(toolbar, "Open", open_image).pack(side="left", padx=3)
make_button(toolbar, "Save", save_image, bg=ACCENT_GOLD, fg=BG_PRIMARY).pack(side="left", padx=3)

# Quick colors bar
quick_color_bar = tk.Frame(root, bg=PANEL_BG, padx=10, pady=5)
quick_color_bar.pack(pady=(0, 10))

tk.Label(
    quick_color_bar, text="Quick Colors:", bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_LABEL
).pack(side="left", padx=(0, 6))

for q_color in QUICK_COLORS:
    swatch = tk.Button(
        quick_color_bar,
        text=q_color.capitalize(),
        command=lambda c=q_color: set_color(c),
        bg=q_color,
        fg="white" if q_color in ("black", "blue", "green", "purple") else "black",
        activebackground=q_color,
        font=FONT_MAIN,
        relief="flat",
        padx=9,
        pady=3,
        cursor="hand2",
    )
    swatch.pack(side="left", padx=3)

# 9. CONNECT MOUSE EVENTS AND RUN
canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw_motion)
canvas.bind("<ButtonRelease-1>", finish_drawing)

root.mainloop()