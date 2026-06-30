from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission

# إعداد لطباعة الاختيارات داخل الأسئلة
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4

# إعداد لعرض الأسئلة داخل الكورس
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2

# إعداد لعرض الدروس داخل الكورس
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5

# تخصيص لوحة تحكم الكورس وتشمل الدروس والأسئلة
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInline]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']

# تخصيص لوحة تحكم الأسئلة وتشمل الاختيارات
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'course', 'grade')
    list_filter = ['course']
    search_fields = ['question_text']

# تخصيص لوحة تحكم الدرس
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']

# تسجيل الكلاسات السبعة في لوحة التحكم
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Instructor)
admin.site.register(Learner)
