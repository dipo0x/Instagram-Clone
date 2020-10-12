from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProfileModelForm 
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

########  TO FOLLOW A USER ##############

@login_required
def follow_user(request, pk):
    user = get_object_or_404(User, id=request.POST.get('user_id'))
    following = False
    if user.profile.followers.filter(id=request.user.id).exists():
        user.profile.followers.remove(request.user)
        request.user.profile.following.remove(user)
        following = False
    else:
        user.profile.followers.add(request.user)
        request.user.profile.following.add(user)
        following = True 
    return HttpResponse("DONE!") 


def register(request):
    registered = False
    if request.method == "POST":
        user_form = RegistrationForm(request.POST or None, request.FILES or None)
        profile_form = ProfileModelForm(request.POST or None, request.FILES or None)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponse("success")

        else:
            user_form = RegistrationForm()
            profile_form = ProfileModelForm()

            return render(request, "reg_form.html",
                    {'user_form':RegistrationForm,
                           'profile_form':ProfileModelForm,
                           'registered':registered})

    form2 = ProfileModelForm
    form = RegistrationForm
    return render(request = request,
                  template_name = "reg_form.html",
                                 context={"form":form, "form2":form2 })


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):

########  TO KNOW THOSE I'M FOLLOWING #############

    those_following = request.user.profile.following.all()
    print(those_following)

########  TO KNOW IF I'M FOLLOWING OR NOT  ##############
    following = False
    if request.user.profile.followers.filter(id=request.user.id).exists():
        following = True

    context = {'user' : User.objects.get(username=request.user), 'following' : following, 'total_followers' : request.user.profile.followers.count(), 'those_following' : those_following}    
    return render(request, 'profile.html', context)