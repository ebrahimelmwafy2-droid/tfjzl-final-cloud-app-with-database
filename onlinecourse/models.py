import sys
from django.utils import timezone
from django.db import models

# 1. كلاس الكورس الأساسي (Course)
class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

# 2. كلاس الدرس (Lesson)
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return "Title: " + self.title

# 3. كلاس السؤال (Question) - [مطلوب أساسي في Task 1]
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500, default="Question text")
    grade = models.IntegerField(default=1)

    # دالة لحساب إذا كانت الإجابة المختارة صحيحة أم لا للحصول على الدرجة
    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        selected_wrong = self.choice_set.filter(is_correct=False, id__in=selected_ids).count()
        if all_answers == selected_correct and selected_wrong == 0:
            return True
        return False

    def __str__(self):
        return self.question_text

# 4. كلاس الاختيارات (Choice) - [مطلوب أساسي في Task 1]
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500, default="Choice text")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

# 5. كلاس التسجيل (Enrollment) لربط المستخدم بالكورس
class Enrollment(models.Model):
    AUDIENCE = [
        ('user', 'User'),
        ('student', 'Student'),
        ('developer', 'Developer')
    ]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=timezone.now)
    mode = models.CharField(max_length=10, choices=AUDIENCE, default='user')
    rating = models.FloatField(default=5.0)

# 6. كلاس تسليم الامتحان (Submission) - [مطلوب أساسي في Task 1]
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    date_submitted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Submission at " + str(self.date_submitted)
