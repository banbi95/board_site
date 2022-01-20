from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from .forms import SignUpForm
from django.contrib.auth import login


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect(reverse('board:home'))
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


@method_decorator(login_required,name='dispatch')
class UserUpdateView(UpdateView):
    model=User
    fields=('first_name','last_name','email')
    template_name = 'accounts/my_account.html'
    success_url = reverse_lazy('board:home')

    def get_object(self, queryset=None):
        return self.request.user

