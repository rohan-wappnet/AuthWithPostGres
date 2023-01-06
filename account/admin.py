from django.contrib import admin
from account.models import details
# Register your models here.

@admin.register(details)
class modelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "city",
        "phone"
    )