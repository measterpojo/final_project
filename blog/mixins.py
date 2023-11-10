
from django.http.response import Http404
from core.utils import is_site_admin

class UpdateArticleMixin(object):

    def has_permission(self):
        return self.get_object().author == self.request.user
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            raise Http404('You are not owner')
        return super(UpdateArticleMixin, self).dispatch(request, *args, **kwargs)
    

class AdminMixin(object):

    def has_permission(self):
        return bool(
            is_site_admin(self.request.user)
        )
    
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            raise Http404('You do not have permission to create Category')
        return super(AdminMixin, self).dispatch(request, *args, **kwargs)