import decimal

import django
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
        return self.price - (self.price * decimal.Decimal(0.10))


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


# orders model
class Order(models.Model):
    ORDER_CHOICES = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    levels = models.PositiveIntegerField()
    order_status = models.IntegerField(choices=ORDER_CHOICES, default=1)
    order_date = models.DateField(default=django.utils.timezone.now())

    def __str__(self):
        return self.course.name

    @property
    def total_cost(self):
        return Order.course.price.all().aggregate(sum("price"))
