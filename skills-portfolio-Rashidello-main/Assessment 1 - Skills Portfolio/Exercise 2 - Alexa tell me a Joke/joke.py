import tkinter as tk # Import tkinter library
import random # Import random library
import os # Import os library
import imageio # Import imageio library
from PIL import Image, ImageTk # Import PIL library

COLOR_BG = "#000000" # Background color
COLOR_PRIMARY = "#D6008D" # Primary neon pink color
COLOR_TURQUOISE = "#00f2ff" # Turquoise color

class TextButton(tk.Button): # Define custom button class
    def __init__(self, master, **kw): # Initialize button
        tk.Button.__init__(self, master=master, **kw) # Initialize parent class
        self.configure( # Configure button style
            bg=COLOR_BG, # Background color
            fg=COLOR_PRIMARY, # Text color
            font=("Courier", 12, "bold"), # Font settings
            bd=0, # No border
            activebackground=COLOR_BG, # Active bg color
            activeforeground=COLOR_TURQUOISE, # Active text color
            cursor="hand2", # Hand cursor
            justify="center" # Center text
        )
        self.bind("<Enter>", self.on_enter) # Bind hover enter
        self.bind("<Leave>", self.on_leave) # Bind hover leave

    def on_enter(self, e): # Define enter handler
        self.configure(fg=COLOR_TURQUOISE) # Change color on hover

    def on_leave(self, e): # Define leave handler
        self.configure(fg=COLOR_PRIMARY) # Revert color

