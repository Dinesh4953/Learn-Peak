from django.contrib import admin
from .models import LectureVideo, Course, CourseFile, Department, Semester, Subject, PythonTopic, Question
# Register your models here.
admin.site.register(Course)
admin.site.register(LectureVideo)
admin.site.register(CourseFile)
admin.site.register(Department)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(PythonTopic)
admin.site.register(Question)



