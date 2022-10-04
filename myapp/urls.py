from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views
app_name = 'myapp'

urlpatterns = [
 # path(r'', views.index, name='index'),
 path(r'index/', views.index, name='index'),
 path(r'about/', views.about, name='about'),
 path(r'courses/', views.courses, name='courses'),
 path(r'detail/<top_no>/', views.detail, name='detail'),
 path(r'place_order/', views.place_order, name='place_order'),
 path(r'myorders/', views.myorders, name='myorders'),
 path(r'courses/<int:cour_id>/', views.coursedetail, name='course_detail'),
 path(r'register/', views.register, name='register'),
 path(r'', views.registerstudent, name='registerstudent'),
 path(r'user_login/', views.user_login, name='user_login'),
 path(r'user_logout/', views.user_logout, name='user_logout'),
 path(r'my_account/', views.myaccount, name='myaccount'),
 path(r'forgot_password', views.forgot_password, name='forgot_password'),  # submit email form
 # path(r'email_sent/', auth_views.PasswordResetDoneView.as_view(), name = "email_sent"),  # email sent successfully
 # path(r'reset/<ud>', auth_views.PasswordResetConfirmView.as_view(), name="reset_password_link"),  # link to password reset in email
 # path(r'reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="reset_password_complete"),  #Password changed successfully

]
