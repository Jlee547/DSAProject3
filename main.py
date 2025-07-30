import tkinter as tk
from collections import defaultdict
from GraphGenerator import GraphGenerator


#node_count = int(input("How many nodes would you like to consider? "))
node_count = 1000
main_generator = GraphGenerator(node_count)


if node_count <= 10000:
        
    def search_1():
        print("Search_1")

    def search_2():
        print("Search_2")

    def on_canvas_click(event):
        x, y = event.x, event.y
        canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")

    # Create root, frame, buttons, and canvas

    root = tk.Tk()
    root.geometry("900x800")
    root.resizable(False, False)
    root.title("Pathfinding")

    top_frame = tk.Frame(root)
    top_frame.pack(side="top")

    button1 = tk.Button(top_frame, text="A*", command=search_1)
    button2 = tk.Button(top_frame, text="Dijkstras*", command=search_2)
    button1.pack(side="left", padx=5, pady=5)
    button2.pack(side="left", padx=5, pady=5)


    canvas = tk.Canvas(root, bg="white")
    canvas.pack(fill="both", expand=True)
    canvas.bind("<Button-1>", on_canvas_click)
    main_generator.draw_to_canvas(canvas)

    root.mainloop()


    

    