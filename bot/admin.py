from .config import TOKEN_BOT
from django.contrib import admin
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect

import telebot
import requests
from .config import TOKEN_BOT


# Register your models here.

from .models import *

class SendMessageForm(forms.Form):
	_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
	mesg = forms.CharField(label=u'', max_length=500, \
	widget=forms.Textarea(attrs={'rows':'10', 'cols': '70'}))


def send_message(modeladmin, request, queryset):
	form = None

	if 'apply' in request.POST:
		form = SendMessageForm(request.POST)

		if form.is_valid():
			mesg = form.cleaned_data['mesg']

		count = 0
		for item in queryset:
			bot = telebot.TeleBot(TOKEN_BOT)
			user_id = item.id
			Chat_ID = User.objects.get(pk=user_id).chat_id
			bot.send_message(Chat_ID, mesg)
			count += 1

		modeladmin.message_user(request, ("Сообщение отправлено %d пользователям." % count))
		return HttpResponseRedirect(request.get_full_path())

	if not form:
		form = SendMessageForm(initial={'_selected_action': request.POST.getlist(admin.helpers.ACTION_CHECKBOX_NAME)})
		return render(request, 'sendToUsers.html', {'items': queryset,'form': form, 'title':u'Отправить сообщение'})

send_message.short_description = "Send message via telegram"



class UserAdmin(admin.ModelAdmin):
	readonly_fields = ("chat_id","CurrentHost")
	list_display =  ("chat_id","fio","username","date_in","description","is_admin",)
	list_filter = ('org',)
	actions = [send_message]

class LogAdmin(admin.ModelAdmin):
	readonly_fields = ("id","date","user","log",)
	list_display = ("date","user","log",)
	list_filter = ('user','date',)

class MessageAdmin(admin.ModelAdmin):
	readonly_fields = ("date","chat_id","name","organization","contact","message","step",)
	list_display = ("date","chat_id","name","organization","contact","message",)
	list_filter = ('date','name','organization')

class CaseAdmin(admin.ModelAdmin):
	list_display = ("name","script","admin",)

class TargetAdmin(admin.ModelAdmin):
	list_display = ('visiblename','description','ip','port',)
	list_filter = ('org','group')

class GroupAdmin(admin.ModelAdmin):
        list_display = ('name','description',)

class OrgAdmin(admin.ModelAdmin):
        list_display = ('name','description',)


admin.site.register(User,UserAdmin)
admin.site.register(Target,TargetAdmin)
admin.site.register(Log,LogAdmin)
admin.site.register(Case,CaseAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Group,GroupAdmin)
admin.site.register(Org,OrgAdmin)
