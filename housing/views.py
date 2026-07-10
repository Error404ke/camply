from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def housing_list(request):
    return render(request, 'housing/housing_list.html')
