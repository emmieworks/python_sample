import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

GOOGLE = "https://www.google.com/complete/search?hl=jp&output=toolbar&q="
# コマンドラインの引数の指定
# 第1引数：キーワード

# 関連キーワードを取得
def main(argv):
  keywords = [argv[1]]
  results = keywords
  keywords = get_suggested_keywords(keywords)
  results += keywords

  keywords = get_suggested_keywords(keywords)
  results += keywords

  output_csv = pd.DataFrame(
      results,
      columns=['Suggested Keywords'])
  output_csv.to_csv('suggestwords_'+ argv[1] + '.csv', index=False)

def get_suggested_keywords(keywords):
  result_keywords =[]
  for ky in keywords:
    url = GOOGLE+ky

    soup = BeautifulSoup(requests.get(url).content,'lxml') # bsでURL内を解析
    suggestions = soup.find_all('suggestion') # suggestion タグを取得

    count = 0
    for sg in suggestions:
      if count != 0:
        result_keywords.append(sg["data"])
      count += 1

  return result_keywords

if __name__ == '__main__':
  main(sys.argv)