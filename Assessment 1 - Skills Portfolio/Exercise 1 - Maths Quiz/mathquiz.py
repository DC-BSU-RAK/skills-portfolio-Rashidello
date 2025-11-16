import tkinter as tk
from tkinter import font as tkfont
import random
import json
import os

EASY_QUESTIONS = []
MEDIUM_QUESTIONS = []
HARD_QUESTIONS = []
ALL_QUESTIONS = []
QUIZ_DATA_BY_DIFFICULTY = {}

score = 0
current_question_index = 0
quiz_data = []
quiz_mode = "standard"

feedback_label = None
next_button = None
option_buttons = []
score_label = None
main_menu_button = None

app = tk.Tk()
app.title("Simple Math Quiz")
app.geometry("500x450")
app.resizable(False, False)
app.configure(bg="#f0f0f0")

TITLE_FONT = ("Helvetica", 20, "bold")
QUESTION_FONT = ("Helvetica", 16)
BUTTON_FONT = ("Helvetica", 12, "bold")
FEEDBACK_FONT = ("Helvetica", 12, "bold")
SCORE_FONT = ("Helvetica", 28, "bold")
SMALL_FONT = ("Helvetica", 10)

content_frame = tk.Frame(app, bg="#f0f0f0")
content_frame.pack(fill="both", expand=True)

def clear_frame():
    for widget in content_frame.winfo_children():
        widget.destroy()

def show_error_screen(message):
    clear_frame()
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_rowconfigure(2, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    
    error_label = tk.Label(content_frame, 
                           text=message,
                           font=QUESTION_FONT,
                           fg="red",
                           bg="#f0f0f0",
                           wraplength=450)
    error_label.grid(row=0, column=0, pady=20)
    
    quit_button = tk.Button(content_frame, text="Quit", 
                            font=SMALL_FONT,
                            command=app.quit,
                            bg="#6c757d", fg="white", width=10)
    quit_button.grid(row=1, column=0, pady=20)


def load_questions_from_file():
    global EASY_QUESTIONS, MEDIUM_QUESTIONS, HARD_QUESTIONS, ALL_QUESTIONS, QUIZ_DATA_BY_DIFFICULTY
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "questions.json")

        with open(json_path, "r") as f:
            data = json.load(f)
            
        EASY_QUESTIONS = data.get("easy", [])
        MEDIUM_QUESTIONS = data.get("medium", [])
        HARD_QUESTIONS = data.get("hard", [])
        
        if not EASY_QUESTIONS and not MEDIUM_QUESTIONS and not HARD_QUESTIONS:
            return False, "Error: questions.json is empty or has wrong format."
            
        ALL_QUESTIONS = EASY_QUESTIONS + MEDIUM_QUESTIONS + HARD_QUESTIONS
        
        QUIZ_DATA_BY_DIFFICULTY = {
            "easy": EASY_QUESTIONS,
            "medium": MEDIUM_QUESTIONS,
            "hard": HARD_QUESTIONS,
            "marathon": ALL_QUESTIONS
        }
        return True, ""
        
    except FileNotFoundError:
        return False, f"Error: questions.json file not found.\nI looked for it here:\n{json_path}\nMake sure it's in the same folder as the .py file."
    except json.JSONDecodeError:
        return False, "Error: Could not read questions.json.\nCheck for syntax errors (e.g., missing comma)."
    except Exception as e:
        return False, f"An unexpected error occurred: {e}"


