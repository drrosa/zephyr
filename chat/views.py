from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import UpdateView, DeleteView
from django.db.models import Q
from .models import Conversation, Message, User
from .forms import MessageForm
from openai import OpenAI
import environ

env = environ.Env()
env.read_env()
client = OpenAI(api_key=env("OPENAI_API_KEY"))
LLM = User.objects.get(username="ChatGPT")
GPT_MODEL = env("GPT_MODEL")


@login_required
def home(request):
    message_thread = get_object_or_404(Conversation, topic_name="welcome")
    chat_messages = message_thread.chat_messages.all()[:30]
    form = MessageForm()

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.sender = request.user
            message.thread = message_thread
            message.save()
            get_chatgpt_response(request.POST["content"], message_thread)
            return redirect("home")

    return render(request, "home.html", {"chat_messages": chat_messages, "form": form})


def get_chatgpt_response(user_message, message_thread):
    try:
        system_message = """
        You are a helpful assistant.
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]

        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=messages,
        )
        msg_content = response.choices[0].message.content

        bot_message = Message(
            sender=LLM,
            content=msg_content,
            thread=message_thread,
        )
        bot_message.save()
    except Exception as e:
        print(f"Error in get_chatgpt_response: {e}")


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
        return qs.filter(Q(sender=self.request.user) | Q(sender=LLM))


class MessageDelete(DeleteView):
    model = Message
    success_url = "/"
