import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt


def quiz():

    window.destroy()
    import easy_questions
    import medium_questions
    import hard_questions


window = tk.Tk()
window.title("Movie Quiz")

def main_window():

    window_width, window_height = 800, 400 
    screen_width = window.winfo_screenwidth()  
    screen_height = window.winfo_screenheight()  
    x_coordinate = int((screen_width/2) - (window_width/2))
    y_coordinate = int((screen_height/2) - (window_height/2))
    window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    message = "Let's start a movie quiz! \n\nThere will be 3 sections (easy, medium, hard) with 4 questions in each. \n Easy questions weigh 10 points each. \nMedium questions weigh 20 points each. \n Hard questions weigh 30 points each."
    msg_label = tk.Label(window, text=message, font=("Helvetica", 14))
    msg_label.pack(pady=20)

    go_button = tk.Button(window, text="Go!", command=quiz, font=("Helvetica", 12))
    go_button.pack()

    close_button = tk.Button(window, text="Close Quiz", command=window.destroy, font=("Helvetica", 12))
    close_button.pack()

    window.mainloop()

main_window()

from easy_questions import easy_total_score
from medium_questions import medium_total_score
from hard_questions import hard_total_score


def create_bar_chart(easy_total_score, medium_total_score, hard_total_score):
    categories = ['Easy', 'Medium', 'Hard']
    scores = [easy_total_score, medium_total_score, hard_total_score]

    plt.figure(figsize=(8, 6))
    plt.bar(categories, scores, color=['green', 'blue', 'red'])
    plt.title('Quiz Scores by Difficulty')
    plt.xlabel('Difficulty Level')
    plt.ylabel('Scores')
    plt.show()

def output_results(name, easy_total_score, medium_total_score, hard_total_score, filename="quiz_results.txt"):
    data = {
        'Difficulty Level': ['Easy', 'Medium', 'Hard'],
        'Score': [easy_total_score, medium_total_score, hard_total_score]
    }
    df = pd.DataFrame(data)

    with open(filename, 'a') as file:
        file.write(f"\n{name}'s Quiz Results:\n")
        file.write(df.to_string(index=False))
        total_score = easy_total_score + medium_total_score + hard_total_score
        file.write(f"\nTotal Quiz Score: {total_score} out of 240\n")

def create_results_window():
    def save_results():
        name = name_entry.get()
        output_results(name, easy_total_score, medium_total_score, hard_total_score)
        root.destroy()
        show_thank_you_window()

    def show_thank_you_window():
        thank_you_root = tk.Tk()
        thank_you_root.title("Thank You")
        screen_width, screen_height = thank_you_root.winfo_screenwidth(), thank_you_root.winfo_screenheight()
        center_x, center_y = int(screen_width / 2 - 200), int(screen_height / 2 - 125)
        thank_you_root.geometry(f"400x250+{center_x}+{center_y}")

        tk.Label(thank_you_root, text="Thank you for your participation!", font=("Arial", 12)).pack()
        tk.Button(thank_you_root, text="Close", command=thank_you_root.destroy).pack()

        thank_you_root.mainloop()

    root = tk.Tk()
    root.title("Quiz Results")
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    center_x, center_y = int(screen_width / 2 - 200), int(screen_height / 2 - 150)
    root.geometry(f"400x300+{center_x}+{center_y}")

    tk.Label(root, text="Please enter your name:", font=("Arial", 12)).pack()
    name_entry = tk.Entry(root, font=("Arial", 10))
    name_entry.pack()
    save_button = tk.Button(root, text="Save Results", command=save_results)
    save_button.pack()
    
    tk.Label(root, text="That's all. Well done!\nYour Quiz Results:", font=("Arial", 12)).pack()
    tk.Label(root, text=f"Total Score for Easy Questions: {easy_total_score}", font=("Arial", 10)).pack()
    tk.Label(root, text=f"Total Score for Medium Questions: {medium_total_score}", font=("Arial", 10)).pack()
    tk.Label(root, text=f"Total Score for Hard Questions: {hard_total_score}", font=("Arial", 10)).pack()

    total_score = easy_total_score + medium_total_score + hard_total_score
    tk.Label(root, text=f"Total Quiz Score: {total_score} out of 240", font=("Arial", 10)).pack()

    chart_button = tk.Button(root, text="Show Results Bar Chart", command=lambda: create_bar_chart(easy_total_score, medium_total_score, hard_total_score))
    chart_button.pack()

    root.mainloop()

create_results_window()
