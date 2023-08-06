from django.db import models

def get_boolean_fields(m):
    return list(filter(lambda f:isinstance(f,models.BooleanField),m._meta.get_fields()))

def get_string_fields(m):
    return list(filter(lambda f:isinstance(f,(models.CharField,models.TextField)),m._meta.get_fields()))
