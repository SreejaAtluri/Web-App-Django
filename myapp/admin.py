import decimal

from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order
# Register your models here.
admin.site.register(Order)

class CourseInline(admin.TabularInline):
    model = Course


class TopicAdmin(admin.ModelAdmin):
    inlines = [
        CourseInline
    ]
    def __str__(self):
        return f"{self.name} ({self.category})"

def apply_discount(modeladmin, request, queryset):
    for book in queryset:
        book.price = book.price * decimal.Decimal('0.9')
        book.save()
apply_discount.short_description = 'Apply 10%% discount'

class CourseAdmin(admin.ModelAdmin):
    list_display = ['topic', 'name', 'price', 'for_everyone', 'description']
    actions = [apply_discount, ]

class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'address')


admin.site.register(Course, CourseAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Student, StudentAdmin)
