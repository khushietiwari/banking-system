from django.contrib.auth.decorators import user_passes_test

def employee_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='Employee').exists()
    )(view_func)

def admin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='Admin').exists()
    )(view_func)
