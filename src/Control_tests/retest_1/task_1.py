import abc


class Course:
    def __init__(self, title: str, hours: int) -> None:
        self.title: str = title
        self.hours: int = hours


class UniversityPerson(metaclass=abc.ABCMeta):
    def __init__(self, courses: list[Course]):
        self.courses: list[Course] = courses

    def add_course(self, course: Course) -> None:
        self.courses.append(course)

    def get_courses(self) -> list[Course]:
        return self.courses

    def get_total_hours(self) -> int:
        total_hours = 0
        for course in self.courses:
            total_hours += course.hours

        return total_hours


class Teacher(UniversityPerson):
    def __init__(self, name: str, courses: list[Course]) -> None:
        super().__init__(courses)
        self.name: str = name


class Student(UniversityPerson):
    def __init__(self, name: str, courses: list[Course], grades: dict[Course, int]) -> None:
        super().__init__(courses)
        self.name: str = name
        self.grades: dict[Course, int] = grades

    def get_grade(self, course: Course) -> int:
        try:
            return self.grades[course]

        except KeyError:
            raise ValueError("The student has not received a grade")

    def get_average_grade(self) -> int:
        avg_grade: int = 0
        report_card = self.grades.items()
        if report_card:
            count = len(report_card)
            for _, grade in report_card:
                avg_grade += grade

            return avg_grade // count

        else:
            raise ValueError("The student has no grades")


class University:
    def __init__(self, courses: list[Course], teachers: list[Teacher], students: list[Student]) -> None:
        self.courses: list[Course] = courses
        self.teachers: list[Teacher] = teachers
        self.students: list[Student] = students

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    def add_teacher(self, teacher: Teacher) -> None:
        self.teachers.append(teacher)

    def add_course(self, course: Course) -> None:
        self.courses.append(course)

    def add_course_for_student(self, name_student: str, title_course: str) -> None:
        student = self._get_student(name_student)
        del self.students[self.students.index(student)]

        course = self._get_course(title_course)
        student.add_course(course)
        self.students.append(student)

    def add_course_for_teacher(self, name_teacher: str, title_course: str) -> None:
        teacher = self._get_teacher(name_teacher)
        del self.teachers[self.teachers.index(teacher)]

        course = self._get_course(title_course)
        teacher.add_course(course)
        self.teachers.append(teacher)

    def _get_student(self, name: str) -> Student:
        for student in self.students:
            if student.name == name:
                return student
        raise ValueError(f"The student {name} does not study at this university")

    def _get_teacher(self, name: str) -> Teacher:
        for teacher in self.teachers:
            if teacher.name == name:
                return teacher
        raise ValueError(f"The teacher {name} does not teaching at this university")

    def _get_course(self, name: str) -> Course:
        for course in self.courses:
            if course.title == name:
                return course
        raise ValueError(f"The course {name} does not available at this university")

    def get_average_grade_student(self, name: str) -> int:
        student = self._get_student(name)
        return student.get_average_grade()

    def get_list_courses_student(self, name: str) -> list[Course]:
        student = self._get_student(name)
        return student.get_courses()

    def get_list_courses_teacher(self, name: str) -> list[Course]:
        teacher = self._get_teacher(name)
        return teacher.get_courses()

    def get_list_students_on_course(self, name: str) -> list[Student]:
        course = self._get_course(name)

        return_list: list[Student] = []

        for student in self.students:
            if course in student.courses:
                return_list.append(student)

        return return_list

    def get_list_teachers_on_course(self, name: str) -> list[Teacher]:
        course = self._get_course(name)

        return_list: list[Teacher] = []

        for teacher in self.teachers:
            if course in teacher.courses:
                return_list.append(teacher)

        return return_list

    def get_average_grade(self, name: str) -> int:
        course = self._get_course(name)
        avg_grade = 0
        students: list[Student] = self.get_list_students_on_course(name)
        if students:
            for student in students:
                avg_grade += student.get_grade(course)

            return avg_grade // len(students)
        else:
            raise ValueError("This course is not attended by students")
