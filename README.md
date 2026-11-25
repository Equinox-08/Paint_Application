# Atelier — Studio Paint

A desktop Paint application built with Python, **Tkinter**, and **Pillow (PIL)** featuring a custom dark studio interface, live shape previewing, undo history, and image import/export.

## Setup & Run

1. Open your project folder in **Visual Studio Code**.
2. Open the terminal (<kbd>Ctrl</kbd> + <kbd>`</kbd>) and install Pillow:

```bash
python -m pip install pillow
```

3. Run the application:

```bash
python paint_application.py
```

## REQUIREMENTS COMPLETED

1. **Bigger brush range:**
   Updated the `Brush Size` slider (`size_slider`) from `from_=1, to=30` to `from_=1, to=100`, and added `draw_pillow_stroke()` with round endcaps so freehand strokes and shapes saved in the Pillow image match the Tkinter canvas size and appearance.

2. **Undo button:**
   Added an `Undo` button and `undo_stack` history tracking (`save_undo_state()` and `undo()`) that captures snapshots before every drawing action, canvas clear, or image load—reverting both freehand strokes and shapes cleanly.

3. **Filled shapes:**
   Added a `Fill: OFF / ON` toggle button (`toggle_fill()`) that fills rectangles, ovals, and triangles with the active drawing color during both live drag preview (`preview_shape_drawing()`) and final Pillow rendering (`finish_drawing()`).

4. **Extra shape tool:**
   Added a `Triangle` tool (`get_triangle_points()`) alongside Line, Rectangle, and Oval, displaying a live polygon preview while dragging and saving the completed triangle onto the Pillow image on mouse release.

5. **Confirm before clearing:**
   Updated `clear_canvas()` to display a `messagebox.askyesno()` confirmation dialog with **Yes** and **No** options before resetting the canvas back to white.

6. **Quick colors:**
   Added a Quick Colors bar with six one-click color buttons (**Black**, **Red**, **Blue**, **Green**, **Yellow**, and **Purple**) via `set_color()` that immediately change the active drawing color (and switch back to the brush if the eraser was selected).

7. **Screenshot of the whole UI design:**

<img src="Screenshot.png" alt="Atelier Studio Paint Full UI" width="850" />