def show_welcome_screen():
    clear_frame()
    
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_rowconfigure(5, weight=1)
    content_frame.grid_rowconfigure(6, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)

    title_label = tk.Label(content_frame, text="Welcome to the Simple Math Quiz!", 
                           font=TITLE_FONT, pady=10, bg="#f0f0f0")
    title_label.grid(row=1, column=0, pady=(20, 10))

    subtitle_label = tk.Label(content_frame, text="Select your mode:", 
                              font=QUESTION_FONT, pady=10, bg="#f0f0f0")
    subtitle_label.grid(row=2, column=0, pady=(0, 20))

    mode_frame = tk.Frame(content_frame, bg="#f0f0f0")
    mode_frame.grid(row=3, column=0)
    
    easy_button = tk.Button(mode_frame, text="Easy", 
                            font=BUTTON_FONT, 
                            command=lambda: start_quiz("easy"),
                            bg="#28a745", fg="white", width=12, height=2,
                            relief="raised", borderwidth=2,
                            activebackground="#218838", activeforeground="white")
    easy_button.grid(row=0, column=0, padx=5, pady=5)
    
    medium_button = tk.Button(mode_frame, text="Medium", 
                              font=BUTTON_FONT, 
                              command=lambda: start_quiz("medium"),
                              bg="#ffc107", fg="black", width=12, height=2,
                              relief="raised", borderwidth=2,
                              activebackground="#e0a800", activeforeground="black")
    medium_button.grid(row=0, column=1, padx=5, pady=5)
    
    hard_button = tk.Button(mode_frame, text="Hard", 
                            font=BUTTON_FONT, 
                            command=lambda: start_quiz("hard"),
                            bg="#dc3545", fg="white", width=12, height=2,
                            relief="raised", borderwidth=2,
                            activebackground="#c82333", activeforeground="white")
    hard_button.grid(row=0, column=2, padx=5, pady=5)
    
    marathon_button = tk.Button(content_frame, text="Marathon", 
                                font=BUTTON_FONT, 
                                command=lambda: start_quiz("marathon"),
                                bg="#007bff", fg="white", width=20, height=2,
                                relief="raised", borderwidth=2,
                                activebackground="#0069d9", activeforeground="white")
    marathon_button.grid(row=4, column=0, pady=15)
    
    quit_button = tk.Button(content_frame, text="Quit", 
                            font=SMALL_FONT,
                            command=app.quit,
                            bg="#6c757d", fg="white", width=10,
                            relief="raised", borderwidth=2,
                            activebackground="#5a6268", activeforeground="white")
    quit_button.grid(row=5, column=0, pady=10, sticky="s")

def start_quiz(mode):
    global quiz_mode, score, current_question_index, quiz_data
    
    quiz_mode = mode
    score = 0
    current_question_index = 0
    
    questions_list = QUIZ_DATA_BY_DIFFICULTY.get(mode, MEDIUM_QUESTIONS)
    quiz_data = list(questions_list)
    random.shuffle(quiz_data)
    
    show_quiz_screen()

def show_quiz_screen():
    global feedback_label, next_button, option_buttons, score_label, main_menu_button
    
    clear_frame()
    
    content_frame.grid_rowconfigure(0, weight=0)
    content_frame.grid_rowconfigure(1, weight=0)
    content_frame.grid_rowconfigure(2, weight=0)
    content_frame.grid_rowconfigure(3, weight=0)
    content_frame.grid_rowconfigure(4, weight=0)
    content_frame.grid_rowconfigure(5, weight=0)
    content_frame.grid_rowconfigure(6, weight=0)
    
    question_data = quiz_data[current_question_index]
    question_num = current_question_index + 1
    
    status_frame = tk.Frame(content_frame, pady=10, bg="#f0f0f0")
    status_frame.pack(fill="x", padx=20)
    
    if quiz_mode == "marathon":
        tracker_text = f"Question: {question_num}"
    else:
        total_questions = len(quiz_data)
        tracker_text = f"Question: {question_num} / {total_questions}"
        
    question_tracker_label = tk.Label(status_frame, text=tracker_text, 
                                           font=SMALL_FONT, bg="#f0f0f0")
    question_tracker_label.pack(side="left")
    
    score_label = tk.Label(status_frame, text=f"Score: {score}", 
                                font=SMALL_FONT, bg="#f0f0f0")
    score_label.pack(side="right")

    question_label = tk.Label(content_frame, text=question_data["question"], 
                                    font=QUESTION_FONT, wraplength=450,
                                    pady=20, bg="#f0f0f0")
    question_label.pack(pady=10)

    options_frame = tk.Frame(content_frame, bg="#f0f0f0")
    options_frame.pack(pady=10)
    
    option_buttons = []
    btn_grid_frame = tk.Frame(options_frame, bg="#f0f0f0")
    btn_grid_frame.pack()
    
    options = question_data["options"]
    for i in range(4):
        button = tk.Button(btn_grid_frame, text=options[i], 
                           font=BUTTON_FONT, width=18, height=2,
                           relief="raised", borderwidth=2, bg="#ffffff",
                           activebackground="#e2e6ea",
                           command=lambda opt=options[i]: check_answer(opt))
        
        row = i // 2
        col = i % 2
        button.grid(row=row, column=col, pady=5, padx=5)
        option_buttons.append(button)

    feedback_label = tk.Label(content_frame, text="", 
                                    font=FEEDBACK_FONT, pady=10, bg="#f0f0f0")
    feedback_label.pack(pady=5)

    navigation_frame = tk.Frame(content_frame, bg="#f0f0f0")
    navigation_frame.pack(pady=20)

    main_menu_button = tk.Button(navigation_frame, text="Main Menu",
                                  font=SMALL_FONT,
                                  command=show_welcome_screen,
                                  width=12, height=2,
                                  relief="raised", borderwidth=2,
                                  bg="#6c757d", fg="white",
                                  activebackground="#5a6268")
    main_menu_button.pack(side="left", padx=10)

    next_button = tk.Button(navigation_frame, text="Next Question", 
                                 font=BUTTON_FONT,
                                 command=next_question,
                                 state="disabled", width=15, height=2,
                                 relief="raised", borderwidth=2,
                                 bg="#007bff", fg="white",
                                 activebackground="#0069d9")
    next_button.pack(side="right", padx=10)

