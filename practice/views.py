from django.shortcuts import render, get_object_or_404 ,redirect
from .models import PracticeQuestions, ProblemTag, SolvedProblem
from django.core.paginator import Paginator
import requests
from .models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def problem_list(request):
    selected_tag = request.GET.get('tag')
    selected_diff = request.GET.get('difficulty')
    search_query = request.GET.get('search', '')
    

    
    questions = PracticeQuestions.objects.all()
    
    if selected_tag:
        questions = questions.filter(tags__name = selected_tag)
        
    if selected_diff:
        questions = questions.filter(difficulty = selected_diff)
        
    if search_query != '' and search_query is not None:
        questions = questions.filter(title__icontains=search_query)
        
    tags = ProblemTag.objects.all()
    difficulties = [
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    ]
    
    paginator = Paginator(questions ,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    querydict = request.GET.copy()
    if 'page' in querydict:
        del querydict['page']
    query_string = querydict.urlencode()

    solved_ids = []
    if request.user.is_authenticated:
        fetch_solved_problems_for_user(request.user) ## we just call it since it return list we are not saving bcoz when we call then only it save solved problems in SolvedProblems model
        solved_ids = SolvedProblem.objects.filter(user=request.user).values_list('problem_id', flat=True)

# 3️⃣ How problem_id fits in
# In Django, any ForeignKey field automatically creates a column with _id.
# So problem = models.ForeignKey(PracticeQuestions) → DB column problem_id.
# When you save:
# solved_problem = SolvedProblem.objects.create(user=user, problem=pq)
# Django stores pq.id in problem_id.
# You don’t manually assign problem_id; Django does it via the ForeignKey relationship.

    return render(request, 'practice/problem_list.html', {
        'page_obj': page_obj,
        'tags': tags,
        'difficulties': [('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard')],
        'selected_tag': selected_tag,
        'selected_diff': selected_diff,
        'search_query': search_query,
        'query_string': query_string,
        'solved_ids': solved_ids,
    })


def user_handle_valid(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        print("DEBUG Response:", response.status_code, response.text)  # <- add this
        return response.status_code == 200 and response.json().get("status") == "OK"
    except Exception as e:
        print("❌ Handle validation failed:", e)
        return False

@login_required
def problem_detail(request, pk):
    problem = get_object_or_404(PracticeQuestions, pk=pk)
    has_solved = False
    handle_valid = False
    user_profile = getattr(request.user, "profile", None)

    if user_profile and user_profile.codeforces_handle:
        handle_valid = user_handle_valid(user_profile.codeforces_handle)
        has_solved = SolvedProblem.objects.filter(user=request.user, problem=problem).exists()


    return render(request, 'practice/problem_detail.html', {
        'problem': problem,
        'user_handle_valid': handle_valid,
        'has_solved' : has_solved
    })

def problem_detail_solved(request, pk):
    problem = get_object_or_404(PracticeQuestions, pk=pk)
    return render(request, 'practice/problem_detail_solved.html', {'problem': problem})



def fetch_solved_problems_for_user(user):
    if not hasattr(user, 'profile') or not user.profile.codeforces_handle:
        return []
    handle = user.profile.codeforces_handle
    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1000"
    
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return []
        
        data = response.json()
        solved = set()
        
        for pro in data.get("result", []):
            if pro.get('verdict') == "OK":
                prob = pro.get("problem", {})
                contest_id = prob.get('contestId')
                index = prob.get("index")
                print(f"Trying to get problem: {contest_id}-{index}")
                try:
                    pq = PracticeQuestions.objects.get(contest_id=contest_id, index=index)
                    print("✅ pq found:", pq)
                    solved_problem, created = SolvedProblem.objects.get_or_create(user=user, problem=pq)

                    if created:
                        print("✅ SolvedProblem added for the first time.")
                    else:
                        print("ℹ️ This problem was already marked as solved by the user.")
                    print("Saved (or already exists)")
                    solved.add(pq.id)
                except PracticeQuestions.DoesNotExist:
                    continue
                
                
        return list(solved)
    except Exception as e :
        print(f"Failed to fetch solved problems: {e}")
        return []



def problem_list_1(request):
    
    if request.user.is_authenticated:
        # Sync from Codeforces (optional: only once a day?)
        fetch_solved_problems_for_user(request.user)

        # Get solved problems
        solved_ids = SolvedProblem.objects.filter(user=request.user).values_list('problem_id', flat=True)
    else:
        solved_ids = []

    return render(request, "practice/problem_list.html", {
       
        'solved_ids': solved_ids,
    })
                





                
# from django.shortcuts import render, get_object_or_404
# from .models import PracticeQuestions, ProblemTag, SolvedProblem
# from django.core.paginator import Paginator
# import requests

# def fetch_solved_problems_for_user(user):
#     if not hasattr(user, 'profile') or not user.profile.codeforces_handle:
#         return []
#     handle = user.profile.codeforces_handle
#     url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1000"
#     try:
#         response = requests.get(url)
#         if response.status_code != 200:
#             return []

#         data = response.json()
#         solved = set()

#         for pro in data.get("result", []):
#             if pro.get('verdict') == "OK":
#                 prob = pro.get("problem", {})
#                 contest_id = prob.get('contestId')
#                 index = prob.get("index")
#                 try:
#                     pq = PracticeQuestions.objects.get(contest_id=contest_id, index=index)
#                     SolvedProblem.objects.get_or_create(user=user, problem=pq)
#                     solved.add(pq.id)
#                 except PracticeQuestions.DoesNotExist:
#                     continue

#         return list(solved)
#     except Exception as e:
#         print(f"Failed to fetch solved problems: {e}")
#         return []


# def problem_list(request):
#     selected_tag = request.GET.get('tag')
#     selected_diff = request.GET.get('difficulty')
#     search_query = request.GET.get('search', '')

#     questions = PracticeQuestions.objects.all()

#     if selected_tag:
#         questions = questions.filter(tags__name=selected_tag)

#     if selected_diff:
#         questions = questions.filter(difficulty=selected_diff)

#     if search_query != '' and search_query is not None:
#         questions = questions.filter(title__icontains=search_query)

#     paginator = Paginator(questions, 5)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     tags = ProblemTag.objects.all()
#     difficulties = [
#         ('E', 'Easy'),
#         ('M', 'Medium'),
#         ('H', 'Hard'),
#     ]

#     querydict = request.GET.copy()
#     if 'page' in querydict:
#         del querydict['page']
#     query_string = querydict.urlencode()

#     # 🔁 Fetch solved problems if user is authenticated
#     if request.user.is_authenticated:
#         fetch_solved_problems_for_user(request.user)
#         solved_ids = SolvedProblem.objects.filter(user=request.user).values_list('problem_id', flat=True)
#     else:
#         solved_ids = []

#     return render(request, 'practice/problem_list.html', {
#         'page_obj': page_obj,
#         'tags': tags,
#         'difficulties': difficulties,
#         'selected_tag': selected_tag,
#         'selected_diff': selected_diff,
#         'search_query': search_query,
#         'query_string': query_string,
#         'solved_ids': solved_ids,
#     })

