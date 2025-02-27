# このファイルが実行ファイルです
"""
動作
アップデート内容のバックアップはしようと思ったタイミングで保存しています

1.年度を入力
  update_対応できない年度を設定しました
2.グレードを入力（グレードの入力が動作分岐になっているので以降ここでの入力内容をそれぞれ〇番という形で書きます）
以下グレードごとの動作
・9番_G1とそれ以外の重賞を分けてその年度のレースをすべて出力
  update_レース一覧をtextファイルに出力できるようになりました。
・1番_G1はG2G3とHTMLの構造とurlが異なるので時間の都合上対応できませんでした。
  1番が選択された場合G1レース一覧が出力されます
・2,3番_指定された年度の指定重賞のjraの結果を開く
"""

import datetime
import webbrowser
import os
from raceID import get_racename_data
from request import Keyget

# 現在の年度を設定することで存在しないページへのアクセスを回避
current_year = datetime.datetime.now().year
raceyear = int(input("検索したい重賞の年度を西暦4桁で入力してください(2016年以降) : "))

if raceyear > current_year or raceyear < 2016:
    print("その年度には対応していません")
else:
    race_data, G1_data = get_racename_data(raceyear)
    racegrade = int(input("検索したい重賞のグレードを整数値で入力してください（重賞のグレードの確認は9）: "))
    
    if racegrade == 9:
        filename = f"race_list_{raceyear}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"このテキストは同様の検索をするたびに上書きされます\n{raceyear}年度重賞一覧\n【G1】\n")
            # raceに毎回G1_dataのvalue[i]を入れて、出力⇒上書きして出力を繰り返す
            for race in G1_data:
                    file.write(race + "\n")
                
            file.write("\n【G2・G3】\n")
            for race in race_data.values():
                file.write(race + "\n")
        # 既に同名のファイルがあっても上書きする
        print(f"レースリストを {filename} に保存しました。")
        # notepadで開く
        os.system(f"notepad {filename}")
        
        # racegradeに2,3が入力されたとき
    elif racegrade in [2, 3]:
        racename = input("検索したい重賞名を入力してください: ")
        keyget_instance = Keyget(race_data, racegrade, racename)
        racekey = keyget_instance.get_racekey()
        
        if racekey:
            webbrowser.open(f"https://www.jra.go.jp/datafile/seiseki/replay/{raceyear}/{racekey}.html")
        else:
            print("重賞のグレードが間違っているか、その年度に存在しない重賞名を入力されています。\n入力内容をご確認ください。")
    elif racegrade == 1:
        print("【G1レース】")
        for race in G1_data:
            print(race)
    else:
        print(f"グレード{racegrade}の重賞は存在しません。")
