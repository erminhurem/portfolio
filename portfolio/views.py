from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from .models import Project, GithubProject
from .chatbot import PortfolioChatbot

def index(request):
    projects = Project.objects.all()
    github_projects = GithubProject.objects.all()
    return render(request, 'portfolio/index.html', {'projects': projects, 'github_projects': github_projects})

def contact(request):
    if request.method == 'POST':
        if 'message' in request.POST and 'chatbot' in request.POST:
            # Handle chatbot request
            chatbot = PortfolioChatbot()
            response = chatbot.get_response(request.POST['message'])
            return JsonResponse({'response': response})
        
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Prepare email content
        email_subject = f"Portfolio Contact: {subject}"
        email_message = f"""
        New contact form submission from your portfolio:
        
        Name: {name}
        Email: {email}
        Subject: {subject}
        
        Message:
        {message}
        """
        
        try:
            # Send email
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        except Exception as e:
            messages.error(request, 'An error occurred while sending your message. Please try again later.')
            return redirect('contact')
    
    return render(request, 'portfolio/contact.html')



