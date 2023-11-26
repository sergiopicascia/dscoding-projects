import pandas as pd
from Quiz_class import Quiz


def main():
    # Load quiz data
    quiz_data = pd.read_csv('all_qiuzable_roles.csv')
    quiz = Quiz(quiz_data)

    playing = True

    while playing:
        quiz.take_quiz()

        while True:
            play_again = input("\n\nDo you want to play again? (yes/no): ").strip().lower()
            if play_again == 'yes':
                break
            elif play_again == 'no':
                playing = False
                print("\n\nThank you for playing!")
                break
            else:
                print("\nPlease insert a valid answer!")


if __name__ == "__main__":
    main()

