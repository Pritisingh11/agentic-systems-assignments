class StudentMarks:
    def __init__(self, marks):
        self.marks = marks

    def last_three_avg(self):
        try:
            if len(self.marks) < 3:
                raise ValueError("Not enough marks to calculate average")
            avg = sum(self.marks[-3:]) / 3
            print(f"Average of last 3 marks is: {avg}")
        except ValueError as e:
            print(e)


# Example usage
marks_input = input("Enter marks separated by spaces: ") 
marks = list(map(int, marks_input.split())) 
student = StudentMarks(marks) 
student.last_three_avg()
