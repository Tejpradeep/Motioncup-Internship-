import random

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0

    def display_question(self, question):
        print(question['question'])
        for i, option in enumerate(question['options'], start=1):
            print(f"{i}. {option}")
        print()

    def get_user_answer(self):
        while True:
            try:
                user_input = int(input("Enter the your answer: "))
                if 1 <= user_input <= 4:
                    return user_input
                else:
                    print("Invalid input. Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def evaluate_answer(self, user_answer, correct_answer):
        if user_answer == correct_answer:
            print("Correct!\n")
            self.score += 1
        else:
            print(f"Incorrect. The correct answer is: {correct_answer}. \n")

    def conduct_quiz(self):
        for i, question in enumerate(self.questions, start=1):
            print(f"Question {i}:")
            self.display_question(question)
            user_answer = self.get_user_answer()
            self.evaluate_answer(user_answer, question['correct_answer'])

        print(f"Your final score is: {self.score}/{len(self.questions)}")


if __name__ == "__main__":
    
    quiz_questions = [
        {
            'question': "What is the capital of France?",
            'options': ["Berlin", "Madrid", "Paris", "Rome"],
            'correct_answer': 3
        },
        {
            'question': "Which planet is known as the Red Planet?",
            'options': ["Mars", "Jupiter", "Venus", "Saturn"],
            'correct_answer': 1
        },
        {
            'question': "What is the largest mammal on Earth?",
            'options': ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
            'correct_answer': 2
        }
        
    ]

    random.shuffle(quiz_questions)  

    my_quiz = Quiz(quiz_questions)
    my_quiz.conduct_quiz()
