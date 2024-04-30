from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Conversation


@login_required
def home(request):
    welcome_topic = get_object_or_404(Conversation, topic_name="welcome")
    chat_messages = welcome_topic.chat_messages.all()[:30]
    return render(request, "home.html", {"chat_messages": chat_messages})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            error_message = "Invalid signup. Try again!"
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)
