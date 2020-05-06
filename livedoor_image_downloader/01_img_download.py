import re
import os
import urllib.request
import urllib.error

current_url = "https://livedoor.blogimg.jp/zeroforest" # 現在のライブドアブログURL
img_url = current_url+'/*imgs/[\w/:%#\$&\?\(\)~\.=\+\-]+' # 画像のURLURL

file_name = "backup.txt" # 読み込むファイル名
dir_name = "images" # 画像保存先フォルダ名


def download_file(url, dst_path):
  try:
    with urllib.request.urlopen(url) as web_file:
      data = web_file.read()
      with open(dst_path, mode='wb') as local_file:
        local_file.write(data)
  except urllib.error.URLError as e:
    print(e)

images = [] # 画像URL格納

# backup.txtから、画像URL取得
with open(file_name, "r") as file_data:
  for line in file_data:
    url_list = re.findall(img_url, line)
    for url in url_list:
      images.append(url)

print(str(len(images))+"個の画像を取得します")

# 画像保存先フォルダがなければ作成する。
try:
  os.makedirs(dir_name)
except:
  pass

# 画像のダウンロード
for img in images:
  download_file(img, os.path.join(dir_name, os.path.basename(img)))