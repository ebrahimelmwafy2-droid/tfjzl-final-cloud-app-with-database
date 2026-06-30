from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

# دالة مساعدة لجلب الإجابات من الـ Request المذكورة في التعليمات
def extract_answers(request):
    selected_choices = []
    for key, value in request.POST.items():
        if 'choice_' in key:
            try:
                choice = Choice.objects.get(pk=value)
                selected_choices.append(choice)
            except Choice.DoesNotExist:
                pass
    return selected_choices

# 1. دالة الـ submit الرسمية
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    # جلب أو إنشاء الـ enrollment للمستخدم الحالي
    try:
        enrollment = Enrollment.objects.get(user=user, course=course)
    except Enrollment.DoesNotExist:
        enrollment = Enrollment.objects.create(user=user, course=course)
        
    submission = Submission.objects.create(enrollment=enrollment)
    choices = extract_answers(request)
    submission.choices.set(choices)
    submission_id = submission.id
    
    return HttpResponseRedirect(reverse(viewname='onlinecourse:exam_result', args=(course.id, submission_id,)))

# 2. دالة عرض النتيجة الرسمية
def show_exam_result(request, course_id, submission_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = Submission.objects.get(id=submission_id)
    choices = submission.choices.all()

    total_score = 0
    questions = course.question_set.all()

    for question in questions:
        correct_choices = question.choice_set.filter(is_correct=True)
        selected_choices = choices.filter(question=question)

        # التحقق من تطابق الاختيارات
        if set(correct_choices) == set(selected_choices):
            total_score += question.grade

    context['course'] = course
    context['grade'] = total_score
    context['choices'] = choices

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
