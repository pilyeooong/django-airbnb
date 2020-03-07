from django.contrib import admin

from .models import Conversation
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message Admin Definition """
    
    pass


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Admin Definition """
    
    pass