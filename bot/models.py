from django.db import models
from smart_selects.db_fields import ChainedManyToManyField

# Create your models here.

class Group(models.Model):
        name = models.CharField(max_length=250, null=True, blank = True)
        description = models.TextField(null=True, blank = True)

        def __str__(self):
                return self.name

        class Meta:
                verbose_name = 'Группы устройств'
                verbose_name_plural = 'Группы устройств'

class Org(models.Model):
        name = models.CharField(max_length=250, null=True, blank = True)
        description = models.TextField(null=True, blank = True)

        def __str__(self):
                return self.name

        class Meta:
                verbose_name = 'Организации'
                verbose_name_plural = 'Организации'


class Case(models.Model):
	name = models.CharField(max_length=250)
	admin = models.BooleanField(default = False)
	script = models.CharField(max_length=250)
	group = models.ForeignKey(Group, on_delete = models.CASCADE)
	def __str__(self):
		return str(self.name)

	class Meta:
		verbose_name = 'Действия'
		verbose_name_plural = 'Действия'


class Target(models.Model):
	TYPE = (("-","-"),("ovpn-client","ovpn-client"),("ppp-client","ppp-client"),("pptp-client","pptp-client"),("sstp-client","sstp-client"))
	name = models.CharField(max_length=250)
	description = models.TextField()
	port = models.BigIntegerField(null=True, blank = True)
	ip = models.GenericIPAddressField(null=True, blank = True)
	group = models.ForeignKey(Group, on_delete = models.CASCADE)
	org = models.ManyToManyField(Org, null=True, blank = True)
	case = ChainedManyToManyField(Case, horizontal=True, chained_field='group', chained_model_field='group', blank=True, null=True)
	interface = models.CharField(max_length=250, null=True, blank = True)
	service = models.CharField(max_length=250, null=True, blank = True)
	cred = models.CharField(max_length=250, null=True, blank = True)
	vpntype = models.CharField(max_length = 20, choices = TYPE, default = '-')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Целевые системы и устройства'
		verbose_name_plural = 'Целевые системы и устройства'


class User(models.Model):
	chat_id = models.BigIntegerField()
	description = models.CharField(max_length=50, null=True, blank = True)
	username = models.CharField(max_length=120)
	fio = models.CharField(max_length=120, null=True, blank = True)
	is_admin = models.BooleanField(default = False)
	org = models.ManyToManyField(Org, null=True, blank = True)
	target = ChainedManyToManyField(Target, horizontal=True, chained_field='org', chained_model_field='org', blank=True, null=True)
	date_in = models.DateTimeField(auto_now_add = True, auto_now = False, null=True, blank = True)
	CurrentHost = models.CharField(max_length=250, null=True, blank = True)
	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name = 'Пользователи телеграмм'
		verbose_name_plural = 'Пользователи телеграмм'

class Log(models.Model):
	date = models.DateTimeField(auto_now_add = True, auto_now = False, null=True, blank = True)
	user = models.CharField(max_length=250, null=True, blank = True)
	log = models.CharField(max_length=250, null=True, blank = True)

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name = 'Логи'
		verbose_name_plural = 'Логи'

class Message(models.Model):
	date = models.DateTimeField(auto_now_add = True, auto_now = False, null=True, blank = True)
	chat_id = models.BigIntegerField()
	name = models.CharField(max_length=250, null=True, blank = True)
	organization = models.CharField(max_length=250, null=True, blank = True)
	contact = models.CharField(max_length=250, null=True, blank = True)
	message = models.CharField(max_length=5000, null=True, blank = True)
	step = models.CharField(max_length=250, null=True, blank = True)

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name = 'Сообщения'
		verbose_name_plural = 'Сообщения'
