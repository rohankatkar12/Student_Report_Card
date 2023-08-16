from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .forms import *
from .models import *

#User = get_user_model()

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username = username)
        if user.exists():
            messages.error(request, "Username already taken....")
            return redirect("/register/")
        
        if len(password) < 6:
            messages.error(request, "Password must be atleast 6 characters....")
            return redirect("/register/")
        
        # Email Validation using regular expression--->
        # if not re.match(r'^.+@[^.].*\.[a-z]{2,10}$', email):
        #     messages.info(request, "Invalid Email")
        #     return redirect("/reciepe/register/")
        
        form = EmailForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username
            )
            user.set_password(password)
            user.is_staff = True
            user.save()
        else:
            messages.error(request, "Invalid Email....")
            return redirect("/register/")

        return redirect('/register/')

    return render(request, "register.html")



def login_page(request):
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid Username")
            return redirect("/login/")
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect("/login/")
        else:
            login(request, user)
            return redirect('/')

    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("/login/")

@login_required(login_url='login/')
def get_student(request):
    students = ReportCard.objects.all()
    if request.GET.get('search'):
        search = request.GET.get('search')
        students = students.filter(
            Q(student__department__department__icontains = search) |
            Q(student__student_name__icontains = search) |
            Q(student__student_id__student_id__icontains = search) |
            Q(student__student_email__icontains = search) |
            Q(student__student_age__icontains = search) 
        )
        paginator = Paginator(students, len(students))
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'students.html', context={'students_page':page_obj})
    
    paginator = Paginator(students, 15)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'students.html', context={'students_page':page_obj})


@login_required(login_url='/')
def see_marks(request, student_id):
    queryset = SubjectMarks.objects.filter(student__student_id__student_id = student_id)
    # stud_name = students[0].student.student_name
    total = queryset.aggregate(total = Sum('marks'))
    ranks = ReportCard.objects.all()
    return render(request, 'see_marks.html', {'queryset':queryset,'total':total, 'ranks':ranks})



 
