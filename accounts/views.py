import uuid
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.email_senders import confirm_email
from accounts.forms import LoginForm, SignUpForm, UserUpdateForm
from payments.models import PaymentAccount

User = get_user_model()


def auth_page(request):
    """Страница для логина и регистрации"""

    if not request.user.is_anonymous:
        messages.info(request, 'Вы уже вошли в систему')
        return redirect("main_app:home")
    next_page = request.GET.get("next")
    signup_form = SignUpForm()
    login_form = LoginForm()
    context = {
        "title": "Вход и регистрация",
        "signup_form": signup_form,
        "login_form": login_form,
        "next_page": next_page
    }
    return render(
        request,
        "accounts/auth.html",
        context=context
    )


def login_user(request):
    """Обработчик логина"""

    if request.user.is_authenticated:
        messages.info(request, "Вы уже вошли в систему")
    if request.user.is_anonymous and request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_data = login_form.cleaned_data
            email = user_data['email']
            password = user_data['password']
            check_email = User.objects.filter(email=email).first()
            if check_email:
                if check_email.is_active:
                    auth_user = authenticate(request, email=email, password=password)
                    if auth_user:
                        login(request, auth_user)
                        messages.success(request, 'Вы успешно вошли в систему!')
                        next_page = request.POST.get("next")
                        if next_page:
                            return redirect(next_page)
                        return redirect('main_app:home')
                    else:
                        messages.error(request, 'Логин или пароль неправильные')
                        return redirect('accounts:auth')
                else:
                    messages.info(request, 'Ваш аккаунт не активен! Проверьте почту и активируйте её!')
            else:
                messages.error(request, 'Пользователь с таким email не существует!')
            return redirect('accounts:auth')
    return redirect('main_app:home')


def signup_user(request):
    """Обработчик регистрации"""

    if request.user.is_anonymous and request.method == "POST":
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user_data = signup_form.cleaned_data
            email = user_data['email']
            check_email = User.objects.filter(email=email).first()
            if not check_email:
                password = user_data['password1']
                user = signup_form.save(commit=False)
                user.set_password(password)
                user.is_active = True
                user.activate_token = str(uuid.uuid4())
                user.save()
                payment_acc = PaymentAccount(user=user, balance=300)
                payment_acc.save()

                # confirm = confirm_email(user.email, user.activate_token)
                # if not confirm:
                #     messages.error(request, 'Сообщение не отправлено! попробуйте снова!')
                #     return redirect('accounts:signup')
                messages.info(request, 'Подтвердите почту! Проверьте её(собщение может попасть в спам)')
                return redirect('main_app:home')
            else:
                messages.error(request, 'Пользователь с таким email уже существует!')
                return redirect("accounts:auth")
        messages.error(request, "Данные не валидны(возможно этот email уже существует либо пароли не совпадают либо пароль"
                                " слишком распостронён)")
        return redirect("accounts:auth")
    return redirect("main_app:home")


def verify(request, email, token):
    if not request.user.is_anonymous:
        messages.info(request, "Ваш аккаунт уже активен")
        return redirect("main_app:home")
    user = User.objects.filter(email=email).first()
    if not user:
        messages.error(request, 'Пользователь не существует!')
        return redirect("main_app:home")
    if user.is_active:
        messages.info(request, 'email уже подтверждён!')
        return redirect("main_app:home")
    if not user.activate_token:
        messages.info(request, "Аккаунт либо подтверждён либо не существует!")
        return redirect("main_app:home")
    if not str(user.activate_token) == str(token):
        messages.error(request, "Токены подтверждения не сопадают!")
        return redirect("main_app:home")
    user.is_active = True
    user.activate_token = None
    user.save()
    messages.success(request, 'Ваш email подтверждён! Войдите в аккаунт')
    return redirect('accounts:auth')


@login_required(login_url='accounts:auth')
def logout_user(request):
    """Страница для выхода"""

    if request.method == "GET":
        logout(request)
        messages.success(request, 'Вы успешно вышли')
    else:
        messages.info(request, 'Метод POST не разрешен')
    return redirect('main_app:home')


@login_required(login_url='accounts:login')
def profile(request):
    return render(
        request,
        'accounts/profile.html'
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
        form = UserUpdateForm()
    context = {
        "form": form,
        "title": "Обновление профиля"
    }
    return render(
        request,
        'accounts/update_page.html',
        context=context
    )
