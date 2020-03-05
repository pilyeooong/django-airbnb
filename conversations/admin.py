from django.contrib import admin

from .models import Conversation
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    pass