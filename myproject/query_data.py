import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# APIDataモデルをインポート
from myapp.models import APIData

# APIDataモデルから全てのデータを取得
all_data = APIData.objects.all()

# 取得したデータを表示
for data in all_data:
    print(f'ID: {data.id}')
    print(f'Calm Score: {data.calm_score}')
    print(f'Anger Score: {data.anger_score}')
    print(f'Joy Score: {data.joy_score}')
    print(f'Sorrow Score: {data.sorrow_score}')
    print(f'Energy Score: {data.energy_score}')
    print(f'Timestamp: {data.timestamp}')
    print('---')
