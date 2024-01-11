def validated_input(prompt: str, expected_type: int) -> str | int | tuple[str, str]:
    """
    Validates input depending on expected type displaying error
    prompt if an error occurs. If and error occurs, the function calls
    itself, restarting the process, otherwise, return a str, int or tuple[str, str]
    """
    input_ = input(prompt)

    if expected_type == 1: # Personal ID
        if input_.isdigit():
            return input_
        print("Personnumret får bara innehålla siffror, försök igen!")
        return validated_input(prompt, expected_type)
    elif expected_type == 2: # Name
        names = input_.strip(" ").split(" ") # Splits the name into first and lastname, name can contain numbers example: elon musk baby
        if len(names) >= 2: # Name must contain first and lastname
            return " ".join(names[0:-1]), names[-1] # Returns tuple
        print("Namnet måste minst innehålla ett för- och efternamn, försök igen!")
        return validated_input(prompt, expected_type)
    elif expected_type == 3: # Amount of students
        if input_.isdigit() and int(input_) > 0:
            return int(input_)
        return validated_input(prompt, expected_type)

class School:
    def __init__(self, name):
        self.name = name
        self.students = []
        
    def add_student(self):
        """
        Appends student instance to school
        """
        first_name, last_name = validated_input("Vad heter studenten? ", 2) # Calls validated_input function which returns a tuple[str, str] (firstname, lastname)

        personal_id = validated_input("Vad är studentens personnummer? ", 1) # Calls validated_input function which returns a valid id

        student = Student(first_name, last_name, personal_id) # Creates the instaces
        self.students.append(student) # Appends the instance into the student list

    def search_students(self, query, tag):
        """
        Searches school for student with matching attribute
        """
        return [student for student in self.students if query in getattr(student, tag, "")]
    
    def print_student(self, student):
        """
        Prints student
        """
        print(f"Student: {student.first_name} {student.last_name} med Personnummer: {student.personal_id} går på {self.name}")

class Student:
    def __init__(self, first_name, last_name, personal_id):
        self.first_name = first_name
        self.last_name = last_name
        self.personal_id = personal_id

    def __repr__(self) -> str:
        return self.first_name + self.last_name + self.personal_id

def main():
    """
    Main function that adds students from student class to school class.
    Later you can search for a specific student.
    """

    school = School("KTH")

    for _ in range(validated_input("Hur många studenter vill du lägga till? ", 3)): # Amount of student loop
        school.add_student()
    
    tag = input("Vad vill du söka med för typ? (förnamn, efternamn eller personnummer): ")
    query = input(f"Vilka {tag} vill du söka efter?: ")
    tag = {"förnamn": "first_name", "efternamn": "last_name", "personnummer": "personal_id"}.get(tag, "") # Allows user to write, förnamn instead of attribute name
    results = school.search_students(query, tag)
    for student in results: # Displays returned students, if any
        school.print_student(student)
    
                 
if __name__ == "__main__":
    main() # Entry point