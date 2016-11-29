from django.contrib import admin
from snippets.models import User, UsedBook, Request, ChatList

admin.site.register(User)
admin.site.register(UsedBook)
admin.site.register(Request)
admin.site.register(ChatList)

# Register your models here.
