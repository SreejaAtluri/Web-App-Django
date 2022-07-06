#Import necessary classes
from django.shortcuts import render, get_object_or_404
from .models import Topic, Course, Student, Order



# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
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
    return render(request, 'myapp/index.html', {'top_list': top_list})

def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist} )

def about(request):
    # response = HttpResponse()
    # heading1 = '<p>' + 'This is an E-learning Website! Search our Topics to find all available Courses. ' + '</p>'
    # response.write(heading1)
    # return response
    # return render(request, 'myapp/about0.html')
    return render(request, 'myapp/about.html')

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