from django.contrib import admin
from .models import Player, Comment
# Register your models here.

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'slug')
    list_filter = ('last_name',)
    prepopulated_fields = {'slug': ('last_name', 'first_name')}