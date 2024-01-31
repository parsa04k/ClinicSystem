from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('you are not authorized to view this page')
        return wrapper
    return decorator

def employee_only(view_func):
    def wrapper(request, *args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'patient':
            pass
        
        if group == 'employee':
            return view_func(request, *args,**kwargs)
    return wrapper