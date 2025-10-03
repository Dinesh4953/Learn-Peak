from django.shortcuts import render, redirect
from .forms import Register
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from practice.models import SolvedProblem, PracticeQuestions
from practice.views import fetch_solved_problems_for_user, problem_detail_solved
# Create your views here.
def register(request):
    if request.method == "POST":
        form  = Register(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}, your account has been created')
            return redirect('login')
    else:
        form  =  Register()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def solved_problems_view(request):
    solved_qs = SolvedProblem.objects.filter(user=request.user).select_related('problem')
    solved_problems = [entry.problem for entry in solved_qs]
    return render(request, 'users/solved_problems.html', {
        'solved_problems': solved_problems
    })



@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        
# With instance=request.user.profile
# By passing instance=..., you are telling Django:
# “Hey, instead of creating a new profile, update this existing profile (request.user.profile) with the submitted data.”


        old_handle = request.user.profile.codeforces_handle  
        # request.POST → submitted data
        # instance=request.user.profile → updates the existing profile of the currently logged-in user
        if form.is_valid():
            form.save()
            
            new_handle = request.user.profile.codeforces_handle
            if new_handle and new_handle != old_handle:
                fetch_solved_problems_for_user(request.user)
                
                
            return redirect('profile')  # Replace with your profile page name
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'users/edit_profile.html', {'form': form})

    
            
