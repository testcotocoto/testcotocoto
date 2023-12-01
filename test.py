from myapp.models import UserProfile
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
try:
    user_profile = UserProfile.objects.get(id=1)
    # オブジェクトが存在する場合の処理
except UserProfile.DoesNotExist:
    # オブジェクトが存在しない場合の処理
    pass
