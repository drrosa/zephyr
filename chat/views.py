from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import UpdateView, DeleteView
from .models import Conversation, Message
from .forms import MessageForm


@login_required
def home(request):
    welcome_topic = get_object_or_404(Conversation, topic_name="welcome")
    chat_messages = welcome_topic.chat_messages.all()[:30]
    form = MessageForm()

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.sender = request.user
            message.thread = welcome_topic
            message.save()
            return redirect("home")

    return render(request, "home.html", {"chat_messages": chat_messages, "form": form})


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


class MessageEdit(UpdateView):
    model = Message
    fields = ("content",)
    template_name = "home.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        welcome_topic = get_object_or_404(Conversation, topic_name="welcome")
        chat_messages = welcome_topic.chat_messages.all()[:30]
        context["chat_messages"] = chat_messages
        context["form"] = MessageForm(instance=self.object)
        return context

    def get_queryset(self):
        """Limit messages to those owned by the request user."""
        qs = super().get_queryset()
        return qs.filter(sender=self.request.user)


class MessageDelete(DeleteView):
    model = Message
    success_url = "/"
