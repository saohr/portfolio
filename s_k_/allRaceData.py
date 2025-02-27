import requests
from bs4 import BeautifulSoup
import raceID

# raceIDを流用
# 全ての重賞名と開催場、距離、勝利騎手を求める
def get_allrace_data(raceyear):
    url = f"https://www.jra.go.jp/datafile/seiseki/replay/{raceyear}/jyusyo.html"
    response = requests.get(url)
    
    # ステータスコードが200番台だと成功。
    # それ以外だと失敗なので空の辞書を返す
    if response.status_code != 200:
        print("データを取得できませんでした。")
        return {}, {}
    
    soup = BeautifulSoup(response.content, "html.parser")
    element = soup.find("div", id="contentsBody")
    
    # エレメント（ページの要素）が空（取得が上手くできなかった）場合空の辞書を返す
    if not element:
        print("ページの構造が変わった可能性があります。")
        return {}, {}
    
    # エレメントの内容の確認
    # print(element)
    
    # 以下が変更部分
    
    racenames = []
    places = []
    distance = []
    jockeys = []
    
    # raceの列からデータを取り出す（中山金杯）
    td_racename_list = element.select("td.race")
    # placeの列からデータを取り出す（中山）
    td_place_list = element.select("td.place")
    # courseの列からデータを取り出す（芝1600m）
    td_racecourse_list = element.select("td.course")
    # jockeys（藤岡佑介）
    td_jockey_list = element.select("td.jockey")    
    
    # raceの名前をすべて取り出す
    racenames = [raceID.replace_roman_with_arabic(td.get_text(strip=True)) for td in td_racename_list]
    places = [td.get_text(strip=True) for td in td_place_list]
    distance = [td.get_text(strip=True) for td in td_racecourse_list]
    jockeys = [td.get_text(strip=True).replace("\u3000", "") for td in td_jockey_list]
    
    
    # 重賞名とコース、騎手
    return list(zip(racenames,places,distance,jockeys))
    
# 試験的にprintする
# print(get_allrace_data(raceyear=2019))