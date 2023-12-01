from pydub import AudioSegment
from scipy.io import wavfile
import numpy as np
import requests

# M4Aファイルのパスを指定する
input_m4a_file = "/content/新規録音 4.m4a"

# M4AファイルをWAVに変換する
audio = AudioSegment.from_file(input_m4a_file, format="m4a")
output_wav_file = "/content/output.wav"
audio.export(output_wav_file, format="wav", parameters=["-ar", "11025"])

print("M4AファイルをWAVに変換しました。")

# WAVファイルの読み込み
sample_rate, data = wavfile.read(output_wav_file)

# サンプルレートを変換する
if sample_rate != 11025:
    # サンプルレートが一致しない場合、変換を行う
    duration = len(data) / float(sample_rate)
    num_output_samples = int(duration * 11025)
    data = np.interp(np.linspace(0, 1, num_output_samples, endpoint=False), np.linspace(0, 1, len(data), endpoint=False), data)

    # 新しいサンプルレートでWAVファイルを保存
    output_wav_file = "/content/output.wav"
    wavfile.write(output_wav_file, 11025, data.astype(np.int16))

    print("WAVファイルのサンプルレートを変換しました。")
else:
    print("サンプルレートは変換不要です。")

# APIキーとWAVファイルのパスを指定する
API_KEY = "weDasgKGI2Dgh_Fg-4LsaJJ6x72cDO2tkHDYcpe6L1k"
API_ENDPOINT = "https://api.webempath.net/v2/analyzeWav"

# WAVファイルをAPIに送信する
files = {'wav': open(output_wav_file, 'rb')}
data = {'apikey': API_KEY}

response = requests.post(API_ENDPOINT, files=files, data=data)

# レスポンスを処理する
if response.status_code == 200:
    print(response.text)
else:
    print("HTTP status {}".format(response.status_code))