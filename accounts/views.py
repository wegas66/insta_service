from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.forms import LoginForm, SignUpForm, UserUpdateForm

User = get_user_model()


def login_page(request):
    """Страница для логина"""

    if request.user.is_authenticated:
        return redirect('main_app:home')
    if request.user.is_anonymous and request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_data = login_form.cleaned_data
            email = user_data['email']
            password = user_data['password']
            check_email = User.objects.filter(email=email).first()
            if check_email:
                auth_user = authenticate(request, email=email, password=password)
                if auth_user:
                    login(request, auth_user)
                    messages.success(request, 'Вы успешно вошли в систему!')
                    return redirect('main_app:home')
                else:
                    messages.error(request, 'Логин или пароль неправильные')
            else:
                messages.error(request, 'Пользователь с таким email не существует!')
    else:
        login_form = LoginForm()
    context = {
        'title': "Вход",
        'login_form': login_form,
    }
    return render(
        request,
        'accounts/login_page.html',
        context=context
    )


def signup_page(request):
    """Страница для регистрации"""

    if request.user.is_authenticated:
        return redirect('main_app:home')
    if request.user.is_anonymous and request.method == "POST":
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user_data = signup_form.cleaned_data
            email = user_data['email']
            check_email = User.objects.filter(email=email).first()
            if not check_email:
                password = user_data['password1']
                user = signup_form.save(commit=False)
                user.is_active = True
                user.set_password(password)
                user.save()
                # hello_sender.delay(email)
                messages.success(request, 'Вы успешно зарегистрировались! Теперь войдите в систему')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Пользователь с таким email уже существует!')
    else:
        signup_form = SignUpForm()
    context = {
        'title': "Регистрация",
        'signup_form': signup_form,
    }
    return render(
        request,
        'accounts/signup_page.html',
        context=context
    )


@login_required(login_url='accounts:login')
def logout_page(request):
    """Страница для выхода"""

    if request.method == "GET":
        logout(request)
        messages.success(request, 'Вы успешно вышли')
    else:
        messages.info(request, 'Метод POST не разрешен')
    return redirect('main_app:home')


@login_required(login_url='accounts:login')
def profile(request):
    """Страница для просмотра профиля"""

    context = {
        'title': "Мой профиль",
    }
    return render(
        request,
        'accounts/profile.html',
        context=context
    )


@login_required(login_url='accounts:login')
def userUpdate(request):
    """Страница для обновления профиля"""

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            valid_data = form.cleaned_data
            if valid_data['password1'] != valid_data['password2']:
                messages.error(request, 'Пароли не совпадают!')
                return redirect("accounts:update_profile")
            user = form.save(commit=False)
            new_password = valid_data['password1']
            if len(new_password) > 0:
                if len(new_password) < 8:
                    messages.error(request, 'Пароль не должен быть менее 8 символов!')
                    return redirect("accounts:update_profile")
                user.set_password(new_password)
            user.save()
            messages.success(request, 'Данные успешно изменены')
            update_session_auth_hash(request, user)
            return redirect("accounts:profile")
    else:
        initial_data = {
            "city": request.user.city,
            "language": request.user.language,
            'subscribed': request.user.subscribed
        }
        form = UserUpdateForm(initial=initial_data)
    context = {
        "form": form,
        "title": "Обновление профиля"
    }
    return render(
        request,
        'accounts/update_page.html',
        context=context
    )


@login_required(login_url='accounts:login')
def deleteAccount(request):
    if request.method != "POST":
        messages.info(request, 'Разрешен только POST запрос!')
        return redirect('accounts:profile')
    user = User.objects.get(pk=request.user.pk)
    user.delete()
    messages.success(request, 'Ваш аккаунт успешно удален!')
    return redirect('main_app:home')