def check_answer(selected_option):
    global score, feedback_label, next_button, option_buttons, score_label
    
    question_data = quiz_data[current_question_index]
    correct_answer = question_data["answer"]
    
    if selected_option == correct_answer:
        score += 1
        feedback_label.config(text="Correct!", fg="#28a745")
        for button in option_buttons:
            button.config(state="disabled")
        next_button.config(state="normal")
        
    else:
        if quiz_mode == "marathon":
            game_over(correct_answer)
        else:
            feedback_label.config(text=f"Incorrect! The answer was {correct_answer}", fg="#dc3545")
            for button in option_buttons:
                button.config(state="disabled")
            next_button.config(state="normal")

    score_label.config(text=f"Score: {score}")

def game_over(correct_answer):
    global feedback_label, next_button, option_buttons, main_menu_button
    
    feedback_label.config(text=f"Game Over! The answer was {correct_answer}", fg="#dc3545")
    
    for button in option_buttons:
        button.config(state="disabled")
    next_button.config(state="disabled")
    main_menu_button.config(state="disabled")
    
    app.after(2000, show_results)

def next_question():
    global current_question_index
    
    current_question_index += 1
    if current_question_index < len(quiz_data):
        show_quiz_screen()
    else:
        show_results()

def show_results():
    clear_frame()
    
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_rowconfigure(6, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    
    final_title = "Quiz Complete!"
    final_comment = ""
    score_text = ""
    
    if quiz_mode == "marathon":
        final_title = "Marathon Complete!"
        score_text = f"Score: {score}"
        final_comment = f"You survived {score} rounds!"
    else:
        total_questions = len(quiz_data)
        
        try:
            percentage = (score / total_questions) * 100
        except ZeroDivisionError:
            percentage = 0
        
        score_text = f"{score} / {total_questions}"
        
        if percentage == 100:
            final_comment = "Perfect! Great job!"
        elif percentage >= 75:
            final_comment = "Great job!"
        elif percentage >= 50:
            final_comment = "Good try!"
        else:
            final_comment = "Keep practicing!"

    title_label = tk.Label(content_frame, text=final_title, 
                           font=TITLE_FONT, pady=10, bg="#f0f0f0")
    title_label.grid(row=1, column=0, pady=20)
    
    score_summary_label = tk.Label(content_frame, text="You scored:", 
                                   font=QUESTION_FONT, bg="#f0f0f0")
    score_summary_label.grid(row=2, column=0, pady=5)
    
    final_score_label = tk.Label(content_frame, text=score_text, 
                                      font=SCORE_FONT, bg="#f0f0f0")
    final_score_label.grid(row=3, column=0, pady=10)
    
    comment_label = tk.Label(content_frame, text=final_comment, 
                                  font=QUESTION_FONT, bg="#f0f0f0")
    comment_label.grid(row=4, column=0, pady=10)
    
    buttons_frame = tk.Frame(content_frame, bg="#f0f0f0")
    buttons_frame.grid(row=5, column=0, pady=30)

    play_again_button = tk.Button(buttons_frame, text="Play Again", 
                                  font=BUTTON_FONT,
                                  command=show_welcome_screen,
                                  bg="#28a745", fg="white", width=15, height=2,
                                  relief="raised", borderwidth=2,
                                  activebackground="#218838")
    play_again_button.pack(side="left", padx=10)
    
    quit_button = tk.Button(buttons_frame, text="Quit", 
                            font=BUTTON_FONT,
                            command=app.quit,
                            bg="#dc3545", fg="white", width=15, height=2,
                            relief="raised", borderwidth=2,
                            activebackground="#c82333")
    quit_button.pack(side="right", padx=10)

if __name__ == "__main__":
    success, error_message = load_questions_from_file()
    
    if success:
        show_welcome_screen()
    else:
        show_error_screen(error_message)
        
    app.mainloop()