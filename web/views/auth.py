from django.shortcuts import render, redirect

from rbac.utils.permission_injection import init_permission
from rbac.models import UserInfo
# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = UserInfo.objects.filter(username=username, password=password).first()

        if user_obj:
            request.session['is_login'] = True

            # inject permission to session
            init_permission(request, user_obj)

            return redirect('index')
        else:
            return redirect('login')


def index(request):

    return render(request, 'index.html')
