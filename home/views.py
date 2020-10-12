from django.shortcuts import render
from core.models import Journal
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.
def home(request):
	following = request.user.profile.following.all()
	print(following)
	for i in following:
		journal = Journal.objects.filter(user=i).order_by('-timestamp')
	context = {'journal': journal}
	return render(request, 'home.html', context)