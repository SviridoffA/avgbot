# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import telebot
import json
import requests
import importlib
from datetime import datetime, timedelta
from .models import *
from .config import TOKEN_BOT

def keyb():
	kb = telebot.types.ReplyKeyboardMarkup(True,False)
	return kb

def mainmenu(accs,trguser):
	kb = keyb()
	chkbuton = 0
	for i in trguser.target.all():
		kb.row(str(i))
		chkbuton += 1
	if accs < 1:
		kb = keyb()
		kb.row(u'Оставить обращение через телеграм')
		kb.row(u'В главное меню')
	elif chkbuton == 0:
		kb.row(u'Оставить обращение через телеграм')
		kb.row(u'В главное меню')
	kb.row(u'Наши контакты')
	return kb

def targetmenu(trgcases,trgservice):
	kb = keyb()
	chkbuton = 0
	for i in trgcases:
		rw = str(i)
		if 'службу' in rw or 'службы' in rw:
			kb.row(rw + ' ' + trgservice)
			chkbuton += 1
		else:
			kb.row(rw)
			chkbuton += 1
	if chkbuton == 0:
		kb.row(u'Оставить обращение через телеграм')
		kb.row(u'В главное меню')
	elif chkbuton > 0:
		kb.row(u'Назад')
	kb.row(u'Наши контакты')
	return kb

#BOT
@csrf_exempt
def bot(request):
	try:
		bot = telebot.TeleBot(TOKEN_BOT)
		data = json.loads(request.body.decode('utf-8'))
		if 'message' in data.keys():
			if 'text' in data['message'].keys():
				text = data['message']['text']
				chat_id = data["message"]["chat"]["id"]
				if chat_id == -1001425092968:
					return HttpResponse('ok')
				name = data["message"]["chat"]["first_name"]
			exist = User.objects.filter(chat_id=chat_id).count()
			msgexist = Message.objects.filter(chat_id=chat_id).count()
			if exist > 0:
				trguser = User.objects.get(chat_id=chat_id)
				trgets = [target.name for target in trguser.target.all()]
				caselist = [cases.name for cases in Case.objects.all()]
				accs = trguser.target.count()

#message steps
		def name_step(chat_id,msgid,text):
			Message.objects.filter(id=msgid).update(step='name')
			kb = keyb()
			kb.row(u'Отмена')
			mes = 'Введите пожалуйста ваше имя:'
			bot.send_message(chat_id, mes, reply_markup = kb)

		def org_step(chat_id,msgid,text):
			Message.objects.filter(id=msgid).update(name=text)
			Message.objects.filter(id=msgid).update(step='org')
			kb = keyb()
			kb.row(u'Отмена')
			mes = 'Введите пожулуйста название вашей организации:'
			bot.send_message(chat_id, mes, reply_markup = kb)

		def contact_step(chat_id,msgid,text):
			Message.objects.filter(id=msgid).update(organization=text)
			Message.objects.filter(id=msgid).update(step='contact')
			kb = keyb()
			kb.row(u'Отмена')
			mes = 'Какой способ связи приемлим для вас? Введите контакт и тип контакта, ' +\
				'например - email examp@exempl.com'
			bot.send_message(chat_id, mes, reply_markup = kb)

		def msg_step(chat_id,msgid,text):
			Message.objects.filter(id=msgid).update(step='msg')
			Message.objects.filter(id=msgid).update(contact=text)
			kb = keyb()
			kb.row(u'Отмена')
			mes = 'Кратко опишите ваш вопрос:'
			bot.send_message(chat_id, mes, reply_markup = kb)

		def end_step(chat_id,msgid,text):
			Message.objects.filter(id=msgid).update(step='end')
			Message.objects.filter(id=msgid).update(message=text)
			Message.objects.filter(date__lte=datetime.now()-timedelta(days=365)).delete()
			kb = mainmenu(accs,trguser)
			mes = 'Спасибо за обращение! Мы обязательно свяжемся свами в кратчайшие сроки'
			bot.send_message(chat_id, mes, reply_markup = kb)
			snd = Message.objects.get(id=msgid)
			bot.send_message(-1001425092968, 'Получено новое сообщение: \n' + 'TelegramID: ' + str(chat_id) + '\n' + \
							'Представился: ' + str(snd.name)  + '\n' + 'Способ связи: ' + str(snd.contact) + '\n' + \
							'Сообщение: \n' + str(snd.message) + '\n\n\n' + 'Свяжитесь с пользователем по указаному контакту!')


		if exist != 0 and text == 'В главное меню' or text == 'Назад':
			trguser = User.objects.get(chat_id=chat_id)
			accs = trguser.target.count()
			kb = mainmenu(accs,trguser)
			chkbuton = 0
			for i in trguser.target.all():
				chkbuton += 1
			if chkbuton > 0:
				mes = 'Доступные узлы и системы: '
			else:
				mes = 'В данный момент вам не назначено никаких прав, ожидайте! ' + '\n'\
					'Для обновления списка прав необходим нажать клавишу "В главное меню"' + '\n'\
					'Либо свяжитесь с нами выбрав соответсвующий пункт меню'
			bot.send_message(chat_id, mes, reply_markup = kb)
			return HttpResponse('ok')

