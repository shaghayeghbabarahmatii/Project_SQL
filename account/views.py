from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from .models import User
from .forms import ProfileForm
from .mixins import (
	FieldsMixin,
	FormValidMixin,
	SuperUserAccessMixin,
	AuthorAccessMixin,
	AuthorsAccessMixin,
	SuperUserAccessMixin,
	SupervisorAccessMixin
)
from django.views.generic import (
	ListView,
	CreateView,
	UpdateView,
	DeleteView
)
from moshavere.models import Call
from django.db.models import Sum
from datetime import datetime, timedelta
from django.utils import timezone
from extensions.utils import jalali_tuple_converter , jalali_full_converter

tomanpermin = 200

# Create your views here.


class CallDashboard(AuthorsAccessMixin, ListView):
	template_name = "registration/dashboard.html"

	def get_queryset(self):
		global call_filter
		time_threshold = timezone.now() - timedelta(days=jalali_tuple_converter(timezone.now())[2])
		if self.request.user.is_superuser or self.request.user.is_supervisor:
			call_filter = Call.objects.all()
			return call_filter
		else:
			call_filter = Call.objects.filter(author=self.request.user).filter(created__gte=time_threshold)
			return call_filter

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['timenow'] = [timezone.now(),jalali_full_converter(timezone.now())]
		time_threshold = timezone.now() - timedelta(days=jalali_tuple_converter(timezone.now())[2])
		call_objects = call_filter.filter(status='p').filter(created__gte=time_threshold)
		countcall = call_objects.count()
		if countcall != 0:
			sumcall = call_objects.aggregate(sumcall=Sum('time_min')).get('sumcall')
			avgcall = sumcall/countcall
			context['data'] = [countcall,sumcall,("%.2f" %avgcall),sumcall*tomanpermin]
			users = User.objects.filter(is_author=True)
			userlist = []
			for user in users:
				usercall = call_objects.filter(author=user)
				passtime = usercall.aggregate(sumcall=Sum('time_min')).get('sumcall')
				if type(passtime) != type(1):
					passtime = 0
					userlist.append([user,passtime,0,0.0,0])
				else:
					userlist.append([user,passtime,usercall.count(),("%.1f" %(passtime/usercall.count())),passtime * tomanpermin])
			context['userlist'] = userlist
		return context
		
class CallList(AuthorsAccessMixin, ListView):
	template_name = "registration/home.html"

	def get_queryset(self):
		global call_filter
		time_threshold = timezone.now() - timedelta(days=jalali_tuple_converter(timezone.now())[2])
		if self.request.user.is_superuser or self.request.user.is_supervisor:
			call_filter = Call.objects.all()
			return call_filter
		else:
			call_filter = Call.objects.filter(author=self.request.user).filter(created__gte=time_threshold)
			return call_filter

class PeygiriList(AuthorsAccessMixin, ListView):
	template_name = "registration/peygiri.html"

	def get_queryset(self):
		global call_filter
		time_threshold = timezone.now() - timedelta(days=jalali_tuple_converter(timezone.now())[2])
		if self.request.user.is_superuser or self.request.user.is_supervisor:
			call_filter = Call.objects.all().filter(pstatus='w')
			return call_filter
class CallCreate(AuthorsAccessMixin,SupervisorAccessMixin, FormValidMixin, FieldsMixin, CreateView):
	model = Call
	template_name = "registration/call-create-update.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pagetitile'] = "افزودن تماس"
		return context


class CallUpdate(AuthorAccessMixin, FormValidMixin, FieldsMixin, UpdateView):
	model = Call
	template_name = "registration/call-create-update.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['pagetitile'] = "ویرایش تماس"
		return context


class CallDelete(SuperUserAccessMixin, DeleteView):
	model = Call
	success_url = reverse_lazy('account:home')
	template_name = "registration/call_confirm_delete.html"


class Profile(LoginRequiredMixin ,UpdateView):
	model = User
	template_name = "registration/profile.html"
	form_class = ProfileForm
	success_url = reverse_lazy("account:profile")

	def get_object(self):
		return User.objects.get(pk = self.request.user.pk)

	def get_form_kwargs(self):
		kwargs = super(Profile, self).get_form_kwargs()
		kwargs.update({
			'user': self.request.user
		})
		return kwargs


class Login(LoginView):
	def get_success_url(self):
		user = self.request.user

		if user.is_superuser or user.is_author or user.is_supervisor:
			return reverse_lazy("account:dashboard")
		else:
			return reverse_lazy("account:dashboard")

