from django.contrib import admin
from .models import PracticeQuestions, UserAnswer, ProblemTag, SolvedProblem
# Register your models here.
admin.site.register(PracticeQuestions)
admin.site.register(UserAnswer)
admin.site.register(ProblemTag)
admin.site.register(SolvedProblem)
