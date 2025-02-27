# このファイルが実行ファイルです
"""
動作
1.年度を入力
2.グレードを入力（グレードの入力が動作分岐になっているので以降ここでの入力内容をそれぞれ〇番という形で書きます）
以下グレードごとの動作
・9番_G1とそれ以外の重賞を分けてその年度のレースをすべて出力
・1番_G1はG2G3とHTMLの構造とurlが異なるので時間の都合上対応できませんでした。
  1番が選択された場合G1レース一覧が出力されます
・2,3番_指定された年度の指定重賞のjraの結果を開く
"""

import datetime
import webbrowser
from raceID import get_racename_data
from request import Keyget

raceyear = int(input("検索したい重賞の年度を教えてください: "))
current_year = datetime.datetime.now().year

if raceyear > current_year or raceyear < 2001:
    print("その年度には対応していません")
else:
    race_data, G1_data = get_racename_data(raceyear)
    racegrade = int(input("検索したい重賞のグレードを整数値で入力してください（全て表示は9）: "))
    
    if racegrade == 9:
        print("【G1レース】")
        for race in G1_data:
            print(race)
        print("\n【G2・G3レース】")
        for race in race_data.values():
            print(race)
    elif racegrade in [2, 3]:
        racename = input("検索したい重賞名を入力してください: ")
        keyget_instance = Keyget(race_data, racegrade, racename)
        racekey = keyget_instance.get_racekey()
        
        if racekey:
            webbrowser.open(f"https://www.jra.go.jp/datafile/seiseki/replay/{raceyear}/{racekey}.html")
        else:
            print("入力内容を確認してください。")
    elif racegrade == 1:
        print("【G1レース】")
        for race in G1_data:
            print(race)
    else:
        print(f"グレード{racegrade}の重賞は存在しません。")
