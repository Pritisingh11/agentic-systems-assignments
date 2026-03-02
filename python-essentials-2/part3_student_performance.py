class StudentPerformance:
    def __init__(self, scores):
        self.scores = scores

    def score_difference(self):
        try:
            if len(self.scores) == 0:
                raise ValueError("No scores available to calculate difference")
            difference = self.scores[-1] - self.scores[0]
            print(f"Difference between last and first score is: {difference}")
        except ValueError as e:
            print(e)


# Take input from user
scores_input = input("Enter scores separated by spaces: ")
scores = list(map(int, scores_input.split()))
student = StudentPerformance(scores)
student.score_difference()
