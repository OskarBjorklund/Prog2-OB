class School:
    def __init__(self):
        self.student_list = []

    def add_student(self, student):
        self.student_list.append(student)

    def display_students(self):
        for student in self.student_list:
            student.showcase_information()

    def search_for_student(self):
        searched_student = input("Sök på personnummer: ")
        student_exists = False
        for student in self.student_list:
            if  student.give_personal_number() == searched_student:
                student_exists = True
                print("Studenten går på KTH:")
                student.showcase_information()
        if student_exists == False:
            print("Studenten går inte på KTH")

class Student:
    def __init__(self, _first_name, _last_name, _personal_number):
        self.first_name = _first_name
        self.last_name = _last_name
        self.personal_number = _personal_number
    
    def showcase_information(self):
        print(self.first_name, self.last_name, self.personal_number)

    def give_personal_number(self):
        return self.personal_number
    
def fetch_list_of_students_from_file():
    wrong_input = True
    while wrong_input:
        try:
            file_name = str(input("Skriv in namnet på filen som ska öppnas: "))
            file_with_students = open(file_name, "r", encoding="utf-8")

            list_from_file_with_students = file_with_students.readlines()

            file_with_students.close()

            for i in range(0, len(list_from_file_with_students)):
                list_from_file_with_students[i] = list_from_file_with_students[i].strip()

            print(list_from_file_with_students)

            return list_from_file_with_students
        except:
            print("Filen hittades inte. Försök igen.\n")


def main():
    school = School()
    list_of_students = fetch_list_of_students_from_file()

    for i in range(0, len(list_of_students), 3):
        school.add_student(Student(list_of_students[i+2], list_of_students[i+1], list_of_students[i+0]))

    print("\nDessa studenter går på KTH: ")
    school.display_students()

    print()
    school.search_for_student()

main()