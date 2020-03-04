from django.contrib import admin
from .models import Prize,User
# Register your models here.



class prizeInfo(admin.TabularInline):
    model = Prize
    extra = 1


class prizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'num', 'content', 'url', 'img', 'puser', 'creatTime','usedTime','isUsed']
    search_fields = ['name']
    list_per_page = 10


class userAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'name', 'email', 'phone', 'pwd','isDelete']
    fields = ['name', 'email', 'phone', 'pwd','isDelete']
    search_fields = ['name']
    list_per_page = 10


admin.site.register(Prize,prizeAdmin)
admin.site.register(User,userAdmin)