from moshavere.models import Call
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

class FieldsMixin():
	def dispatch(self, request, *args, **kwargs):
		self.fields = [
			"name", "time_min", "category",
			"description", "phone", "sextype",
			"age", "status", "ptext" , "pstatus" , "ptime"
		]
		if request.user.is_superuser:
			self.fields.append("author")
		return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
	def form_valid(self, form):
		if self.request.user.is_superuser or self.request.user.is_supervisor:
			form.save()
		else:
			self.obj = form.save(commit=False)
			self.obj.author = self.request.user
			if not self.obj.status == 'i':
				self.obj.status = 'd'
		return super().form_valid(form)


class AuthorAccessMixin():
	def dispatch(self, request, pk, *args, **kwargs):
		call = get_object_or_404(Call, pk=pk)
		if call.author == request.user and call.status in ['b', 'd'] or\
		request.user.is_superuser or request.user.is_supervisor:
			return super().dispatch(request, *args, **kwargs)
		else:
			raise Http404("You can't see this page.")

class SupervisorAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser or request.user.is_author:
			return super().dispatch(request, *args, **kwargs)
		elif request.user.is_supervisor:
			raise Http404("You can't see this page.")

class AuthorsAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_superuser or request.user.is_author or request.user.is_supervisor:
				return super().dispatch(request, *args, **kwargs)
			else:
				return redirect("account:profile")
		else:
			return redirect("login")


class SuperUserAccessMixin():
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_superuser or request.user.is_supervisor:
			return super().dispatch(request, *args, **kwargs)
		else:
			raise Http404("You can't see this page.")