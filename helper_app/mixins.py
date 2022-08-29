from django.contrib.auth.mixins import AccessMixin
from helper_app.models import User
from django.core.exceptions import PermissionDenied




class VendorRequiredMixin(AccessMixin):
    permission_denied_message = "Register as a speaker to create class."
    
    def dispatch(self, request, *args, **kwargs):
        if User.objects.filter(user=request.user,user__user_type = "vendor"):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied(self.permission_denied_message)
