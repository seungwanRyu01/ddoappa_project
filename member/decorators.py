from django.shortcuts import redirect
from .models import User


def login_required(func):
    def wrapper(req, *args, **kwargs):
        login_session = req.session.get('id', '')

        if login_session == '':
            return redirect('../login/')

        return func(req, *args, **kwargs)
    
    return wrapper