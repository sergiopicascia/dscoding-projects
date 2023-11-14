import pandas as pd
from quiz import Quiz

def main():
    # Load quiz data
    quiz_data = pd.read_csv('/all_qiuzable_roles.csv')  # Update the path to your CSV file
    quiz = Quiz(quiz_data)

    while True:
        quiz.take_quiz()
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            break

if __name__ == "__main__":
    main()