#target menu
		if exist != 0 and text in trgets:
			usrmsg = Message.objects.filter(chat_id=chat_id).latest('id')
			m = Message.objects.get(id=usrmsg.id)
			if m.step == 'end':
				trg = Target.objects.get(name=text)
				trgcases = trg.case.all()
				trgservice = trg.service
				User.objects.filter(chat_id=chat_id).update(CurrentHost=trg.name)
				kb = targetmenu(trgcases,trgservice)
				if trg.case.count() == 0:
					mes = 'Для данного обьекта ещё не назначены действия'
				else:
					mes = 'Выберите действие для обьекта ' + text + ':'
				bot.send_message(chat_id, mes, reply_markup = kb)
				return HttpResponse('ok')

#case action
		if exist != 0 and text in caselist:
			usrmsg = Message.objects.filter(chat_id=chat_id).latest('id')
			m = Message.objects.get(id=usrmsg.id)
			if m.step == 'end':
				trg = Target.objects.get(name=trguser.CurrentHost)
				if text in [cases.name for cases in trg.case.all()]:
					script = trg.case.get(name=text).script
					act = importlib.import_module('bot.cases.' + script)
					result = int(act.action(trg))

					if result == 2:
						mess = "Пользователь %s \n %s \n поставил задачу - %s \n на узел - %s" % (trguser.username, trguser.fio, text, trguser.CurrentHost)
						mes = 'Задача ' + '"' + text + '"' + 'Выполнена успешно!!!'
						Log.objects.create(user=trguser.username,log=text + ' на узле ' + trguser.CurrentHost + ' - Успех')
					elif result == 1:
						mess = "Пользователь %s \n %s \n поставил задачу - %s \n на узел - %s \n Но задача уже выполнена и не требует действий." % (trguser.username, trguser.fio, text, trguser.CurrentHost)
						mes = 'Задача ' + '"' + text + '"' + ' уже выполнена для данного узла, и более не требует действий.'
						Log.objects.create(user=trguser.username,log=text + ' на узле ' + trguser.CurrentHost + ' - Уже выполнено')
					else:
						mess = "Пользователь %s \n %s \n поставил задачу - %s \n на узел - %s \n Но возникла ошибка!!" % (trguser.username, trguser.fio, text, trguser.CurrentHost)
						mes = 'Не удалось выполнить задание, просим связаться с нами по контактам ниже!'
						Log.objects.create(user=trguser.username,log=text + ' на узле ' + trguser.CurrentHost + ' - Ошибка')
					bot.send_message(-1001425092968, mess) 
				else:
					mes = 'Задача ' + '"' + text + '"' + ' не назначена на данный узел'
				bot.send_message(chat_id, mes)
				return HttpResponse('ok')

#message cancel
		if text == 'Отмена':
			if exist >0:
				kb = mainmenu(accs,trguser)
				mes = 'Пожалуйста, выберите действие: '
			else:
				kb = keyb()
				kb.row(u'Регистрация')
				kb.row(u'Наши контакты')
				mes = 'Отправка отменена..'
			Message.objects.filter(chat_id=chat_id).latest('id').delete()
			bot.send_message(chat_id, mes, reply_markup = kb)
			return HttpResponse('ok')

		if msgexist != 0:
			usrmsg = Message.objects.filter(chat_id=chat_id).latest('id')
			msgid = usrmsg.id
			m = Message.objects.get(id=msgid)
			if m.step == 'name':
				org_step(chat_id,msgid,text)
				return HttpResponse('ok')
			if m.step == 'org':
				contact_step(chat_id,msgid,text)
				return HttpResponse('ok')
			if m.step == 'contact':
				msg_step(chat_id,msgid,text)
				return HttpResponse('ok')
			if m.step == 'msg':
				end_step(chat_id,msgid,text)
				return HttpResponse('ok')

