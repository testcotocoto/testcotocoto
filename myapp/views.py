import os
from datetime import date
import buffer
from django.contrib.auth import authenticate, login
from django.urls import path
from scipy.io import wavfile
import numpy as np
import requests
from pydub import AudioSegment
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from django.contrib.auth.decorators import user_passes_test
from myapp.users.forms import UserRegistrationForm
from .models import UserAudio
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import font_manager
from django.core.files.base import ContentFile
from matplotlib.font_manager import FontProperties
from django.http import HttpResponse
import matplotlib.pyplot as plt
from io import BytesIO
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import TemplateView #テンプレートタグ
from django.db import models
from django.contrib.auth.models import User


# ログイン・ログアウト処理に利用
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from matplotlib.font_manager import FontProperties
# フォントプロパティを指定してプロットする
font_path = '/Users/cocoo/cocoo_empath_test/myproject/venv/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/ipaexg.ttf'  # 代替のフォントを指定します
plt.rcParams['font.family'] = 'IPAexGothic'

# MatplotlibのバックエンドをAggに設定する
import matplotlib

matplotlib.use('Agg')


#
from django.http import HttpResponse
from pydub import AudioSegment
from scipy.io import wavfile
import numpy as np
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
temp_file_path = os.path.join(settings.BASE_DIR, 'temp.m4a')
output_wav_file = os.path.join(BASE_DIR, 'user_audios/wav/output.wav')



def home(request):
    # ここにビューロジックを追加
    return render(request, 'home.html')

def about(request):
    # ここに'about'ページのビューロジックを追加
    return render(request, 'about.html')

from .forms import UserRegistrationForm

def result(request):
    return render(request, 'result.html')
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # ユーザーを保存
            login(request, user)  # ユーザーをログイン状態にする
            return redirect('home')  # ユーザーをホームページにリダイレクト
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # ユーザーオブジェクトを作成
        user = User.objects.create_user(username=username, email=email, password=password)

        # UserProfileオブジェクトを作成
        UserProfile.objects.create(user=user)

        # ユーザーの作成が成功した場合の処理
        return redirect('login')  # ログインページにリダイレクト

    return render(request, 'register.html')  # 登録フォームを表示


def login_not_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return csrf_exempt(wrapped_view)


def send_audio_to_api(wav_file_path):
    # Web Empath API のキーとエンドポイントを設定する
    API_KEY = 'weDasgKGI2Dgh_Fg-4LsaJJ6x72cDO2tkHDYcpe6L1k'
    API_ENDPOINT = 'https://api.webempath.net/v2/analyzeWav'

    # WAV ファイルを API に送信する
    files = {'wav': open(wav_file_path, 'rb')}
    data = {'apikey': API_KEY}

    response = requests.post(API_ENDPOINT, files=files, data=data)
    return response

import io
import tempfile


def convert_m4a_to_wav(m4a_file):
    # M4AファイルをWAVに変換
    audio = AudioSegment.from_file(m4a_file, format="m4a")

    # サンプルレートを変換する（必要であれば）
    if audio.frame_rate != 11025:
        audio = audio.set_frame_rate(11025)

    # メディアフォルダ内のwavディレクトリに保存する例
    media_root = settings.MEDIA_ROOT
    wav_directory = os.path.join(media_root, 'wav')  # wavディレクトリのパスを取得

    # wavディレクトリが存在しない場合は作成
    os.makedirs(wav_directory, exist_ok=True)

    # WAVファイルとして保存（wavディレクトリ内に保存する例）
    output_wav_file = os.path.join(wav_directory, 'output.wav')
    audio.export(output_wav_file, format="wav")

    return output_wav_file


