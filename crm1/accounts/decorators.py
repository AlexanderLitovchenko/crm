from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_finc):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_finc(request, *args, **kwargs)
	return wrapper_func

def allowed_users(allowed_roles = []):
	def decorator(view_finc):
		def wrapper_func(request, *args, **kwargs):
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			if group in allowed_roles:
				return view_finc(request, *args, **kwargs)
			else:
				return HttpResponse('You are not allowed to see this page')
		return wrapper_func
	return decorator

def admin_only(view_finc):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
		if group == 'customer':
			return redirect('user-page')
		if group == 'admin':
			return view_finc(request, *args, **kwargs)
	return wrapper_function

