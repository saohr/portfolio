import requests
from bs4 import BeautifulSoup

def replace_roman_with_arabic(text):
    roman_to_arabic = {"Ⅰ": "1", "Ⅱ": "2", "Ⅲ": "3"}
    for roman, arabic in roman_to_arabic.items():
        text = text.replace(roman, arabic)
    return text

def get_racename_data(raceyear):
    url = f"https://www.jra.go.jp/datafile/seiseki/replay/{raceyear}/jyusyo.html"
    response = requests.get(url)
    
    # ステータスコードが200番台だと成功。
    # それ以外だと失敗なので空の辞書を返す
    if response.status_code != 200:
        print("データを取得できませんでした。")
        return {}, {}
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # エレメント（ページの要素）が空（取得が上手くできなかった）場合空の辞書を返す
    element = soup.find("div", id="contentsBody")
    if not element:
        print("ページの構造が変わった可能性があります。")
        return {}, {}
    
    # エレメントの内容の確認
    # print(element)
    
    notG1races = []
    G1races = []
    td_race_list = element.select("td.race")
    for td in td_race_list:
        race_text = replace_roman_with_arabic(td.get_text(strip=True))
        if "G1" in race_text or "J・G1" in race_text:
            G1races.append(race_text)
        else:
            notG1races.append(race_text)
    
    # idBaseは例えば中山金杯のIDは「001」なのでそうなるように調整する。
    # idBase[zfill(指定した数に満たない桁の場合残りを0で埋める) for (001から行数文繰り返す)]
    idBase = [str(i).zfill(3) for i in range(1, len(notG1races) + 1)]
    
    return dict(zip(idBase, notG1races)),G1races