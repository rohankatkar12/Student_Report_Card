from django.contrib import admin
from django.db.models import Sum
from .models import *

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department']


@admin.register(StudentId)
class StudentIdAdmin(admin.ModelAdmin):
    list_display = ['student_id']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['department','student_id', 'student_name', 'student_email', 'student_age', 'student_address']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_name']



class SubjectMarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'marks']

admin.site.register(SubjectMarks, SubjectMarksAdmin)


class ReportCardAdmin(admin.ModelAdmin):
    list_display = ['student', 'student_rank', 'total_marks', 'date_of_report_card_geaneration']

    ordering = ['student_rank']

    def total_marks(request, obj):
        subject_marks = SubjectMarks.objects.filter(student = obj.student)
        marks = subject_marks.aggregate(marks = Sum('marks'))
        return marks['marks']

admin.site.register(ReportCard, ReportCardAdmin)



