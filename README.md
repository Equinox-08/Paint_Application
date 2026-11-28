# Paint Application
Name: Adrian J. Tor <br>
Section: BS INFORTECH SE - 3A

## Description
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

Original Code

<img src="CT 5/Obrush.png" alt="Orig Brush Code" width="600" />

   So, what I did here, ma'am, was change the brush size slider range from `1` to `30` up to `1` to `100` so I can draw with much thicker strokes. I also added a helper function (`draw_pillow_stroke`) that adds rounded caps to the Pillow lines so that when I save the drawing, the size and smooth look match what's on the Tkinter canvas.

Updated code

<img src="CT 5/Nbrush.png" alt="New Brush Code" width="600" />

Result

<img src="CT 5/ResultBrush.png" alt="Result Brush" width="500" />

2. **Undo button:**
   For the Undo feature, ma'am, I made an `undo_stack` list that saves a snapshot of the canvas right before I start drawing, clearing, or opening an image. Whenever I click the **Undo** button, it simply pops the last saved snapshot and brings it back—so whether it was a freehand brush stroke or a shape, it removes my latest action cleanly.

Code

<img src="CT 5/undo.png" alt="undo" width="500" />

Result

<img src="CT 5/resultUndo.png" alt="Result Brush" width="200" />

3. **Filled shapes:**
   Here, ma'am, I added a **Fill: OFF / ON** toggle button so I can switch between outline-only shapes and solid filled shapes. When it's toggled ON, both the live preview while dragging and the final shape saved on the Pillow image get filled with whatever color I currently have selected.

Code

<img src="CT 5/Fill.png" alt="undo" width="500" />

Result

<img src="CT 5/FillR.png" alt="Result Brush" width="200" />

4. **Extra shape tool:**
   Aside from Line, Rectangle, and Oval, ma'am, I added a **Triangle** tool. I calculated the three corner points based on where I drag the mouse so it shows a live triangle preview as I drag, and once I release the mouse button, it saves the triangle directly onto the Pillow image.

Code

<img src="CT 5/shapeCode1.png" alt="Result Brush" width="400" />

<img src="CT 5/shapeCode2.png" alt="Result Brush" width="400" />

Result

<img src="CT 5/resultCode.png" alt="Result Brush" width="500" />

5. **Confirm before clearing:**
   To avoid accidentally deleting my drawing, ma'am, I updated the `clear_canvas()` function to pop up a confirmation box using `messagebox.askyesno()` with **Yes** and **No** buttons. It only wipes the canvas clean if I click **Yes**.

Code

<img src="CT 5/Clear.png" alt="Result Brush" width="400" />

Result

<img src="CT 5/ConfirmC.png" alt="Result Brush" width="500" />

6. **Quick colors:**
   Instead of always opening the full color picker, ma'am, I added a Quick Colors bar right below the main toolbar with six one-click buttons: **Black**, **Red**, **Blue**, **Green**, **Yellow**, and **Purple**. Clicking any of them immediately switches my active color (and automatically switches back to the brush if I was using the eraser).

Code

<img src="CT 5/ColorsC.png" alt="Result Brush" width="400" />

Result

<img src="CT 5/ColorsR.png" alt="Result Brush" width="500" />

7. **Screenshot of the whole UI design:**

<img src="CT 5/SS.png" alt="Full UI Image" width="850" />
