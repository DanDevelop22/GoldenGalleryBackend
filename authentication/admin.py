from django.contrib import admin
from authentication.models import * 
# Register your models here.

@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ('id','email','is_active','is_staff')
    search_fields = ('email',)

@admin.register(Cuadro)
class Cuadro(admin.ModelAdmin):
    list_display = ('name','img')
