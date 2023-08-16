from .models import *
from django.db.models import Sum
from faker import Faker
fake = Faker()
import random

def create_subject_marks():
    try:
        student_obj = Student.objects.all()
        for student in student_obj:
            subject_obj = Subject.objects.all()
            for subject in subject_obj:
                SubjectMarks.objects.create(
                    student = student,
                    subject = subject,
                    marks = random.randint(0, 100)
                )
    except Exception as e:
        print(e)


def seed_db(n=10) ->None:
    try:
        for _ in range(n):
            department_obj = Department.objects.all()
            random_index = random.randint(0, len(department_obj)-1)

            department = department_obj[random_index]
            student_id = f"STU-0{random.randint(100, 999)}"
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(20, 30)
            student_address = fake.address()

            stud_id_obj = StudentId.objects.create(student_id = student_id)

            stud = Student.objects.create(
                department = department,
                student_id = stud_id_obj,
                student_name = student_name,
                student_email = student_email,
                student_age = student_age,
                student_address = student_address
            )
    except Exception as e:
        print(e)


def generate_report_card():
    ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('-marks', 'student_age')
    current_rank = -1
    i = 1
    for rank in ranks:
        obj = ReportCard.objects.create(
            student = rank,
            student_rank = i
        )
        i += 1