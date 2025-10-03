from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
import pdfkit
from users.models import Profile

@login_required
def accept(request):
    profile = request.user.profile
    if request.method == "POST":
        profile.name_cv = request.POST.get("name", "")
        profile.email_cv = request.POST.get("email", "")
        profile.phone = request.POST.get("phone", "")
        profile.summary = request.POST.get("summary", "")
        profile.degree = request.POST.get("degree", "")
        profile.school = request.POST.get("school", "")
        profile.university = request.POST.get("university", "")
        profile.previous_work = request.POST.get("previous_work", "")
        profile.skills = request.POST.get("skills", "")
        
        
        profile.save()
        template = loader.get_template("cv/cv.html")
        html = template.render({"user_profile": profile})

        options = {
            "page-size": "Letter",
            "encoding": "UTF-8",
        }
        path_wkhtmltopdf = r"D:\wkhtmltox-0.12.6-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdf = pdfkit.from_string(html, False, options=options, configuration=config)

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{request.user.username}_cv.pdf"'
        return response
    return render(request, 'cv/accept.html')

# def cv(request):
#     profile = request.user.profile
    
#     template = loader.get_template('cv/cv.html')
#     html = template.render({"user_profile": profile})
    
#     options = {
#         'page-size' : 'Letter',
#         'encoding' : 'UTF-8',
#     }
    
#     path_wkhtmltopdf =  r"D:\wkhtmltox-0.12.6-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe"
#     config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

#     pdf = pdfkit.from_string(html, False, options=options, configuration=config)
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{request.user.username}_cv.pdf"'
#     return response