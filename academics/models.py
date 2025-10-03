from django.db import models
from django.core.validators import FileExtensionValidator
from django.shortcuts import redirect, render

# Create your models here.



class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    
    
    
    
# …existing Course and LectureVideo models stay as‑is …










                                    ### Engineering Courses
                                    
class Department(models.Model):
    name = models.CharField(200)
    code = models.CharField(10, unique=True)
    
    def __str__(self):
        return self.code    
    
class Semester(models.Model):
    number = models.IntegerField(10)
    name = models.CharField(200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name  or f"Semester {self.number}"
    
class Subject(models.Model):
    name = models.CharField(200)
    department  = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester  = models.ForeignKey(Semester, on_delete=models.CASCADE)
    url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    

    
# class SubjectFile(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='files')
#     description = models.CharField(1000, help_text="e.g Unit 1")
#     file = models.FileField(
#         upload_to="subject_files/%Y/%m/",
#         validators=[FileExtensionValidator(['pdf', 'docx', 'pptx','xlsx'])]
#     )
#     uploaded_to = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"{self.description} ({self.subject.name})"
    
    
class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255, blank=True, null=True)
    option4 = models.CharField(max_length=255, blank=True, null=True)
    correct_option = models.CharField(
        max_length=1,
        choices=[("1", "Option 1"), ("2", "Option 2"), ("3", "Option 3"), ("4", "Option 4")]
    )
    page_number = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return self.text
    
    
    ######## CODING LANGUAGES  ##########
    # models.py

class PythonTopic(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='topics'
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(help_text="Use basic HTML or rich text for formatting.", blank=True, null=True)
    example_code = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='topics/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="Optional embedded video URL (YouTube etc.)")
    show_compiler = models.BooleanField(default=True)

    def __str__(self):
        return self.title or ""


class LectureVideo(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='videos'
    )
    title = models.CharField(max_length=200)
    youtube_url = models.URLField(help_text="Paste full YouTube URL (e.g. https://youtu.be/xyz)")

    def youtube_id(self):
        import re
        match = re.search(r'(?:v=|youtu\.be/)([^&]+)', self.youtube_url)
        return match.group(1) if match else None

    def thumbnail_url(self):
        vid = self.youtube_id()
        return f"https://img.youtube.com/vi/{vid}/hqdefault.jpg" if vid else ""

    def __str__(self):
        return f"{self.title} ({self.course.name})"


class CourseFile(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="files"
    )
    description = models.CharField(max_length=200, help_text="e.g. Week‑1 Notes")
    file = models.FileField(
        upload_to="course_files/%Y/%m/",
        validators=[FileExtensionValidator(['pdf'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} ({self.course.name})"