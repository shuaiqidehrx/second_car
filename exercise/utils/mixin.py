from django.contrib.auth.decorators import login_required

class LoginRequired(object):

    @classmethod
    def as_view(cls,**initkwargs):
        view = super(LoginRequired, cls).as_view(**initkwargs)
        return login_required(view)