@login_required(login_url='login')
def upload(request):
    if request.method == 'GET':
        # GETリクエストに対する処理を行う（フォームを表示する）

        return render(request, 'upload.html')
    elif request.method == 'POST' and request.FILES.get('audio_file'):

        try:

            user = request.user
            audio_file = request.FILES['audio_file']

            # M4AファイルをWAVに変換する
            temp_wav_file_path = convert_m4a_to_wav(audio_file)

            # WAVファイルをAPIに送信する
            api_response = send_audio_to_api(temp_wav_file_path)

            if api_response.status_code == 200:
                # レーダーチャートのデータを生成
                radar_chart_data = process_api_result(api_response.json(), user)

                # テンプレートに渡すデータを辞書に設定
                context = {
                    'radar_chart_data': radar_chart_data,
                }

                return render(request, 'result.html', context)

            else:
                print(f'APIエラー: {api_response.status_code}')
                return render(request, 'upload.html', {'error': 'APIエラーが発生しました。再度お試しください。'})

        except Exception as e:
            print(f'エラー: {e}')


            return render(request, 'upload.html', {'error': 'アップロードに失敗しました。再度お試しください。'})

    return HttpResponse("Invalid Request")

def process_api_result(api_result, user):
    # APIのレスポンスをそのままユーザープロフィールに保存する
    user_profile = UserProfile.objects.get(user=user)
    user_profile.calm_score = api_result.get('calm', 0)
    user_profile.anger_score = api_result.get('anger', 0)
    user_profile.joy_score = api_result.get('joy', 0)
    user_profile.sorrow_score = api_result.get('sorrow', 0)
    user_profile.energy_score = api_result.get('energy', 0)
    user_profile.save()  # ユーザープロフィールを保存する

    # レーダーチャートのデータをそのまま返す
    radar_chart_data = {
        'labels': ['Calm', 'Anger', 'Joy', 'Sorrow', 'Energy'],
        'data': [user_profile.calm_score, user_profile.anger_score, user_profile.joy_score,
                 user_profile.sorrow_score, user_profile.energy_score]
    }

    # プロセス後の値を確認するためにprint文を追加

    return radar_chart_data






from .models import User
from .models import UserProfile
from django.shortcuts import render, redirect


@login_not_required
# レーダーチャートを描画する関数
def plot_emotion_radar_chart(emotion_scores):

    categories = emotion_scores['labels']
    values = emotion_scores['data']

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    # レーダーチャートを描画
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color='b', linewidth=2, linestyle='solid')
    ax.fill(angles, values, color='b', alpha=0.4)

    # カテゴリラベルを日本語に設定する
    translated_categories = ["冷静", "怒り", "喜び", "悲しみ", "元気さ"]
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(translated_categories, fontproperties=FontProperties(fname=font_path))

    # レーダーチャートの最大値を設定する（適宜調整）
    ax.set_yticks([0, 10, 20, 30, 40, 50])
    ax.set_ylim(0, 50)

    # レーダーチャートのタイトルを設定する
    plt.title('感情レーダーチャート', size=20, color='b', y=1.1,
              fontproperties=font_manager.FontProperties(fname=font_path))

    # 画像をBytesIOに保存
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # 画像データをBase64エンコード
    image_data = base64.b64encode(buffer.getvalue()).decode()

    return image_data

from io import BytesIO
import base64



