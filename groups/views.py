from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def group_list(request):
    return render(request, 'groups/group_list.html')
