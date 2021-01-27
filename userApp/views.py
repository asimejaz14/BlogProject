from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    title = 'Sign Up'
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            e_mail = form.cleaned_data.get('email')
            messages.success(request, 'Your account has been created, login in now.')

            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'userApp/register.html', context={'form': form,
                                                             'title': title})


@login_required
def profile(request):
    title = 'Profile'
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your data has been updated!')

            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'title': title,
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'userApp/profile.html', context=context)
