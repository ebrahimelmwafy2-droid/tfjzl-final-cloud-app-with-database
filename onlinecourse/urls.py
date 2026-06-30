from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # المسارات الحالية للكورس اتركها كما هي، وأضف المسارين الرسميين بالأسفل:
    path('<int:course_id>/submit/', views.submit, name="submit"),
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name="exam_result"),
]
