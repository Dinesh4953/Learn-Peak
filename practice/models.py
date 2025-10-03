from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField 
# Create your models here.

class ProblemTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class PracticeQuestions(models.Model):
    DIFFICULTY_CHOISES = [
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H','Hard'),
    ]
    
    title = models.CharField(max_length=500)
    question_text = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOISES)
    solution = models.TextField(blank=True)
    tags = models.ManyToManyField(ProblemTag)
    contest_id = models.IntegerField()
    index = models.CharField(max_length=10)
    question_number = models.IntegerField(unique=True) 
    
    def __str__(self):
        return f"{self.title} ({self.difficulty})"
    
    
    
class SolvedProblem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(PracticeQuestions, on_delete=models.CASCADE)
    solved_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'problem')  # prevent duplicates

    def __str__(self):
        return f"{self.user.username} solved {self.problem.title}"
    
    
    
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(PracticeQuestions, on_delete=models.CASCADE)
    answer = models.TextField(blank=True)
    # You can submit the form without filling answer (blank=True)
    
    is_correct = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now=True)
    
    ## auto_now=True    --->    Updates to current time every time saved
    #    auto_now_add=True ------>  Sets to current time only on creation
    class Meta:
        unique_together = ('user', 'question')
        
        
        ### class Meta: is a special inner class used to define metadata — extra settings that control how your model behaves in the database, admin, and Django ORM.
        
        
        
        
    def __str__(self):
        return f"{self.user.username} - {self.question.title}"