class JokeApp: # Define main app class
    def __init__(self, root): # Initialize app
        self.root = root # Set root window
        self.root.title("NPC DIALOGUE | EXERCISE 2") # Set title
        
        self.win_width = 1000 # Set window width
        self.win_height = 600 # Set window height
        self.root.geometry(f"{self.win_width}x{self.win_height}") # Apply geometry
        self.root.configure(bg=COLOR_BG) # Configure background

        self.jokes_list = [] # Initialize jokes list
        self.load_jokes() # Load jokes from file
        self.current_joke_index = 0 # Set current index
        self.current_state = "IDLE" # Set initial state

        self.scene_canvas = tk.Canvas(root, bg="black", highlightthickness=0) # Create background canvas
        self.scene_canvas.place(relx=0, rely=0, relwidth=1, relheight=1) # Place canvas

        self.video_reader = None # Initialize video reader
        self.bg_item_id = None # Initialize bg item id
        
        try: # Try block for video loading
            base_folder = os.path.dirname(os.path.abspath(__file__)) # Get base folder
            video_path = os.path.join(base_folder, "assets", "hld.mp4") # Build video path
            
            self.video_reader = imageio.get_reader(video_path) # Create video reader
            
            self.bg_item_id = self.scene_canvas.create_image(0, 0, anchor="nw") # Create placeholder image
            
            self.stream_video() # Start video stream
            
        except Exception: # Catch errors
            self.scene_canvas.create_text( # Create error text
                self.win_width//2, self.win_height//2, # Center coordinates
                text="VIDEO LOAD ERROR", # Error message
                fill="red" # Red color
            )

        box_w, box_h = 600, 240 # Set box dimensions
        self.transparent_box_img = Image.new('RGBA', (box_w, box_h), (0, 0, 0, 200)) # Create transparent image
        self.tk_box_img = ImageTk.PhotoImage(self.transparent_box_img) # Convert to Tkinter image

        self.box_item_id = None # Initialize box ID
        self.border_item_id = None # Initialize border ID
        self.text_item_id = None # Initialize text ID

        self.button_frame = tk.Frame(root, bg=COLOR_BG) # Create button frame
        self.button_frame.place(relx=0.5, rely=0.88, anchor="n", relwidth=0.7, relheight=0.1) # Place frame

        self.btn_exit = TextButton(self.button_frame, text="EXIT", command=self.root.destroy) # Create Exit button
        self.btn_exit.pack(side="left", expand=True, fill="x") # Pack Exit button

        self.btn_prev = TextButton(self.button_frame, text="PREV", command=self.prev_joke) # Create Prev button
        self.btn_prev.pack(side="left", expand=True, fill="x") # Pack Prev button

        self.btn_continue = TextButton(self.button_frame, text="INTERACT", command=self.handle_continue) # Create Interact button
        self.btn_continue.pack(side="left", expand=True, fill="x") # Pack Interact button

        self.btn_next = TextButton(self.button_frame, text="NEXT", command=self.next_joke) # Create Next button
        self.btn_next.pack(side="left", expand=True, fill="x") # Pack Next button

    def stream_video(self): # Define video stream function
        try: # Try block
            frame_data = self.video_reader.get_next_data() # Get next frame
            img = Image.fromarray(frame_data) # Convert to PIL image
            img = img.resize((self.win_width, self.win_height)) # Resize image
            self.current_frame_img = ImageTk.PhotoImage(img) # Convert to Tkinter image
            self.scene_canvas.itemconfig(self.bg_item_id, image=self.current_frame_img) # Update canvas image
            self.root.after(33, self.stream_video) # Schedule next frame
            
        except IndexError: # Handle end of video
            self.video_reader.set_image_index(0) # Reset video
            self.stream_video() # Restart stream
            
        except Exception: # Catch other errors
            pass # Ignore

    def load_jokes(self): # Define load jokes function
        try: # Try block
            base_folder = os.path.dirname(os.path.abspath(__file__)) # Get base folder
            file_path = os.path.join(base_folder, "randomJokes.txt") # Build file path
            with open(file_path, "r") as f: # Open file
                lines = f.readlines() # Read lines
                for line in lines: # Loop through lines
                    if "?" in line: # Check format
                        parts = line.strip().split("?") # Split by question mark
                        setup = parts[0] + "?" # Get setup
                        punchline = parts[1] if len(parts) > 1 else "" # Get punchline
                        self.jokes_list.append({"setup": setup, "punchline": punchline}) # Add to list
        except: # Catch errors
            pass # Ignore

    def draw_chat_box(self, text_content): # Define draw chat box function
        center_x = self.win_width // 2 # Calculate center X
        center_y = self.win_height // 3 # Calculate center Y

        if self.box_item_id is None: # Check if box exists
            self.box_item_id = self.scene_canvas.create_image( # Create box image
                center_x, center_y, # Coordinates
                image=self.tk_box_img, # Image source
                anchor="center" # Anchor point
            )
        
        x1 = center_x - 300 # Calculate x1
        y1 = center_y - 120 # Calculate y1
        x2 = center_x + 300 # Calculate x2
        y2 = center_y + 120 # Calculate y2
        
        if self.border_item_id is None: # Check if border exists
            self.border_item_id = self.scene_canvas.create_rectangle( # Create border
                x1, y1, x2, y2, # Coordinates
                outline=COLOR_TURQUOISE, # Outline color
                width=3 # Border width
            )

        if self.text_item_id is None: # Check if text exists
            self.text_item_id = self.scene_canvas.create_text( # Create text
                center_x, center_y, # Coordinates
                text=text_content, # Content
                fill=COLOR_PRIMARY, # Text color
                font=("Courier", 15, "bold"), # Font settings
                width=500, # Wrap width
                justify="center" # Justify center
            )
        else: # If exists
            self.scene_canvas.itemconfig(self.text_item_id, text=text_content) # Update text content
        
        self.scene_canvas.tag_raise(self.box_item_id) # Raise box layer
        self.scene_canvas.tag_raise(self.border_item_id) # Raise border layer
        self.scene_canvas.tag_raise(self.text_item_id) # Raise text layer

    def handle_continue(self): # Define continue handler
        if self.current_state == "IDLE": # Check if idle
            self.show_setup() # Show setup
        elif self.current_state == "SETUP": # Check if setup
            self.show_punchline() # Show punchline
        elif self.current_state == "PUNCHLINE": # Check if punchline
            self.next_joke() # Show next joke

    def show_setup(self): # Define show setup function
        if not self.jokes_list: return # Return if no jokes
        joke = self.jokes_list[self.current_joke_index] # Get current joke
        self.draw_chat_box(joke['setup']) # Draw setup text
        self.current_state = "SETUP" # Update state
        self.btn_continue.config(text="PUNCHLINE") # Update button text

    def show_punchline(self): # Define show punchline function
        if not self.jokes_list: return # Return if no jokes
        joke = self.jokes_list[self.current_joke_index] # Get current joke
        full_text = f"{joke['setup']}\n\n{joke['punchline']}" # Create full text
        self.draw_chat_box(full_text) # Draw full text
        self.current_state = "PUNCHLINE" # Update state
        self.btn_continue.config(text="NEXT JOKE") # Update button text

    def next_joke(self): # Define next joke function
        self.current_joke_index = random.randint(0, len(self.jokes_list) - 1) # Pick random index
        self.show_setup() # Show setup

    def prev_joke(self): # Define prev joke function
        self.current_joke_index = (self.current_joke_index - 1) % len(self.jokes_list) # Decrement index
        self.show_setup() # Show setup

if __name__ == "__main__": # Main entry check
    root = tk.Tk() # Create root window
    app = JokeApp(root) # Create app instance
    root.mainloop() # Start main loop