@login_required
def radar_chart_view(request):
    # ユーザー情報を取得
    user = request.user
    current_time = datetime.now()

    # ユーザーの感情スコアやAPIから受け取った感情データを取得するロジックを追加
    calm_normalized = user.profile.calm_score  # ユーザーの穏やかさの感情スコア
    anger_normalized = user.profile.anger_score  # ユーザーの怒りの感情スコア
    joy_normalized = user.profile.joy_score  # ユーザーの喜びの感情スコア
    sorrow_normalized = user.profile.sorrow_score  # ユーザーの悲しみの感情スコア
    energy_normalized = user.profile.energy_score  # ユーザーのエネルギーの感情スコア

    # ここにAPIからデータを取得する処理を追加
    api_response = send_audio_to_api(output_wav_file)  # APIからデータを取得する関数（例: send_audio_to_api）を呼び出す
    if api_response.status_code == 200:
        api_data = api_response.json()

        # APIのレスポンスを適切に処理するロジックを追加する
        api_calm_score = api_data.get('calm', 0)
        api_anger_score = api_data.get('anger', 0)
        api_joy_score = api_data.get('joy', 0)
        api_sorrow_score = api_data.get('sorrow', 0)
        api_energy_score = api_data.get('energy', 0)

        # APIDataモデルのインスタンスを作成
        api_data_instance = APIData(
            calm=calm_normalized,
            anger=anger_normalized,
            joy=joy_normalized,
            sorrow=sorrow_normalized,
            energy=energy_normalized,
            api_calm_score=api_calm_score,
            api_anger_score=api_anger_score,
            api_joy_score=api_joy_score,
            api_sorrow_score=api_sorrow_score,
            api_energy_score=api_energy_score,
            timestamp=current_time
        )

        # データベースに保存
        api_data_instance.save()

        # レーダーチャートのデータを生成
        emotion_scores = {
            "calm": calm_normalized,
            "anger": anger_normalized,
            "joy": joy_normalized,
            "sorrow": sorrow_normalized,
            "energy": energy_normalized,
            "API Calm": api_calm_score,
            "API Anger": api_anger_score,
            "API Joy": api_joy_score,
            "API Sorrow": api_sorrow_score,
            "API Energy": api_energy_score,
        }

        # レーダーチャートのデータを生成する関数を呼び出し、日本語のカテゴリラベルを設定
        radar_chart_data = plot_emotion_radar_chart(emotion_scores)

        # テンプレートにユーザー情報とレーダーチャートのデータを渡す
        context = {
            'user': user,
            'radar_chart_data': radar_chart_data,  # レーダーチャートのデータをセット
            'current_time': current_time,
        }

        return render(request, 'radar_chart.html', context)
    else:
        print(f'APIエラー: {api_response.status_code}')
        return HttpResponse('APIエラーが発生しました。再度お試しください。')

from django.http import JsonResponse
from .models import APIData
from .utils import send_request_to_api


def save_api_data(request):
    # APIからデータを取得するロジックを呼び出す（仮定の関数名）
    api_data = send_request_to_api()

    # データベースに保存
    APIData.objects.create(
        calm_score=api_data.get('calm', 0),
        anger_score=api_data.get('anger', 0),
        joy_score=api_data.get('joy', 0),
        sorrow_score=api_data.get('sorrow', 0),
        energy_score=api_data.get('energy', 0)
    )

    return JsonResponse({'message': 'Data saved successfully.'})

def daily_emotion_scores(request):
    # ユーザー名を取得
    user_profile = UserProfile.objects.get(user=request.user)
    username = user_profile.user.username

    # 特定の日付（10/6）以降の過去50件のデータを取得
    some_date = date(2023, 10, 6)  # 特定の日付を設定
    data = APIData.objects.filter(user=request.user, created_at__date__gte=some_date).order_by('-created_at')[:50]

    # ユーザーごとの毎日の感情スコアデータを取得
    api_data = APIData.objects.filter(user=request.user)

    # daily_emotion_scores.html テンプレートに渡すコンテキストを作成
    context = {
        'username': username,
        'data': data,  # 特定の日付（10/6）以降の過去50件のデータ
        'api_data': api_data,  # ユーザーごとの毎日の感情スコアデータ
    }

    # daily_emotion_scores.html テンプレートを使用してデータを表示
    return render(request, 'daily_emotion_scores.html', context)



def audio_list_by_date(request):
    # 現在の日付を取得
    current_date = date.today()

    # 当日にアップロードされた音声データを取得
    audio_data = UserAudio.objects.filter(upload_datetime__date=current_date)

    return render(request, 'audio_list_by_date.html', {'audio_data': audio_data})


def your_view(request):
    now = datetime.now()
    context = {
        'user': request.user,
        'now': now,
        # 他のコンテキスト変数を追加
    }
    return render(request, 'your_template.html', context)