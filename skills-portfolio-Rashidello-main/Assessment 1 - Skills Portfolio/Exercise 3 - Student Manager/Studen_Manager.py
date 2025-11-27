import tkinter as tk # Import tkinter library
from tkinter import messagebox, simpledialog # Import specific modules
import os # Import os module
from PIL import Image, ImageTk # Import PIL library

COLOR_BG = "#000000" # Background color
COLOR_PRIMARY = "#D6008D" # Primary neon pink color
COLOR_TURQUOISE = "#00f2ff" # Turquoise color
COLOR_WHITE = "#ffffff" # White color

class StudentManager: # Define class
    def __init__(self, root): # Initialize class
        self.root = root # Set root window
        self.root.title("STUDENT DATA TERMINAL | EXERCISE 3") # Set window title
        
        self.win_width = 1000 # Set window width
        self.win_height = 600 # Set window height
        self.root.geometry(f"{self.win_width}x{self.win_height}") # Apply geometry
        self.root.configure(bg=COLOR_BG) # Set background color

        self.students = [] # Initialize empty student list
        self.load_data() # Load data from file

        self.scene_canvas = tk.Canvas(root, bg="black", highlightthickness=0) # Create background canvas
        self.scene_canvas.place(relx=0, rely=0, relwidth=1, relheight=1) # Place canvas

        try: # Try block for image loading
            base_folder = os.path.dirname(os.path.abspath(__file__)) # Get base folder
            image_path = os.path.join(base_folder, "assets", "hld_again.png") # Build image path
            
            pil_image = Image.open(image_path) # Open image
            pil_image = pil_image.resize((self.win_width, self.win_height)) # Resize image
            
            self.bg_img = ImageTk.PhotoImage(pil_image) # Convert to Tkinter image
            self.scene_canvas.create_image(0, 0, image=self.bg_img, anchor="nw") # Draw image on canvas
        except Exception as e: # Catch errors
            print(f"BG Error: {e}") # Print error
            self.scene_canvas.create_text(500, 300, text="BG NOT FOUND", fill="red") # Show error text

        ROW_1_Y = 0.105 # Set Row 1 Y position
        ROW_2_Y = 0.245 # Set Row 2 Y position

        COL_1_X = 0.125 # Set Column 1 X position
        COL_2_X = 0.375 # Set Column 2 X position
        COL_3_X = 0.625 # Set Column 3 X position
        COL_4_X = 0.855 # Set Column 4 X position

        self.create_nav_btn("VIEW ALL",    COL_1_X, ROW_1_Y, self.view_all) # Create View All button
        self.create_nav_btn("VIEW RECORD", COL_2_X, ROW_1_Y, self.view_individual) # Create View Record button
        self.create_nav_btn("HIGH SCORE",  COL_3_X, ROW_1_Y, self.show_highest) # Create High Score button
        self.create_nav_btn("LOW SCORE",   COL_4_X, ROW_1_Y, self.show_lowest) # Create Low Score button

        self.create_nav_btn("SORT LIST",   COL_1_X, ROW_2_Y, self.sort_records) # Create Sort List button
        self.create_nav_btn("ADD NEW",     COL_2_X, ROW_2_Y, self.add_student) # Create Add New button
        self.create_nav_btn("DELETE",      COL_3_X, ROW_2_Y, self.delete_student) # Create Delete button
        self.create_nav_btn("UPDATE",      COL_4_X, ROW_2_Y, self.update_student) # Create Update button

        self.terminal_frame = tk.Frame(root, bg=COLOR_BG, highlightbackground=COLOR_TURQUOISE, highlightthickness=2) # Create terminal frame
        self.terminal_frame.place(relx=0.5, rely=0.68, anchor="center", relwidth=0.9, relheight=0.55) # Place terminal frame

        self.output_text = tk.Text( # Create text widget
            self.terminal_frame, # Parent is terminal frame
            bg=COLOR_BG, # Background color
            fg=COLOR_TURQUOISE, # Text color
            font=("Courier", 11), # Font settings
            bd=0, # No border
            padx=20, pady=20 # Padding
        )
        self.output_text.pack(fill="both", expand=True) # Pack text widget
        
        self.log("Hello :D") # Log initial message

    def create_nav_btn(self, text, relx, rely, command): # Define button creation function
        btn = tk.Button( # Create button widget
            self.root, # Parent is root
            text=text, # Set button text
            command=command, # Set click command
            bg=COLOR_BG, # Background color
            fg=COLOR_WHITE, # Text color
            activebackground=COLOR_BG, # Active bg color
            activeforeground=COLOR_PRIMARY, # Active text color
            font=("Courier", 11, "bold"), # Font settings
            bd=0, # No border
            cursor="hand2" # Hand cursor
        )
        btn.place(relx=relx, rely=rely, anchor="center") # Place button

    def load_data(self): # Define load data function
        self.students = [] # Clear students list
        try: # Try block
            base_folder = os.path.dirname(os.path.abspath(__file__)) # Get base folder
            file_path = os.path.join(base_folder, "studentMarks.txt") # Build file path
            
            with open(file_path, "r") as f: # Open file read mode
                lines = f.readlines() # Read all lines
                for line in lines[1:]: # Loop through lines skipping first
                    parts = line.strip().split(',') # Split line by comma
                    if len(parts) >= 6: # Check if valid line
                        s_id = parts[0] # Get ID
                        name = parts[1] # Get Name
                        c1, c2, c3 = int(parts[2]), int(parts[3]), int(parts[4]) # Get coursework marks
                        exam = int(parts[5]) # Get exam mark
                        
                        total_coursework = c1 + c2 + c3 # Calculate total coursework
                        total_score = total_coursework + exam # Calculate total score
                        percentage = (total_score / 160) * 100 # Calculate percentage
                        grade = self.calculate_grade(percentage) # Calculate grade
                        
                        self.students.append({ # Add student dict to list
                            "id": s_id, "name": name, # Store ID and Name
                            "c_total": total_coursework, "exam": exam, # Store scores
                            "total": total_score, "percent": percentage, # Store totals
                            "grade": grade, "raw_parts": parts # Store grade and raw parts
                        })
        except Exception as e: # Catch errors
            messagebox.showerror("Error", f"Failed to load data: {e}") # Show error message

    def calculate_grade(self, percent): # Define grade calculation
        if percent >= 70: return 'A' # Check for A
        elif percent >= 60: return 'B' # Check for B
        elif percent >= 50: return 'C' # Check for C
        elif percent >= 40: return 'D' # Check for D
        else: return 'F' # Else F

    def log(self, message): # Define log function
        self.output_text.delete("1.0", tk.END) # Clear text box
        self.output_text.insert("1.0", message) # Insert message

    def format_student(self, s): # Define format string function
        return (f"ID: {s['id']} | NAME: {s['name']}\n" # Format line 1
                f"   Coursework: {s['c_total']}/60 | Exam: {s['exam']}/100\n" # Format line 2
                f"   TOTAL: {s['total']}/160 ({s['percent']:.1f}%) -> GRADE: {s['grade']}\n" # Format line 3
                f"{'-'*60}\n") # Format separator

    def view_all(self): # Define view all function
        report = "--- CLASS REPORT ---\n\n" # Initialize report string
        total_percent = 0 # Initialize total percent
        for s in self.students: # Loop through students
            report += self.format_student(s) # Add formatted student
            total_percent += s['percent'] # Add to total percent
        
        avg = total_percent / len(self.students) if self.students else 0 # Calculate average
        report += f"\nCLASS SUMMARY:\nStudents: {len(self.students)}\nAverage Score: {avg:.1f}%" # Add summary
        self.log(report) # Log report

    def view_individual(self): # Define view individual function
        target_id = simpledialog.askstring("Input", "Enter Student ID:") # Ask for ID
        if target_id: # If ID provided
            for s in self.students: # Loop through students
                if s['id'] == target_id: # Check ID match
                    self.log(self.format_student(s)) # Log formatted student
                    return # Exit function
            self.log(f"Student ID {target_id} not found.") # Log not found

    def show_highest(self): # Define show highest function
        if not self.students: return # Return if no students
        top = max(self.students, key=lambda x: x['total']) # Find max total
        self.log("--- HIGHEST PERFORMING STUDENT ---\n\n" + self.format_student(top)) # Log result

    def show_lowest(self): # Define show lowest function
        if not self.students: return # Return if no students
        low = min(self.students, key=lambda x: x['total']) # Find min total
        self.log("--- LOWEST PERFORMING STUDENT ---\n\n" + self.format_student(low)) # Log result

    def sort_records(self): # Define sort function
        choice = simpledialog.askstring("Sort", "Type 'A' for Ascending or 'D' for Descending:") # Ask sort order
        if choice and choice.upper() == 'A': # If Ascending
            self.students.sort(key=lambda x: x['total'])  # Sort list
            self.log("Sorted: Ascending Order") # Log status
        else: # If Descending
            self.students.sort(key=lambda x: x['total'], reverse=True) # Sort reverse
            self.log("Sorted: Descending Order (Highest First)") # Log status
        self.view_all() # View all records

    def add_student(self): # Define add student function
        data = simpledialog.askstring("Add", "Format: ID,Name,C1,C2,C3,Exam\nExample: 5555,New Guy,15,15,15,80") # Ask for data
        if data: # If data provided
            try: # Try block
                if data.count(',') != 5: # Validate format
                    self.log("Error: Invalid format. Please use commas.") # Log error
                    return # Return
                with open("studentMarks.txt", "a") as f: # Open file append mode
                    f.write("\n" + data) # Write data
                self.load_data() # Reload data
                self.log("Student added successfully.") # Log success
            except: # Catch errors
                self.log("Error saving to file.") # Log error

    def delete_student(self): # Define delete student function
        target_id = simpledialog.askstring("Delete", "Enter ID to delete:") # Ask for ID
        if target_id: # If ID provided
            found = False # Initialize found flag
            new_list = [] # Initialize new list
            for s in self.students: # Loop through students
                if s['id'] == target_id: # Check ID match
                    found = True # Set found true
                else: # Else
                    new_list.append(s) # Add to new list
            if found: # If found
                self.students = new_list # Update students list
                self.save_all_to_file() # Save to file
                self.log(f"Student {target_id} deleted.") # Log success
            else: # Else
                self.log("Student ID not found.") # Log not found

    def update_student(self): # Define update student function
        target_id = simpledialog.askstring("Update", "Enter ID to update:") # Ask for ID
        if target_id: # If ID provided
            target_student = None # Initialize target
            for s in self.students: # Loop through students
                if s['id'] == target_id: # Check ID match
                    target_student = s # Set target
                    break # Break loop
            
            if not target_student: # If not found
                self.log("ID not found.") # Log error
                return # Return

            self.log(f"Updating {target_student['name']}...") # Log updating
            new_data = simpledialog.askstring("Update", f"Enter NEW data for {target_id}:\nFormat: ID,Name,C1,C2,C3,Exam") # Ask new data
            
            if new_data: # If new data provided
                self.students = [s for s in self.students if s['id'] != target_id] # Remove old student
                self.save_all_to_file() # Save to file
                with open("studentMarks.txt", "a") as f: # Open file append mode
                    f.write("\n" + new_data) # Write new data
                self.load_data() # Reload data
                self.log("Student record updated.") # Log success

    def save_all_to_file(self): # Define save function
        try: # Try block
            with open("studentMarks.txt", "w") as f: # Open file write mode
                f.write(str(len(self.students)) + "\n") # Write count
                for s in self.students: # Loop through students
                    line = ",".join(s['raw_parts']) # Join raw parts
                    f.write(line + "\n") # Write line
        except Exception as e: # Catch errors
            print(f"Save Error: {e}") # Print error

if __name__ == "__main__": # Main entry check
    root = tk.Tk() # Create root window
    app = StudentManager(root) # Create app instance
    root.mainloop() # Start main loop