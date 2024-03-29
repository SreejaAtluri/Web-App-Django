# Import necessary classes
import string
from datetime import datetime
from random import random

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import OrderForm, InterestForm, RegisterUserForm, RegisterStudentForm
from .models import Topic, Course, Student, Order
from django.contrib.auth import authenticate, login, logout, hashers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm

def register(request):
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:user_login')
    return render(request, 'myapp/register.html', {'form': form })

def registerstudent(request):
    if request.method == 'POST':
        form = RegisterStudentForm(request.POST, request.FILES or None)
        if form.is_valid():
            student = form.save(commit=False)
            student.set_password(student.password)
            student.save()
            form.save_m2m()
            return redirect('myapp:user_login')
    else:
        form = RegisterStudentForm()
    return render(request, 'myapp/registerstudent.html', {'form': form })

def user_login(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            print("test cookie worked")
        else:
            print("test cookie didn't work")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = datetime.now().strftime("%H:%M:%S - %B %d, %Y")
                request.session.set_expiry(3600)
                # request.session.set_expiry(0)
                return HttpResponseRedirect(reverse('myapp:myaccount'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        request.session.set_test_cookie()
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    # for key in list(request.session.keys()):
    #     del request.session[key]
    return redirect('myapp:user_login')

@login_required
def myaccount(request):
    students = Student.objects.filter(pk=request.user.id)
    if len(students) == 1:
        student = students[0]
        return render(request, 'myapp/myaccount.html', {'fullName': student.first_name + " " + student.last_name,
        'orders': student.order_set.all(), 'interested_in': student.interested_in.all()})
    else:
        return HttpResponse('You are not a registered student!')

# Create your views here.
@login_required
def index(request):
    student_exist = Student.objects.filter(username=request.user.username).count()
    print(student_exist,"suuuuuuuuuuu")
    top_list = Topic.objects.all().order_by('id')[:10]
    if 'last_login' in request.session:
        last_login = request.session['last_login']
    else:
        request.session.flush()
        last_login = 'Your last login was more than one hour ago'
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of topics: ' + '</p>'
    # response.write(heading1)
    # for topic in top_list:
    #     para = '<p>' + str(topic.id) + ': ' + str(topic) + '</p>'
    #     response.write(para)
    #
    # top_courses = Course.objects.all().order_by('-price')[:5]
    # heading2 = '<p>' + 'List of Courses: ' + '</p>'
    # response.write(heading2)
    # for course in top_courses:
    #     if course.for_everyone:
    #         avail = "This Course is For Everyone"
    #     else:
    #         avail = "This Course is Not For Everyone!"
    #     para = '<p>'+ str(course.name) + ': ' + str(course.price) + ': ' + str(avail) + '</p>'
    #     response.write(para)
    #
    # return response
    # return render(request, 'myapp/index0.html', {'top_list': top_list})
    return render(request, 'myapp/index.html', {'top_list': top_list, 'last_login': last_login, 'student_exist': student_exist})

@login_required
def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})

@login_required
def about(request):
    if 'about_visits' in request.session:
        request.session['about_visits'] += 1
    else:
        request.session['about_visits'] = 1
        request.session.set_expiry(300)
    # response = HttpResponse()
    # heading1 = '<p>' + 'This is an E-learning Website! Search our Topics to find all available Courses. ' + '</p>'
    # response.write(heading1)
    # return response
    # return render(request, 'myapp/about0.html')
    return render(request, 'myapp/about.html', {'about_visits': request.session['about_visits']})

@login_required
def detail(request, top_no):
    topic = get_object_or_404(Topic, pk=top_no)
    # response = HttpResponse()
    #
    # heading1 = '<p>' + 'List of courses under ' + topic.name + '</p>'
    # response.write(heading1)
    # subheading1 = '<p>' + 'Category: ' + topic.category + '</p>'
    # response.write(subheading1)
    #
    # course_list = Course.objects.filter(topic=top_no)
    # for course in course_list:
    #     para = '<p>' + str(course.name) + ': ' + str(course.price) + '</p>'
    #     response.write(para)
    # return response

    name = topic.name
    category = topic.category
    course_list = Course.objects.filter(topic=top_no)
    # return render(request, 'myapp/detail0.html', {'name': name, 'course_list': course_list, 'category': category})
    return render(request, 'myapp/detail.html', {'name': name, 'course_list': course_list, 'category': category})

@login_required
def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                order.save()
                msg = 'Your course has been ordered successfully.'
                if order.course.price > 150:
                    print(order.course.discount(), "discount**************")
                    order.course.price = order.course.discount()
                    order.course.save()
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg,
                                                     'courlist': courlist})
@login_required
def coursedetail(request, cour_id):
    msg = ''
    course_list = Course.objects.all().filter(id=cour_id)
    if request.method == 'POST':
        form = InterestForm(request.POST, request.FILES)
        if form.is_valid():
            # course = form.save(commit=False)
            data = form.cleaned_data
            course = Course.objects.get(id=cour_id)
            # isInterested = int(data['interested'])
            if data['interested'] == 'Yes':
                isInterested=1
            elif data['interested'] == 'No':
                isInterested = 0
            print(isInterested)
            if isInterested >= 1:
                course.interested = course.interested+isInterested
                course.save()
                msg = 'Course Interest Added '
            else:
                course.save()
                msg = 'Course Interest Not Added '
        return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = InterestForm()
    return render(request, 'myapp/coursedetail.html', {'form': form, 'courlist': course_list})


@login_required
def myorders(request):
    students = Student.objects.filter(pk=request.user.id)
    if len(students) == 1:
        orders = Order.objects.all().filter(student_id=request.user.id)
        return render(request, 'myapp/myorders.html', {'student': students[0], 'orders': orders})
    else:
        return render(request, 'myapp/myorders.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email,"email**************")
        student = Student.objects.get(email=email)

        if student:
            random_password = Student.objects.make_random_password()
            # print(random_password)
            student.set_password(random_password)
            student.save()
            send_mail(

                subject=f'{student.first_name}: Here is your new password',
                message=f'Your new password is: {random_password}. Please change your password from myaccount page',
                from_email="sreejaatluri33@gmail.com",
                recipient_list=[student.email, ],
                fail_silently=False

            )

        return redirect('myapp:user_login')

    return render(request, 'myapp/forgotpassword.html')