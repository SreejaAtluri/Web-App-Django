from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)

    def __str__(self):
        return f"{self.name}"

    def discount(self):
        return (self.price - (self.price * .10))


class Student(User):
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    CITY_CHOICES = [('WS', 'Windsor'), ('CG', 'Calgary'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    address = models.CharField(max_length=500, null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic, related_name='students')

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Order(models.Model):
    ORDER_STATUS = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    # course = models.ForeignKey(Course, related_name='orders', on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, related_name='orders')
    student = models.ForeignKey(Student, related_name='orders', on_delete=models.CASCADE)
    levels = models.PositiveIntegerField(default=0)
    order_status = models.IntegerField(choices=ORDER_STATUS, default=0)
    order_date = models.DateField(auto_now_add=True)

    def total_cost(self):
        total = 0
        objects = Order.course.all()
        for order in objects:
            total += order.price
        return total

    def __str__(self):
        return '{} ({})'.format(', '.join(self.course.all().values_list('name', flat=True)), self.order_date)
