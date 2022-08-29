from django.shortcuts import redirect


def user_is_vendor(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == "vendor":
                return redirect("vendor_app:home")
            else:
                return function(request, *args, **kwargs)

        else:
            return function(request, *args, **kwargs)
    return wrap