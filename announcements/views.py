from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def announcement_list(request):
    return render(request, 'announcements/announcement_list.html')
