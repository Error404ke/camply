from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def chat_home(request):
    return render(request, 'chat/chat_home.html')
