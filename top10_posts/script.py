import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse
import csv
GOOGLE = "https://www.google.com/search?q="
# top10のtitle h1 h2 h3をcsv吐き出し
# コマンドラインの引数の指定
# 第1引数：キーワード
# https://katsuhiroblog.com/google-search-result-scraping/

#置換用
def replace_n(str_data):
    return str_data.replace('\n', '').replace('\r', '')

#文字列用
def concat_list(list_data):
    str_data = ''
    for j in range(len(list_data)):
        str_data = str_data + replace_n(list_data[j].getText()).strip() + '\n\n'
    return str_data.rstrip("\n")

# 関連キーワードを取得
def main(argv):
  keywords = argv[1]
  output_data = []
  columns=['順位','URL','Title','h1','h2','h3']
  output_data.append(columns)

  google_url = GOOGLE+keywords
  output_tmp_data = []

  soup = BeautifulSoup(requests.get(google_url).content,'lxml') # bsでURL内を解析
  # print(soup.prettify())
  tags = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')
  i = 0
  for tag in tags:
    tag_parent = tag.parent
    site_url = tag_parent.get('href').split('&sa=U&')[0].replace('/url?q=', '')
    site_url = urllib.parse.unquote(urllib.parse.unquote(site_url))
    print(site_url)

    if 'https://' in site_url or 'http://' in site_url:
      #サイトの内容を解析
      try:
          res_site = requests.get(site_url)
          res_site.encoding = 'utf-8'
      except:
        continue
      bs4_site = BeautifulSoup(res_site.text, 'html.parser')

      #データを初期化
      title_site = ''
      h1_site = ''
      h2_site = ''
      h3_site = ''

      #データを取得
      if bs4_site.select('title'):
          title_site = replace_n(bs4_site.select('title')[0].getText())
      if bs4_site.select('h1'):
          h1_site = concat_list(bs4_site.select('h1'))
      if bs4_site.select('h2'):
          h2_site = concat_list(bs4_site.select('h2'))
      if bs4_site.select('h3'):
          h3_site = concat_list(bs4_site.select('h3'))

      #データをリストに入れておく
      output_data_new = i+1, site_url, title_site, h1_site, h2_site, h3_site
      output_data.append(output_data_new)
      #print(output_data_new)
      i += 1

  # print(output_data)

  # データの書き出し
  with open('Top10Posts_'+ keywords + '.csv', "w", encoding="utf-8") as f: # 文字コードをShift_JISに指定
    writer = csv.writer(f, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
    writer.writerows(output_data) # csvファイルに書き込み

if __name__ == '__main__':
  main(sys.argv)