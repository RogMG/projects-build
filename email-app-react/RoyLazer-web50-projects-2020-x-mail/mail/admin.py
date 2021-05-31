from django.contrib import admin
from .models import Email
# Register your models here.

class EmailUser(admin.ModelAdmin):
    list_display=("id","archived","read", "timestamp" ,"body", "subject", "sender", "user")


admin.site.register(Email, EmailUser)