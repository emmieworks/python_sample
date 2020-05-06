import re
import os

current_url = "https://livedoor.blogimg.jp/zeroforest" # 現在のHPのURL
new_url = "http://sample.local" # 新しいHPのURL
img_dir_path = "/wp-content/uploads/images/" #WordPressの画像アップロードファイル
img_pattern = current_url+r'/*imgs/[\w/:%#\$&\?\(\)~\.=\+\-]+'

original_file_path = "./backup.txt" # ファイル名
new_file_path ="./backup_updated.txt" #更新後のファイル

new_lines = ''

with open(original_file_path, "r") as f:

    for line in f:
      # TAGをTAGSに変換
      line = re.sub("TAG: ","TAGS: ",line)

      # 画像URLをWordPressの画像アップロード先に変更
      img_url_list = re.findall(img_pattern, line)
      for image_url in img_url_list:
        line = re.sub(image_url,new_url+img_dir_path+os.path.basename(image_url),line)

      # 記事状態を下書きに変更
      line = re.sub("STATUS: Publish","STATUS: Draft",line)

      # 旧URLを親URLに変更
      line = re.sub(current_url,new_url,line)

      # パーマリンクから.htmlを削除
      #if(re.match(r'PATH: ', line)):
      #  print(line)
      #  line = re.sub(r'.html$','',line)

      new_lines += line

with open(new_file_path, mode='w', encoding='utf-8') as f:
  f.writelines(new_lines)