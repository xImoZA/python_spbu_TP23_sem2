from collections import Counter

import pytest

from src.Control_tests.retest_1.task_1 import *

mathan = Course("Mathematical Analysis", 62)
informatics = Course("Computer Science", 32)
algebra = Course("Algebra and Number Theory", 32)
t1 = Teacher("Широков Николай Алексеевич", [])
t2 = Teacher("Терехов Андрей Николаевич", [])
t3 = Teacher("Иванова Ольга Юрьевна", [algebra])
s1 = Student("Eren Jaeger", [mathan], {mathan: 5, informatics: 2})
s2 = Student("Satoru Gojo", [], {informatics: 4})
s3 = Student("ABOBA", [], {})
uni = University([], [], [])


class TestUniversity:
    @pytest.mark.parametrize("student", [s1, s2])
    def test_add_student(self, student: Student) -> None:
        uni.add_student(student)
        assert student in uni.students

    @pytest.mark.parametrize("teacher", [t1, t2])
    def test_add_teacher(self, teacher: Teacher) -> None:
        uni.add_teacher(teacher)
        assert teacher in uni.teachers

    @pytest.mark.parametrize("course", [mathan, informatics])
    def test_add_course(self, course: Course) -> None:
        uni.add_course(course)
        assert course in uni.courses

    @pytest.mark.parametrize(
        "name_teacher, name_course",
        [["Широков Николай Алексеевич", "Mathematical Analysis"], ["Терехов Андрей Николаевич", "Computer Science"]],
    )
    def test_add_course_for_teacher(self, name_teacher: str, name_course: str) -> None:
        uni.add_course_for_teacher(name_teacher, name_course)
        assert uni._get_course(name_course) in uni._get_teacher(name_teacher).courses

    @pytest.mark.parametrize(
        "name_student, name_course", [["Eren Jaeger", "Computer Science"], ["Satoru Gojo", "Computer Science"]]
    )
    def test_add_course_for_student(self, name_student: str, name_course: str) -> None:
        uni.add_course_for_student(name_student, name_course)
        assert uni._get_course(name_course) in uni._get_student(name_student).courses

    @pytest.mark.parametrize("name_student, expected", [["Eren Jaeger", s1], ["Satoru Gojo", s2]])
    def test_get_student(self, name_student: str, expected: Course) -> None:
        assert uni._get_student(name_student) == expected

    def test_errors_get_student(self) -> None:
        with pytest.raises(ValueError):
            uni._get_student("ABOBA")

    @pytest.mark.parametrize(
        "name_teacher, expected", [["Широков Николай Алексеевич", t1], ["Терехов Андрей Николаевич", t2]]
    )
    def test_get_teacher(self, name_teacher: str, expected: Course) -> None:
        assert uni._get_teacher(name_teacher) == expected

    def test_errors_get_teacher(self) -> None:
        with pytest.raises(ValueError):
            uni._get_teacher("Иванова Ольга Юрьевна")

    @pytest.mark.parametrize(
        "name_course, expected", [["Mathematical Analysis", mathan], ["Computer Science", informatics]]
    )
    def test_get_course(self, name_course: str, expected: Course) -> None:
        assert uni._get_course(name_course) == expected

    def test_errors_get_course(self) -> None:
        with pytest.raises(ValueError):
            uni._get_course("Algebra and Number Theory")

    def test_get_average_grade_student(self) -> None:
        assert uni.get_average_grade_student(s1.name) == 3
        assert uni.get_average_grade_student(s2.name) == 4

    def test_get_list_courses_student(self) -> None:
        assert uni.get_list_courses_student(s1.name) == s1.courses
        assert uni.get_list_courses_student(s2.name) == s2.courses

    def test_get_list_courses_teacher(self) -> None:
        assert uni.get_list_courses_teacher(t1.name) == t1.courses
        assert uni.get_list_courses_teacher(t2.name) == t2.courses

    def test_get_list_students(self) -> None:
        assert Counter(uni.get_list_students_on_course("Mathematical Analysis")) == Counter([s1])
        assert Counter(uni.get_list_students_on_course("Computer Science")) == Counter([s1, s2])

    def test_get_list_teachers(self) -> None:
        assert uni.get_list_teachers_on_course("Mathematical Analysis") == [t1] and uni.get_list_teachers_on_course(
            "Computer Science"
        ) == [t2]

    def test_get_average_grade(self) -> None:
        assert uni.get_average_grade("Mathematical Analysis") == 5 and uni.get_average_grade("Computer Science") == 3

    def test_errors_get_average_grade(self) -> None:
        with pytest.raises(ValueError):
            uni.get_average_grade("Algebra and Number Theory")


class TestHuman:
    def test_get_course(self) -> None:
        assert t1.get_courses() == [mathan] and t2.get_courses() == [informatics]
        assert s1.get_courses() == [mathan, informatics] and s2.get_courses() == [informatics]

    def test_get_total_hours(self) -> None:
        assert t1.get_total_hours() == 62 and t2.get_total_hours() == 32
        assert s1.get_total_hours() == 62 + 32 and s2.get_total_hours() == 32


class TestStudent:
    def test_get_grade(self) -> None:
        assert s1.get_grade(mathan) == 5 and s1.get_grade(informatics) == 2 and s2.get_grade(informatics) == 4

    def test_errors_get_grade(self) -> None:
        with pytest.raises(ValueError):
            s2.get_grade(mathan)

    def test_get_average_grade(self) -> None:
        assert s1.get_average_grade() == 3 and s2.get_average_grade() == 4

    def test_errors_get_average_grade(self) -> None:
        with pytest.raises(ValueError):
            s3.get_average_grade()
