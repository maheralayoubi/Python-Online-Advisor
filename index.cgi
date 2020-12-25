#!/home/allonsy1124/.local/share/virtualenvs/online-advisor-bRJeH8N5/bin/python3.8
import sys, os
 
sys.path.insert(0, "/home/allonsy1124/.local/share/virtualenvs/online-advisor-bRJeH8N5/bin")
 
os.environ['DJANGO_SETTINGS_MODULE'] = "chat_django.settings"
 
from wsgiref.handlers import CGIHandler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
CGIHandler().run(application)
