class StudentScores:
    def __init__(self, scores):
        self.scores = scores

    def highest_last_two(self):
        try:
            if len(self.scores) < 2:
                raise ValueError("Not enough scores to find highest value")
            highest = max(self.scores[-2:])
            print(f"Highest score among last two is: {highest}")
        except ValueError as e:
            print(e)


# Take input from user
scores_input = input("Enter scores separated by spaces: ")
scores = list(map(int, scores_input.split()))
student = StudentScores(scores)
student.highest_last_two()
