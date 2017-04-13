from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='home_apps')
def home_apps(app_list):
    filtered_apps = []
    for app in app_list:
        if app['name'] in settings.HOME_APPS:
            filtered_apps.append(app)
    return filtered_apps
