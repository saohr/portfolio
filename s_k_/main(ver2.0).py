# このファイルが実行ファイルです

import datetime
import webbrowser
import os
import raceID
from request import Keyget
import analyze
import re

# 現在の年度を取得
today = datetime.datetime.now()
current_year = today.year

def main1():
    # Runnning変数でwhile trueを実装
    Running = True
    while Running:
        # raceyearには基本的に西暦が入るが、メニュー0と8がある
        raceyear = input("【重賞結果検索メニュー】\n検索する年度の西暦を整数4桁で入力してください\n(2016年以降, データ分析[8], 終了[0]): ").strip()
        if raceyear == "0":
            break
        if raceyear == "8":        
            print("この処理には時間がかかることがあります。少々お待ちください。")
            print()
            main2()
        
        # isdigit()は入力されたものが数字のみで構成されているか判定する関数
        if not raceyear.isdigit() or not (2016 <= int(raceyear) <= current_year):
            print("その年度には対応していません")
            continue
        
        raceyear = int(raceyear)
        race_data, G1_data = raceID.get_racename_data(raceyear)
        
        while Running:
            racegrade = (input("検索したい重賞のグレードを整数値で入力してください（全重賞の確認は9）\nG1[1],G2[2],G3[3],年度の変更[7],データ分析へ[8],全重賞名確認[9],終了[0]: "))
            # Runningをfalseにすることで二重ループから一気に抜ける
            if racegrade == "0":
                Running = False
            elif racegrade == "7":
                print()
                main1()
                
            elif racegrade == "8":
                print("この処理には時間がかかることがあります。少々お待ちください。")
                print()
                main2()
                
                
            elif racegrade == "9":
                filename = f"race_list_{raceyear}.txt"
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(f"{raceyear}年度重賞一覧\n【G1】\n")
                    for race in G1_data:
                        file.write(race + "\n")
                    file.write("\n【G2・G3】\n")
                    for race in race_data.values():
                        file.write(race + "\n")
                print(f"レースリストを {filename} に保存しました。")
                os.system(f"notepad {filename}")
                continue
            
            # メイン処理
            elif racegrade in ["1", "2", "3"]:
                racegrade = int(racegrade)
                if racegrade == 1:
                    print("URLの構造が違うのでG1レースの検索には対応していません。")
                    print("代わりにG1レースの一覧を出力します")
                    for race in G1_data:
                        print(race)
                else:
                    racename = input("検索したい重賞名を入力してください: ").strip()
                    keyget_instance = Keyget(race_data, racegrade, racename)
                    racekey = keyget_instance.get_racekey()
                    if racekey:
                        webbrowser.open(f"https://www.jra.go.jp/datafile/seiseki/replay/{raceyear}/{racekey}.html")
                    else:
                        print("重賞のグレードが間違っているか、その年度に存在しない重賞名を入力されています。")
            else:
                print(f"グレード {racegrade} の重賞は存在しません。")


def main2():
    analyzer = analyze.RaceDataAnalyzer()
    maxSearchYear = current_year - 2016 - 1
    while True:
        select_analyze = input(f"【データ分析メニュー】\n[1]過去{maxSearchYear}年分のデータから検索する,\n[2]年度を指定して検索する,\n[0]終了する\nまとめて検索[1],年度指定[2],重賞検索へ[8],終了[0]: ").strip()
        
        if select_analyze == "0":
            break
        
        elif select_analyze == "8":
            print()
            main1()
            return
        
        elif select_analyze == "1":
            a = input("【まとめて検索:メニュー】\n[1]指定騎手の指定重賞の勝利回数を検索する,\n[2]レースを指定して指定騎手の同じコースの勝利回数を調べる,\n重賞名指定[1],同コース指定[2],やめる[その他]: ").strip()
            if a == "1":
                raceName = input("重賞名をグレード+名前で入力[例:G1ジャパンC]: ").strip()
                jockey = input("騎手名を入力[例:C.ルメール,福永祐一]: ").strip()
                result1 = analyzer.search_race_jockey(raceName, jockey)
                print("=" * 50)
                if not result1:
                    print(f"{jockey}は{raceName}を勝っていません")
                else:
                    analyze.print_result(result1)
            # 2の処理に関しては1とほとんど同じ
            # 安田記念と東京新聞杯、富士Sなど同コースを使った複数重賞がある場合のために使う
            elif a == "2":
                racename = input("重賞名をグレード+名前で入力[例:G1ジャパンC] : ").strip()
                jockey = input("騎手名を入力[例:C.ルメール,福永祐一]: ").strip()
                coursefinder = analyzer.get_distance_by_race(racename)
                result2 = analyzer.search_place_distance_jockey(racename,jockey)
                print("=" * 50)
                if not result2:
                    print(f"{jockey}は{coursefinder}の条件の重賞で勝っていません")
                else:
                    analyze.print_result(result2)
                
        elif select_analyze == "2":
            # 距離表記を '芝2,000メートル' のようにカンマ付きに変換
            def format_distance(dist):
                return re.sub(r'(\d{4})メートル', lambda m: f"{m.group(1)[:1]},{m.group(1)[1:]}メートル", dist)

            raceyear = input(f"検索する年度を西暦4桁で入力してください(2016年-{current_year - 1}年): ").strip()
            if not raceyear.isdigit() or not (2016 <= int(raceyear) < current_year):
                print("その年度には対応していません")
                continue
            raceyear = int(raceyear)
            b = input("【まとめて検索:メニュー】\n[1]騎手の距離別の勝利回数を検索する,\n[2]距離を指定してその条件で2鞍以上勝った騎手を勝ち鞍が多い順で表示,\n騎手から距離指定[1],芝ダ,距離から騎手[2],やめる[その他]: ").strip()
            if b == "1":
                jockey = input("騎手名を入力[例:W.ビュイック,横山武史]: ").strip()
                dist = input("距離条件を入力[例:芝2000メートル]: ").strip()
                # format_distanceで2000メートルを2,000メートルにする
                result3 = analyzer.search_year_jockey_distance(raceyear, jockey, format_distance(dist))
                print("=" * 50)
                if not result3:
                    print(f"{jockey}は、{dist}の重賞で勝っていません")
                else:
                    analyze.print_result(result3)
                    
            if b == "2":
                print("距離条件を入力後、その条件で2回以上勝った騎手を勝ち鞍の多い順に表示します")
                seldist = input("距離条件を入力[例:芝2000メートル]: ")

                result4 = analyzer.search_year_distance_jockeys(raceyear, format_distance(seldist), min_count=2)
                print("=" * 50)
                    # 2回以上勝った騎手がいないこともある
                if not result4:
                    print("該当する騎手が見つかりませんでした。")
                else:
                    analyze.print_result(result4)

try:
    # .stripでスペースや改行を削除
    select_main = input("【メインメニュー】\n半角数字で[]内のものを選んで入力してください。\n重賞結果検索[1],データ分析[2],終了[その他]: ").strip()
    if select_main == "1":
        print()
        main1()
    elif select_main == "2":
        print("この処理には時間がかかることがあります。少々お待ちください。")
        print()
        main2()
    else:
        print("プログラムを終了します")
except Exception as e:
    print(f"想定していないエラーが発生しました: {e}")
    print("プログラムを終了します")

