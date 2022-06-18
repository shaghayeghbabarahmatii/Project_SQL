from django.db import models
from django.urls import reverse
from account.models import User
from django.utils import timezone
from extensions.utils import jalali_converter


class CallManager(models.Manager):
	def published(self):
		return self.filter(status='p')


# Create your models here.


class Call(models.Model):
    SUBJECT_CHOICES = [
    ('روانشناسی', (
        ('RZO', 'زوج و خانواده'),
        ('RKO', 'کودک'),
        ('RNO', 'نوجوان'),
        ('REK', 'اختلالات روانی'),
        ('RET', 'اعتیاد'),
        ('RFA', 'روانشناسی فردی'),
    )),
    ('تحصیلی', (
        ('TMA', 'مدارس'),
        ('TKO', 'کنکور سراسری'),
        ('TBE', 'دانشگاه های بدون آزمون'),
        ('TKA', 'کارشناسی ارشد'),
        ('TDR', 'دکتری'),
        ('TAZ', 'آزمون زبان'),
        ('TAE', 'آزمون استخدامی'),
        ('TAA', 'سایر آزمون ها '),
    )),
    ('حقوقی', (
        ('HKH', 'خانواده'),
        ('HGH', 'عقود و قرارداد ها'),
        ('HHO', 'حقوقی'),
        ('HKE', 'کیفری'),
        ('HTE', 'تجاری'),
        ('HDA', 'آیین دادرسی'),
        ('HMA', 'مراجع حقوقی'),
        ('HAH', 'آزمون های حقوقی '),
    )),
    ]
    GENDER_CHOICES = [('f','زن'),('m','مرد')]
    STATUS_CHOICES = (
		('d', 'پیش‌نویس'),		 # draft
		('i', "در حال بررسی"),	 # investigation
		('p', "تایید شده"),		 # publish
		('b', "رد شده"), # back
	)
    PSTATUS_CHOICES = (
        ('w','درحال پیگیری'),
        ('a','پیگیری انجام شد'),
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='calls', verbose_name="مشاور")
    category = models.CharField(max_length=3, choices=SUBJECT_CHOICES, verbose_name="موضوع تماس",blank=True)
    time_min = models.PositiveSmallIntegerField(default=0,verbose_name='مدت تماس')
    name = models.CharField(max_length=50 ,blank=True, verbose_name='نام')
    sextype = models.CharField(max_length=1,choices=GENDER_CHOICES,verbose_name='جنسیت',blank=True)
    age= models.PositiveSmallIntegerField(blank=True, null=True ,verbose_name='سن')
    phone = models.CharField(max_length=11 ,blank=True, verbose_name='شماره تماس')
    description = models.TextField(verbose_name='توضیحات',blank=True)
    created = models.DateTimeField(auto_now_add=True,verbose_name='زمان ثبت')
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت",default='d')
    ptime = models.DateTimeField(verbose_name='زمان پیگیری',blank=True,default=timezone.now)
    pstatus = models.CharField(null=True,blank=True,max_length=1, choices=PSTATUS_CHOICES, verbose_name="وضعیت پیگیری")
    ptext = models.TextField(null=True,blank=True,verbose_name='توضیحات پیگیری')

    class Meta:
        verbose_name='تماس'
        verbose_name_plural = 'تماس ها'
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse("account:home")

    def jcreated(self):
        return jalali_converter(self.created)
    jcreated.short_description = 'زمان ثبت'

    def jptime(self):
        return jalali_converter(self.ptime)


    def __str__(self):
        return self.phone