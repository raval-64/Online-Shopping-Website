from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import UserForm, MobileForm

# Create your views here.
def login_user(request):
    request.session.modified = True
    if not request.user.is_authenticated:
        next_url = request.GET.get('next')
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if next_url:
                        print('next_url')
                        return redirect(next_url)
                    else:
                        return redirect('/')
                else:
                    error = {'error_message': 'Your account has been disabled'}
                    return render(request, 'userauth/login.html', error)
            else:
                error = {'error_message': 'Invaild Username or Password'}
                return render(request, 'userauth/login.html', error)
        return render(request, 'userauth/login.html')
    else:
        return redirect('/')


def logout_user(request):
    request.session.modified = True
    logout(request)
    return redirect('/')


def register(request):
    request.session.modified = True
    if not request.user.is_authenticated:
        next_url = request.POST.get('next')
        u_form = UserForm(request.POST or None)
        m_form = MobileForm(request.POST or None)
        if u_form.is_valid() and m_form.is_valid():
            user_f = u_form.save(commit=False)
            mobile = m_form.save(commit=False)
            username = u_form.cleaned_data['username']
            password = u_form.cleaned_data['password']
            user_f.set_password(password)
            user_f.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    mobile.m_id = request.user
                    print(request.user)
                    mobile.save()
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('/')
        context = {'u_form': u_form, 'm_form': m_form}
        return render(request, 'userauth/reg.html', context)
    else:
        return redirect('/')

