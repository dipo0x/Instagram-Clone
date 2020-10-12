from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Journal
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import login, authenticate, logout
from core.forms import JournalModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts.models import Profile

# Create your views here.

########  TO SEE THE INFO OF ANOTHER USER ##############

@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)
    jn = Journal.objects.filter(user=user).order_by('-timestamp')

    ########  TO KNOW IF I'M FOLLOWING THE USER ##############

    following = False
    if user.profile.followers.filter(id=request.user.id).exists():
        following = True

########  TO KNOW THOSE I'M FOLLOWING #############

    those_following = user.profile.following.all()

    context = locals()
    context2 =  {'jn':jn, 'following': following }
    template = 'other_user.html'
    return render (request, template, context, context2)


def journal_list_view(request):

    template_name = 'journal.html'
    jn = Journal.objects.order_by("-timestamp")

    journal = Journal.objects.filter()
    context = {'journal': jn}
    return render(request, template_name, context)


@login_required
def journal_create_view(request):
    form = JournalModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.Country = request.user.profile.location
        obj.slug = "uhfugnrgurgn"
        obj.profile_pix = request.user.profile.image
        return redirect('/journal/')
        form = JournalModelForm()
    template_name = 'add_post.html'
    context = {'form': form}
    return render(request, template_name, context)  


@login_required
def journal_detail_view(request, slug):
    instance = get_object_or_404(Journal, slug=slug)

    initial_data = {
        'content_type':instance.get_content_type,
        'object_id': instance.id,
    }

    print("I've seen : " + instance.Your_Post_Title)

    context = {'journal' : instance}

    return render(request, 'journal_detail.html', context)