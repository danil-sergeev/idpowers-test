import os

from django.core.wsgi import get_wsgi_application

#для продакшна

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

application = get_wsgi_application()