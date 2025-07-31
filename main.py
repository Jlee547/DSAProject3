import tkinter as tk
from collections import defaultdict
from GraphGenerator import GraphGenerator
from jasonLee import dijkstra
from lucaColl import astar
import math
import time


#node_count = int(input("How many nodes would you like to consider? "))
node_count = 100
main_generator = GraphGenerator(node_count)

class State:
    def __init__(self):
        self.curr_source = None
        self.curr_destination = None
        self.last_clicked = "curr_source"
        self.drawn_lines = []
    
    def reset_state(self):
        self.curr_source = None
        self.curr_destination = None
        self.last_clicked = "curr_source"
        self.drawn_lines = []

state = State()


if node_count <= 10000:

    def clear_board():
        for l_id in state.drawn_lines:
            canvas.delete(l_id)

    def reset_board():
        canvas.delete("all")
        main_generator.reset_graph(100)
        main_generator.draw_to_canvas(canvas)
        main_generator.draw_edges(canvas)
        main_generator.generate_subset_graph()
        state.reset_state()


    def draw_path(path):
        for index, id in enumerate(path):
            if index == len(path) - 1:
                return

            
            node_g = main_generator.nodes
            line_id = canvas.create_line(node_g[id].x, node_g[id].y, node_g[path[index + 1]].x, node_g[path[index + 1]].y, fill="green", width=3)
            state.drawn_lines.append(line_id)


        
    def search_1():
        if state.drawn_lines:
            clear_board

        start = time.time()
        if not state.curr_destination or not state.curr_source:
            print("No endpoints")
            message_box.configure(text="No source or destination")
            return
        else:
            message_box.configure(text="")

        res = dijkstra(state.curr_source.id, state.curr_destination.id,main_generator.graph_subset)
        draw_path(res)
        end = time.time()
        formatted = f"{end - start:.{6}f}"

        message_box.configure(text=f"Elapsed time: {formatted}")
        
        print(res)

    def search_2():
        if state.drawn_lines:
            clear_board

        start = time.time()
        if not state.curr_destination or not state.curr_source:
            print("No endpoints")
            message_box.configure(text="No source or destination")
            return
        else:
            message_box.configure(text="")

        res = astar(state.curr_source.id, state.curr_destination.id, main_generator.graph_subset)
        draw_path(res)

        end = time.time()
        formatted = f"{end - start:.{6}f}"
        message_box.configure(text=f"Elapsed time: {formatted}")
        
        print(res)

    def on_canvas_click(event):
        x, y = event.x, event.y
        canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")

    def get_closest_node_click(event):
        if state.drawn_lines:
            clear_board()


        x, y = event.x, event.y
        print(f"Clicked at {x}, {y}")
        closest_dist = float('inf')
        closest_node = 0

        for id, node in main_generator.nodes.items():
            curr_dist = math.sqrt((node.x - x) ** 2 + (node.y - y)** 2)
            if curr_dist < closest_dist:
                closest_dist = curr_dist
                closest_node = id

        actual_node = main_generator.nodes[closest_node]
        
        if state.curr_source is None:
            state.curr_source = actual_node
            canvas.create_oval(actual_node.x-3, actual_node.y-3, actual_node.x+3, actual_node.y+3, fill="yellow")
            state.last_clicked = "curr_source"
        elif state.curr_destination is None:
            state.curr_destination = actual_node
            canvas.create_oval(actual_node.x-3, actual_node.y-3, actual_node.x+3, actual_node.y+3, fill="red")
            state.last_clicked = "curr_destination"
        else:
            if state.last_clicked == "curr_source":
                prev_node = state.curr_destination
                canvas.create_oval(prev_node.x-3, prev_node.y-3, prev_node.x+3, prev_node.y+3, fill="black")

                state.curr_destination = actual_node
                canvas.create_oval(actual_node.x-3, actual_node.y-3, actual_node.x+3, actual_node.y+3, fill="red")
                state.last_clicked = "curr_destination"
            else:
                prev_node = state.curr_source
                canvas.create_oval(prev_node.x-3, prev_node.y-3, prev_node.x+3, prev_node.y+3, fill="black")

                state.curr_source = actual_node
                canvas.create_oval(actual_node.x-3, actual_node.y-3, actual_node.x+3, actual_node.y+3, fill="yellow")
                state.last_clicked = "curr_source"
        
        


    # Create root, frame, buttons, and canvas

    root = tk.Tk()
    root.geometry("900x800")
    root.resizable(False, False)
    root.title("Pathfinding")

    top_frame = tk.Frame(root)
    top_frame.pack(side="top")

    message_box = tk.Label(top_frame, text="", fg="Black", bg="lightgray")
    button1 = tk.Button(top_frame, text="Dijkstra", command=search_1)
    button2 = tk.Button(top_frame, text="A*", command=search_2)
    buttonClear = tk.Button(top_frame, text="Clear", command=clear_board)
    buttonReset = tk.Button(top_frame, text="Reset", command=reset_board)

    button1.pack(side="left", padx=5, pady=5)
    button2.pack(side="left", padx=5, pady=5)
    buttonClear.pack(side="left", padx=5, pady=5)
    buttonReset.pack(side="left", padx=5, pady=5)
    message_box.pack(side="right", padx=5, pady=5)

    canvas = tk.Canvas(root, bg="white")
    canvas.pack(fill="both", expand=True)
    canvas.bind("<Button-1>", get_closest_node_click)
    main_generator.draw_to_canvas(canvas)
    main_generator.draw_edges(canvas)
    main_generator.generate_subset_graph()

    root.mainloop()


    

    