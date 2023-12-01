import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject/myproject/settings.py')  # myproject.settings はあなたのプロジェクトの設定ファイルのパスに置き換える

application = get_wsgi_application()
