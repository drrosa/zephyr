from django.contrib import admin
from .models import Channel, Conversation, Message

admin.site.register([Channel, Conversation, Message])
