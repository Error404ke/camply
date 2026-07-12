from django.shortcuts import redirect

def inbox_redirect(request):
    return redirect('chat:chat_home')

def notifications_redirect(request):
    return redirect('notify:notification_list')

def profile_redirect(request):
    return redirect('accounts:profile')
