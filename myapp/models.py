from django.db import models
from django.contrib.auth.models import User
from django.db import models


from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class MyService:
    def get_user_emotion_scores(self, user_profile_id):
        historical_entry = UserProfile.objects.filter(pk=user_profile_id).historical.first()

        if historical_entry:
            calm_score = historical_entry.calm_score
            anger_score = historical_entry.anger_score
            joy_score = historical_entry.joy_score
            sorrow_score = historical_entry.sorrow_score
            energy_score = historical_entry.energy_score

            # これらのスコアを利用して何かを行う...
            return calm_score, anger_score, joy_score, sorrow_score, energy_score
        else:
            # 対応するユーザープロフィールが見つからなかった場合の処理
            return None
# ユーザープロフィールのモデル定義（既存のフィールドと変更履歴を追跡するフィールドを含む）
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    calm_score = models.FloatField(default=0)
    anger_score = models.FloatField(default=0)
    joy_score = models.FloatField(default=0)
    sorrow_score = models.FloatField(default=0)
    energy_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username


class UserAudio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='user_audios/')
    upload_datetime = models.DateTimeField(auto_now_add=True)  # アップロード日時を保存するフィールド

    def __str__(self):
        return self.audio_file.name

class APIData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anger_score = models.FloatField()
    calm_score = models.FloatField()
    energy_score = models.FloatField()
    joy_score = models.FloatField()
    sorrow_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)