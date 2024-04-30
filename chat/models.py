from django.db import models
from django.db.models import CASCADE, SET_NULL
from django.contrib.auth.models import User

MAX_TOPIC_NAME_LENGTH = 128


class Channel(models.Model):
    MAX_DESCRIPTION_LENGTH = 1024
    MAX_NAME_LENGTH = 64
    creator = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    channel_name = models.CharField(max_length=MAX_NAME_LENGTH)
    description = models.CharField(max_length=MAX_DESCRIPTION_LENGTH, default="")
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.channel_name


class Conversation(models.Model):
    channel = models.ForeignKey(Channel, on_delete=CASCADE)
    creator = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    topic_name = models.CharField(max_length=MAX_TOPIC_NAME_LENGTH)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.topic_name


class Message(models.Model):
    thread = models.ForeignKey(
        Conversation, related_name="chat_messages", on_delete=CASCADE
    )
    sender = models.ForeignKey(User, on_delete=CASCADE)
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    last_edit_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.thread.topic_name} - {self.sender.username}: {self.content}"

    class Meta:
        ordering = ("-date_sent",)