#start
		if text == '/start' or text == 'В главное меню':
			if exist == 0:
				mes = 'Здравствуйте' + ' ' + name + '! \n \n' + \
					'Мы рады приветсвовать вас. \nДля начала работы с ботом необходимо пройти регистрацию с помощью кнопки ниже. \n' + \
					'После чего, мы назначим вам все необходимые права. Как только всё будет готово, я уведомлю вас сообщением. \n \n' + \
					'Пожалуйста свяжитесь с нами если у вас возникают какие либо сложности. Наши контакты вы можете найти нажав соответсвующую кнопку ниже.' 
				kb = keyb()
				kb.row(u'Регистрация')
				kb.row(u'Наши контакты')
				bot.send_message(chat_id, mes, reply_markup = kb)
				return HttpResponse('ok')
			else:
				kb = mainmenu(accs,trguser)
				mes = 'Пожалуйста, выберите действие: '
				bot.send_message(chat_id, mes, reply_markup = kb)
				return HttpResponse('ok')

#registration
		if text == 'Регистрация':
			checkreg = User.objects.filter(chat_id=chat_id).count()
			if checkreg > 0:
				mes = 'Вы уже зарегистрированы в системе!'
				kb = mainmenu(accs,trguser)
				bot.send_message(chat_id, mes, reply_markup = kb)
				return HttpResponse('ok')
			else:
				mes = 'Спасибо' + ' ' + name + '! ' + 'Вы успешно зарегистрировались в системе. Ожидайте назначения необходимых прав. ' + \
				'По окончанию мы уведомим вас сообщением.'
				try:
					username = data["message"]["from"]["username"]
				except:
					username = "Empty"
				if username is None:
					username = "Empty"
				try:
					fio = data["message"]["from"]["first_name"] + u" " + data["message"]["from"]["last_name"]
				except:
					fio = "Empty"
				if fio is None:
					fio = "Empty"
				User.objects.create(chat_id=chat_id, fio=fio.encode('utf8'), username=username)
				kb = keyb()
				kb.row(u'Наши контакты')
				kb.row(u'В главное меню')
				bot.send_message(chat_id, mes, reply_markup = kb)
				bot.send_message(-1001425092968, 'Новая регистрация: \n' + 'TelegramID: ' + str(chat_id) + '\n' + \
					'Login: ' +  username + '\n' + 'ФИО: ' + fio + '\n' + \
					'Необходимо назначит права пользователю в админке по адресу https://avgbot.dc-01.ru/admin/ \n' + \
					'ссылка RDM - rdm://open?DataSource=4E82CB3F-54C8-4707-9BEC-3B09BB123E6F&Repository=00000000-0000-0000-0000-000000000000' + \
					'&Session=7c97022b-6183-4c76-b299-8c69043c5947')
				return HttpResponse('ok')
#contacts
		if text == 'Наши контакты':
			kb = keyb()
			kb.row(u'Оставить обращение через телеграм')
			kb.row(u'В главное меню')
			mes = 'C нами можно связаться по следующим номерам: \n \n \n' + \
				'Техническая поддержка: \n \n    +7 (499)677-64-38 \n \n' + \
				'Отдел продаж: \n \n    +7 (499) 677-14-98 \n \n' + \
				'Либо же напишите нам на email: help@avangardpc.ru \n \n \n' + \
				'Также можете оставить нам своё обращение через телеграмм нажав на кнопку ниже.'
			bot.send_message(chat_id, mes, reply_markup = kb)
			return HttpResponse('ok')

#message throgh telegram
		if text == 'Оставить обращение через телеграм':
			Message.objects.create(chat_id=chat_id, step='name')
			usrmsg = Message.objects.filter(chat_id=chat_id).latest('id')
			msgid = usrmsg.id
			name_step(chat_id,msgid,text)
			return HttpResponse('ok')

		else:
			mes = 'Не могу опознать команду' + ' ' + '"' + text + '"'  + ', ' + 'либо у вас недостаточно прав для этого действия. ' + \
				' Просим связаться с нами' + \
				' указаными ниже способами.'
			kb = keyb()
			kb.row(u'Наши контакты')
			kb.row(u'В главное меню')
			bot.send_message(chat_id, mes, reply_markup = kb)
			return HttpResponse('Alive!!')

	except Exception as e:
                bot.send_message(324248972, str(e))
                return HttpResponse('Alive!!')

