from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Course, Subject, Department
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Course, PythonTopic, LectureVideo, CourseFile, Question
from django.core.paginator import Paginator
from .ai import get_final_answer
# Create your views here.


def index(request):
    return render(request, 'academics/index.html')


class CourseListView(ListView):
    model = Course
    template_name = 'academics/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'academics/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
#2️⃣ Django sends the captured parameter to the view
# When you click a course link:
# <a href="{% url 'course-detail' course.id %}">{{ course.name }}</a>
# Django calls CourseDetailView and sends:
# {'pk': 3}   # if course id = 3
# This {'pk': 3} is automatically sent as a keyword argument to your view method, like get_context_data.
        context = super().get_context_data(**kwargs)
        course = self.object
        topics_ = PythonTopic.objects.filter(course=course).order_by('id')
        paginator = Paginator(topics_, 20)
        page = int(self.request.GET.get('page', 1))
        topics = paginator.get_page(page)

        for topic in topics:
            if topic.example_code:
            # Strip any leading or trailing empty lines
                lines = topic.example_code.strip().splitlines()
                # Remove spaces from the first actual code line
                if lines:
                    lines[0] = lines[0].lstrip()
                    topic.example_code = "\n".join(lines)

        # Add related topics, videos, and files
        context['topics'] = topics
        context['videos'] = LectureVideo.objects.filter(course=course)
        context['files'] = CourseFile.objects.filter(course=course)

        
        questions = Question.objects.filter(course=course, page_number=page).order_by('id')
        context['questions_page'] = questions
        
        return context

class SubjectList(ListView):
    model = Subject
    template_name = 'academics/subject_list.html'
    context_object_name = 'subjects'
    
    
    
def branch_subject_view(request):
    departments = Department.objects.all()
    selected_id = request.GET.get('branch_id')

    selected_department = None
    semesters = []

    if selected_id:
        selected_department = Department.objects.get(id=selected_id)
        semesters = selected_department.semester_set.prefetch_related('subject_set')

    return render(request, 'academics/branch_subjects.html', {
        'departments': departments,
        'selected_department': selected_department,
        'semesters': semesters
    })


def ask_gemini(request):
    response = ""
    prompt = ""
    
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        if prompt:
            response = get_final_answer(prompt)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"response": response})
   
    return render(request, "academics/ai.html", 
                   {"response": response,
        "prompt": prompt})
    
    
    




# ###### Python Course Model #######
# def python_course(request):
#     # Get the "Python" course or return 404 if not found
#     course = get_object_or_404(Course, name="Python")

#     # Get all topics, videos, and files related to this course
#     topics = PythonTopic.objects.filter(course=course).order_by('id')
#     videos = LectureVideo.objects.filter(course=course)
#     files = CourseFile.objects.filter(course=course)

#     return render(request, 'academics/python.html', {
#         'course': course,
#         'topics': topics,
#         'videos': videos,
#         'files': files,
#     })

######### Compiler(Python) ###############
from django.views.decorators.csrf import csrf_exempt
import requests
import base64
import time
@csrf_exempt
def run_code(request):
    context = {}
    if request.method == "POST":
        code = request.POST.get("code", "")
        inp = request.POST.get("inp", "")

        headers = {
            "Content-Type": "application/json",
            "X-RapidAPI-Key": "2289620fd3msh8c3eeaa96f71c18p181243jsn7bcc6fc11399",
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
        }

        payload = {
            "language_id": 71,  # Python 3
            "source_code": base64.b64encode(code.encode()).decode(),
            "stdin": base64.b64encode(inp.encode()).decode()
        }

        # Submit code
        res = requests.post("https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=true&wait=false", headers=headers, json=payload)
        token = res.json().get("token")
        time.sleep(2)

        # Fetch result
        result = requests.get(f"https://judge0-ce.p.rapidapi.com/submissions/{token}?base64_encoded=true", headers=headers).json()

        output = result.get("stdout") or result.get("stderr") or result.get("compile_output") or "No output"
        if output:
            try:
                output = base64.b64decode(output).decode()
            except Exception:
                pass

        # Send data back to template
        context = {
            "output": output,
            "code": code,
            "stdin": inp
        }

    return render(request, "academics/coding_langs/compiler.html", context)

LANGUAGE_IDS = {
    
    "react": 63,
    "python": 71,       # Python 3
    "c": 50,            # C (GCC 9.2.0)
    "cpp": 54,          # C++ (GCC 9.2.0)
    "java": 62,         # Java (OpenJDK 13.0.1)
    "javascript": 63,   # JavaScript (Node.js 12.14.0)
    "nodejs": 63        # Same as JavaScri
}

LANGUAGE_LABELS = {
    "c": "C",
    "python": "Python",
    "javascript": "JavaScript",
    "node": "Node.js",
    "react": "React",
    "cpp": "CPP",
    "java": "Java"
}


DEFAULT_CODE = {
    "python": 'print("Hello, World!")',
    "c": '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
    "cpp": '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, World!" << endl;\n    return 0;\n}',
    "javascript": 'console.log("Hello, World!");',
    "nodejs": 'console.log("Hello, Node.js World!");',
    "java": 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
}

@csrf_exempt
def run_code_big(request):
    output = ""
    code = ""
    inp = ""
    active_language = "python"

    if request.method == "POST":
        active_language = request.POST.get("language", "python")
        code = request.POST.get("code") or DEFAULT_CODE.get(active_language, "")
        if not code.strip():
            code = DEFAULT_CODE.get(active_language, "")
        inp = request.POST.get("inp", "")
    
        headers = {
            "Content-Type": "application/json",
            "X-RapidAPI-Key": "2289620fd3msh8c3eeaa96f71c18p181243jsn7bcc6fc11399",
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
        }

        payload = {
            "language_id": LANGUAGE_IDS.get(active_language, 71),
            "source_code": base64.b64encode(code.encode()).decode(),
            "stdin": base64.b64encode(inp.encode()).decode()
        }

        # Submit code and wait for result
         # Submit code
        res = requests.post("https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=true&wait=false", headers=headers, json=payload)
        print(res.status_code)   # Should be 200
        print(res.text)   
        token = res.json().get("token")
        time.sleep(2)

        # Fetch result
        result = requests.get(f"https://judge0-ce.p.rapidapi.com/submissions/{token}?base64_encoded=true", headers=headers).json()

        output = result.get("stdout") or result.get("stderr") or result.get("compile_output") or "No output"
        if output:
            try:
                output = base64.b64decode(output).decode()
            except Exception:
                pass
    else:
        code = DEFAULT_CODE.get(active_language, "")
        
    context = {
        "output": output,
        "code": code,
        "active_language": active_language,
        "language_labels": LANGUAGE_LABELS,
        "DEFAULT_CODE": DEFAULT_CODE
    }
    return render(request, "academics/coding_langs/big_compiler.html", context)
