from django.contrib import admin
from clients.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """ Filed in admin panel """
    list_display = ('username', 'is_superuser', 'is_active')
    list_display_links = ('username',)
    search_fields = ('username',)
