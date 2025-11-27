import tkinter as tk # Import tkinter library
from tkinter import messagebox # Import messagebox module
import random # Import random module
import os # Import os module
import time # Import time module
import imageio # Import imageio library
from PIL import Image, ImageTk # Import PIL library

COLOR_BG = "#000000" # Background color
COLOR_PRIMARY = "#ff0099" # Primary neon pink color
COLOR_EXIT = "#D6008D" # Exit button pink color
COLOR_TURQUOISE = "#00f2ff" # Turquoise color
COLOR_WHITE = "#ffffff" # White color
FONT_MAIN = ("Courier", 14, "bold") # Main font settings
FONT_TITLE = ("Courier", 24, "bold") # Title font settings
FONT_QUESTION = ("Courier", 20, "bold") # Question font settings

class MathQuizApp: # Define class
    def __init__(self, root): # Initialize class
        self.root = root # Set root window
        self.root.title("NEON MATH | EXERCISE 1") # Set title
        
        self.win_width = 1000 # Set window width
        self.win_height = 600 # Set window height
        self.root.geometry(f"{self.win_width}x{self.win_height}") # Apply geometry
        self.root.configure(bg=COLOR_BG) # Set background color

        self.score = 0 # Initialize score
        self.question_count = 0 # Initialize question count
        self.max_questions = 10 # Set max questions
        self.difficulty = "easy" # Set default difficulty
        self.current_answer = 0 # Initialize answer variable
        self.attempts_on_current = 0 # Initialize attempts counter
        
        self.marathon_start_time = 0 # Initialize timer start
        self.is_marathon = False # Initialize marathon flag
        self.timer_id = None # Initialize timer ID

        self.scene_canvas = tk.Canvas(root, bg="black", highlightthickness=0) # Create background canvas
        self.scene_canvas.place(relx=0, rely=0, relwidth=1, relheight=1) # Place canvas

        self.video_reader = None # Initialize video reader
        self.bg_item_id = None # Initialize bg item ID
        self.init_video_background() # Call video setup

        self.box_img_id = None # Initialize box image ID
        self.border_id = None # Initialize border ID
        self.text_ids = [] # Initialize text ID list
        self.ui_elements = [] # Initialize UI elements list

        self.show_menu() # Show menu screen

    def init_video_background(self): # Define video setup
        try: # Try block
            base_folder = os.path.dirname(os.path.abspath(__file__)) # Get base folder
            video_path = os.path.join(base_folder, "assets", "hld_mainmenu.mp4") # Build video path
            self.video_reader = imageio.get_reader(video_path) # Create video reader
            self.bg_item_id = self.scene_canvas.create_image(0, 0, anchor="nw") # Create placeholder image
            self.stream_video() # Start stream
        except Exception: # Catch errors
            self.scene_canvas.create_text(500, 300, text="VIDEO ERROR", fill="red") # Show error text

    def stream_video(self): # Define stream loop
        try: # Try block
            frame_data = self.video_reader.get_next_data() # Get next frame
            img = Image.fromarray(frame_data) # Convert to PIL image
            img = img.resize((self.win_width, self.win_height)) # Resize image
            self.current_frame_img = ImageTk.PhotoImage(img) # Convert to Tkinter image
            self.scene_canvas.itemconfig(self.bg_item_id, image=self.current_frame_img) # Update canvas
            self.root.after(33, self.stream_video) # Schedule next frame
        except IndexError: # Handle end of video
            self.video_reader.set_image_index(0) # Reset video
            self.stream_video() # Restart stream
        except: # Catch other errors
            pass # Ignore

    def draw_transparent_box(self, x, y, w, h, border_color=COLOR_PRIMARY): # Define draw box function
        alpha_img = Image.new('RGBA', (w, h), (10, 5, 15, 220)) # Create transparent image
        self.tk_alpha_img = ImageTk.PhotoImage(alpha_img) # Convert to Tkinter image
        
        if self.box_img_id: self.scene_canvas.delete(self.box_img_id) # Delete old box
        self.box_img_id = self.scene_canvas.create_image(x, y, image=self.tk_alpha_img, anchor="center") # Draw new box
        
        if self.border_id: self.scene_canvas.delete(self.border_id) # Delete old border
        self.border_id = self.scene_canvas.create_rectangle( # Draw new border
            x - w//2, y - h//2, x + w//2, y + h//2, # Coordinates
            outline=border_color, width=3 # Style
        )

    def clear_ui(self): # Define clear UI function
        for widget in self.ui_elements: # Loop widgets
            widget.destroy() # Destroy widget
        self.ui_elements = [] # Clear list
        
        for tid in self.text_ids: # Loop text IDs
            self.scene_canvas.delete(tid) # Delete text
        self.text_ids = [] # Clear list
        
        self.scene_canvas.delete("timer_tag") # Delete timer text

    def show_menu(self): # Define show menu function
        self.clear_ui() # Clear screen
        self.is_marathon = False # Reset marathon flag
        if self.timer_id: self.root.after_cancel(self.timer_id) # Cancel timer
        
        self.draw_transparent_box(500, 300, 400, 500, COLOR_PRIMARY) # Draw menu box

        tid = self.scene_canvas.create_text(500, 150, text="MATH QUIZ", font=FONT_TITLE, fill=COLOR_WHITE) # Create title
        self.text_ids.append(tid) # Store ID

        self.create_menu_btn("EASY", 0.45, "easy") # Create Easy button
        self.create_menu_btn("MEDIUM", 0.55, "medium") # Create Medium button
        self.create_menu_btn("HARD", 0.65, "hard") # Create Hard button
        self.create_menu_btn("MARATHON", 0.75, "marathon") # Create Marathon button

    def create_menu_btn(self, text, rely, mode): # Define menu button creator
        btn = tk.Button(self.root, text=text, font=FONT_MAIN, # Create button
                        bg="#0d0212", fg=COLOR_PRIMARY, bd=0, activebackground=COLOR_PRIMARY, # Style
                        command=lambda: self.start_game(mode)) # Command
        btn.place(relx=0.5, rely=rely, anchor="center") # Place button
        self.ui_elements.append(btn) # Store widget

    def start_game(self, mode): # Define start game function
        self.difficulty = mode # Set difficulty
        self.score = 0 # Reset score
        self.question_count = 0 # Reset count
        
        if mode == "marathon": # Check marathon mode
            self.is_marathon = True # Set flag
            self.max_questions = 15 # Set max questions
            self.marathon_duration = 30 # Set duration
            self.marathon_start_time = time.time() # Set start time
            self.update_timer() # Start timer
        else: # Normal mode
            self.max_questions = 10 # Set max questions
            self.is_marathon = False # Set flag
        
        self.next_question() # Start first question

    def update_timer(self): # Define timer function
        if not self.is_marathon: return # Return if not marathon
        
        elapsed = time.time() - self.marathon_start_time # Calculate elapsed
        remaining = int(self.marathon_duration - elapsed) # Calculate remaining
        
        self.scene_canvas.delete("timer_tag") # Clear old timer text
        if remaining > 0: # Check if time left
            self.scene_canvas.create_text( # Draw timer text
                900, 50, text=f"TIME: {remaining}", fill="red", # Settings
                font=FONT_TITLE, tags="timer_tag" # Tags
            )
            self.timer_id = self.root.after(1000, self.update_timer) # Schedule next update
        else: # Time over
            self.game_over() # End game

    def generate_math(self): # Define math generator
        if self.difficulty == "easy": # Easy mode
            ops = ['+', '-'] # Operations
            op = random.choice(ops) # Pick operation
            a, b = random.randint(1, 100), random.randint(1, 100) # Pick numbers
            if op == '-': a, b = max(a,b), min(a,b) # Ensure positive result
            return f"{a} {op} {b}", eval(f"{a} {op} {b}") # Return Q and A

        elif self.difficulty == "medium": # Medium mode
            ops = ['+', '-', '*', '/'] # Operations
            op = random.choice(ops) # Pick operation
            if op in ['+', '-']: # + or -
                a, b = random.randint(50, 500), random.randint(10, 200) # Pick numbers
            elif op == '*': # Multiply
                a, b = random.randint(10, 50), random.randint(2, 12) # Pick numbers
            else: # Divide
                b = random.randint(2, 20) # Divisor
                ans = random.randint(2, 50) # Answer
                a = b * ans # Calculate Dividend
            expression = f"{a} {op} {b}" # Create string
            return expression.replace('/', '÷'), int(eval(expression)) # Return formatted

        elif self.difficulty == "hard": # Hard mode
            ops = ['+', '-', '*', '/', '**'] # Operations
            op = random.choice(ops) # Pick operation
            if op == '**': # Power
                a, b = random.randint(2, 15), random.randint(2, 3) # Pick numbers
            elif op == '*': # Multiply
                a, b = random.randint(20, 100), random.randint(10, 50) # Pick numbers
            elif op == '/': # Divide
                b = random.randint(5, 50) # Divisor
                ans = random.randint(10, 100) # Answer
                a = b * ans # Dividend
            else: # + or -
                a, b = random.randint(100, 1000), random.randint(100, 1000) # Pick numbers
            expression = f"{a} {op} {b}" # Create string
            display_expr = expression.replace('**', '^').replace('/', '÷') # Format string
            return display_expr, int(eval(expression)) # Return Q and A
            
        return self.generate_math_difficulty("medium") # Fallback to medium
        
    def generate_math_difficulty(self, diff): # Define helper
        temp = self.difficulty # Save current
        self.difficulty = diff # Switch difficulty
        q, a = self.generate_math() # Generate
        self.difficulty = temp # Restore difficulty
        return q, a # Return result

    def next_question(self): # Define next question function
        if self.question_count >= self.max_questions: # Check limit
            self.game_over() # End game
            return # Exit

        self.clear_ui() # Clear screen
        self.question_count += 1 # Increment count
        self.attempts_on_current = 0 # Reset attempts
        
        q_text, ans = self.generate_math() # Generate Q and A
        self.current_answer = ans # Store answer

        self.draw_transparent_box(500, 300, 800, 350, COLOR_PRIMARY) # Draw game box

        mode_str = f"/// {self.difficulty.upper()} MODE ///" # Create mode string
        tid_mode = self.scene_canvas.create_text( # Draw mode text
            500, 180, text=mode_str, font=("Courier", 16, "bold"), fill=COLOR_TURQUOISE
        )
        self.text_ids.append(tid_mode) # Store ID

        tid_q = self.scene_canvas.create_text( # Draw question text
            500, 250, text=f"{q_text} = ?", font=FONT_QUESTION, fill=COLOR_WHITE
        )
        self.text_ids.append(tid_q) # Store ID

        self.entry_ans = tk.Entry(self.root, font=("Courier", 20), justify='center', bg="#222", fg=COLOR_TURQUOISE, insertbackground=COLOR_PRIMARY) # Create entry
        self.entry_ans.place(relx=0.5, rely=0.55, anchor="center", width=200) # Place entry
        self.entry_ans.focus_set() # Focus entry
        self.entry_ans.bind('<Return>', self.check_answer) # Bind Enter key
        self.ui_elements.append(self.entry_ans) # Store widget

        btn_submit = tk.Button(self.root, text="SUBMIT", font=FONT_MAIN, # Create submit button
                               bg="#0d0212", fg=COLOR_PRIMARY, command=lambda: self.check_answer(None)) # Command
        btn_submit.place(relx=0.5, rely=0.68, anchor="center") # Place button
        self.ui_elements.append(btn_submit) # Store widget

        btn_exit = tk.Button(self.root, text="QUIT", font=("Courier", 12, "bold"), # Create quit button
                             bg=COLOR_EXIT, fg=COLOR_WHITE, bd=0, 
                             activebackground="#a3006b", command=self.show_menu) # Command
        btn_exit.place(relx=0.25, rely=0.72, anchor="center") # Place button
        self.ui_elements.append(btn_exit) # Store widget

        progress_str = f"{self.question_count}/{self.max_questions}" # Create progress string
        tid_prog = self.scene_canvas.create_text( # Draw progress text
            320, 432, text=progress_str, font=("Courier", 14, "bold"), fill=COLOR_WHITE
        )
        self.text_ids.append(tid_prog) # Store ID

    def check_answer(self, event): # Define check answer function
        user_input = self.entry_ans.get() # Get input
        try: # Try block
            val = int(user_input) # Convert to int
        except ValueError: # Catch invalid input
             messagebox.showwarning("System", "Please enter a valid number.") # Show warning
             return # Return

        if val == self.current_answer: # Check correct
            if self.attempts_on_current == 0: # Check first try
                points = 10 # 10 points
            else: # Second try
                points = 5 # 5 points
            
            self.score += points # Add score
            messagebox.showinfo("Result", f"CORRECT! [ +{points} POINTS ]") # Show success
            self.next_question() # Next question
            
        else: # Incorrect
            self.attempts_on_current += 1 # Increment attempts
            
            if self.attempts_on_current < 2: # Check attempts left
                messagebox.showwarning("Result", "WRONG. Try Again for 5 points.") # Show warning
                self.entry_ans.delete(0, 'end') # Clear input
            else: # No attempts left
                messagebox.showerror("Result", f"WRONG AGAIN. The answer was {self.current_answer}.") # Show error
                self.next_question() # Next question

    def game_over(self): # Define game over function
        if self.timer_id: self.root.after_cancel(self.timer_id) # Cancel timer
        
        self.clear_ui() # Clear screen
        self.draw_transparent_box(500, 300, 600, 400, COLOR_TURQUOISE) # Draw result box
        
        tid_over = self.scene_canvas.create_text(500, 200, text="SESSION COMPLETE", font=FONT_TITLE, fill=COLOR_TURQUOISE) # Draw title
        self.text_ids.append(tid_over) # Store ID

        grade = "F" # Default grade
        if self.score >= 90: grade = "A+" # Check A+
        elif self.score >= 80: grade = "A" # Check A
        elif self.score >= 70: grade = "B" # Check B
        elif self.score >= 60: grade = "C" # Check C

        tid_score = self.scene_canvas.create_text(500, 300, text=f"SCORE: {self.score}\nRANK: {grade}", font=("Courier", 30, "bold"), fill=COLOR_WHITE, justify="center") # Draw score
        self.text_ids.append(tid_score) # Store ID

        btn_menu = tk.Button(self.root, text="RETURN TO MENU", font=FONT_MAIN, # Create menu button
                             bg="#0d0212", fg=COLOR_PRIMARY, command=self.show_menu) # Command
        btn_menu.place(relx=0.5, rely=0.75, anchor="center") # Place button
        self.ui_elements.append(btn_menu) # Store widget

if __name__ == "__main__": # Main entry check
    root = tk.Tk() # Create root window
    app = MathQuizApp(root) # Create app instance
    root.mainloop() # Start main loop