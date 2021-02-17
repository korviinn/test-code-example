from django.conf import settings


# usual unittest skip decorator skip all test if see him
def skip_in_tests(obj):
    def wrapper(*args, **kwargs):
        if settings.IS_TESTING:
            return
        return obj(*args, **kwargs)

    return wrapper
