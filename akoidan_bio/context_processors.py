__author__ = 'andrew'

def create_login_out_page(request):
    """
    adds to context navbar page with login action or username
    """
    c = {}
    if request.user.is_authenticated():
        page = 'akoidan_bio/logout.html'
        c.update({'username': request.user.login})
    else:
        page = 'akoidan_bio/registerAndLogin.html'
    c.update({'log_in_out_page': page})
    return c