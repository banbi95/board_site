from django.shortcuts import redirect
from django.urls import reverse


def redirect_to_home(request):

    return redirect("board/")

