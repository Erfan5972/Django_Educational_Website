from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserEditProfileForm, UserOtpCodeForm
from .models import User, UserOtpCode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from utils import send_otp_code
from .models import Subscription


class UserRegisterView(View):
    form_class = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(phone_number=cd['phone_number'])
            if user.exists():
                messages.error(request, 'کاربری با این اطلاعات وجود دارد', 'danger')
                return redirect('accounts:user-register')
            else:
                random_code = random.randint(1000, 9999)
                print(random_code)
                UserOtpCode.objects.create(code=random_code, phone_number=cd['phone_number'])
                items = {
                    'phone_number': str(cd['phone_number']),
                    'full_name': cd['full_name'],
                    'password': cd['password1'],
                }
                request.session['user_registration_info'] = items
                send_otp_code(str(cd['phone_number']), code=random_code)
                messages.success(request, 'کد تایید برای شما ارسال شد', 'success')
                return redirect('accounts:user-otp-verify')
        return render(request, 'accounts/register.html', {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, username=phone_number, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'خوش آمدید!')
                return redirect('home:home')
            else:
                messages.error(request, 'شماره تلفن یا رمز شما اشتباه است!', 'danger')
                return redirect('accounts:user-login')
        else:
            return render(request, 'accounts/login.html', {'form': form})


class UserSendOtpCode(View):
    def get(self, request):
        form = UserOtpCodeForm()
        return render(request, 'accounts/otpcode.html', {'form': form})

    def post(self, request):
        form = UserOtpCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_session = request.session.get('user_registration_info')

            if user_session is None:
                messages.error(request, 'اطلاعات ثبت نام کاربر یافت نشد', 'danger')
                return redirect('accounts:user-register')

            otp_codes = UserOtpCode.objects.filter(phone_number=user_session.get('phone_number'))
            if otp_codes.exists():
                otp_code = otp_codes.first()

                if cd['code'] == int(otp_code.code):
                    User.objects.create_user(phone_number=user_session.get('phone_number'),
                                             full_name=user_session.get('full_name'),
                                             password=user_session.get('password'))
                    otp_code.delete()
                    messages.success(request, 'شما با موفقیت ثبت نام شدید', 'success')
                    return redirect('home:home')
                else:
                    messages.error(request, 'کد وارد شده صحیح نمی باشد', 'danger')
                    return redirect('accounts:user-otp-verify')
            else:
                messages.error(request, 'کد تایید یافت نشد', 'danger')
                return redirect('accounts:user-otp-verify')
        return render(request, 'accounts/otpcode.html', {'form': form})


class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.success(request, 'شما با موفقیت خارج شدید', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        return render(request, 'accounts/profile.html', {'user': user})


class UserEditProfileView(LoginRequiredMixin, View):
    form_class = UserEditProfileForm

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        form = self.form_class(initial={
            'phone_number': user.phone_number,
            'full_name': user.full_name
        })
        return render(request, 'accounts/edit-profile.html', {'user': user, 'form': form})

    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        form = self.form_class(request.POST)
        if form.is_valid():
            user.phone_number = form.cleaned_data['phone_number']
            user.full_name = form.cleaned_data['full_name']

            if form.cleaned_data['password1']:
                user.set_password(form.cleaned_data['password1'])

            user.save()
            messages.success(request, 'اطلاعات شما با موفقیت ویرایش شد', 'success')
            return redirect('home:home')
        else:
            return render(request, 'accounts/edit-profile.html', {'user': user, 'form': form})


class SubscriptionView(View):
    def get(self, request):
        subscriptions = Subscription.objects.all()
        return render(request, 'accounts/subscription.html', context={'subscriptions': subscriptions})