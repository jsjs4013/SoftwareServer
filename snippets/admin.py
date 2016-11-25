from django.contrib import admin
from snippets.models import User, UsedBook, Request

admin.site.register(User)
admin.site.register(UsedBook)
admin.site.register(Request)

# Register your models here.
