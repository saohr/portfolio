import datetime
import re
from collections import Counter
from allRaceData import get_allrace_data


def print_result(result):
    for key, value in result.items():
        print(f"{' '.join(key)}: {value}")
        
class RaceDataAnalyzer:
    def __init__(self):
        """ 2016年から現在の前年までのレースデータを取得 """
        current_year = datetime.datetime.now().year
        self.race_data = [race for year in range(2016, current_year) for race in get_allrace_data(year)]

    def filter_data(self, search_params):
        """
        任意のパラメータでレースデータをフィルタリング
        :param search_params: { "race": レース名, "place": 場所, "distance": 距離, "jockey": 騎手 }
        :return: フィルタリング後のレースデータ
        """
        return [
            (race, place, distance, jockey) for race, place, distance, jockey in self.race_data
            if all(search_params.get(k, v) == v for k, v in zip(["race", "place", "distance", "jockey"], (race, place, distance, jockey)) if search_params.get(k) is not None)
        ]

    def count_combinations(self, filtered_data, key_indices, min_count=1):
        """
        指定された要素の組み合わせの出現回数をカウント
        :param filtered_data: フィルタリング済みのレースデータ
        :param key_indices: カウント対象のインデックス（例: (1, 3) -> (場所, 騎手)）
        :param min_count: 最低出現回数（デフォルト: 1）
        :return: 出現回数の辞書
        """
        counter = Counter(tuple(data[i] for i in key_indices) for data in filtered_data)
        return {k: v for k, v in counter.items() if v >= min_count}

    def subcount_combinations(self, filtered_data, key_indices, min_count=1):
        """
        指定された要素の組み合わせの出現回数をカウント
        :param filtered_data: フィルタリング済みのレースデータ
        :param key_indices: カウント対象のインデックス（例: (0, 1) -> (レース名, 場所)）
        :param min_count: 最低出現回数（デフォルト: 1）
        :return: 出現回数の辞書
        """
        if not filtered_data:
            return {}
        # 組み合わせをタプルとして作成
        combinations = [tuple(data[i] for i in key_indices) for data in filtered_data]
        # 出現回数をカウント
        counter = Counter(combinations)
        # 指定回数以上出現する組み合わせを抽出
        result = {k: v for k, v in counter.items() if v >= min_count}
        # デバッグ
        # print(f"カウント結果: {result}")
        return result


    # 2016年から現在年度-1年までのレースと騎手の組み合わせ
    def search_race_jockey(self, selrace, seljock):
        filtered_data = self.filter_data({"race": selrace, "jockey": seljock}) 
        return self.count_combinations(filtered_data, (0, 3), min_count=1)
        

    # 下のsearch_place_distance_jockeyで使う
    def get_distance_by_race(self, race_name):
        # 重賞名から対応する場所と距離を取得
        # :param race_name: レース名
        # :return: (場所, 距離) のタプル（該当なしの場合 None）
        race_name = race_name.strip().lower()  # 前後の空白削除 & 小文字変換
        for race, place, distance, _ in self.race_data:
            if race.strip().lower() == race_name:
                return place.strip(), distance.strip()  # 前後の空白を削除して返す
        return None

    # 2016年から現在年度-1年までの（場所＋距離）と騎手の組み合わせ
    def search_place_distance_jockey(self, selrace, seljock):
        place_distance = self.get_distance_by_race(selrace)
        if place_distance is None:
            return f"レース {selrace} の場所と距離が見つかりません。"
        filtered_data = self.filter_data({"place": place_distance[0], "distance": place_distance[1], "jockey": seljock})
        return self.count_combinations(filtered_data, (1, 2, 3), min_count=1)

    # 指定年度での騎手と距離の組み合わせ 
    def search_year_jockey_distance(self, raceyear, jockey, dist):
        all_races = get_allrace_data(raceyear)
        filtered_races = [race for race in all_races if race[2] == dist and race[3] == jockey]
        result = self.subcount_combinations(filtered_races, (0, 1), min_count=1)
        return result
    
   # 指定年度ー騎手ー距離のデバッグ
    # def search_year_jockey_distance(self, raceyear, jockey, dist):
    #     """指定年度での騎手と距離の組み合わせ"""
    #     # データ取得
        # all_races = get_allrace_data(raceyear)
        
        # # デバッグ情報の表示
        # print(f"取得したレース数: {len(all_races)}")
        
        # # 条件に一致するレースをフィルタリング
        # filtered_races = [race for race in all_races if race[2] == dist and race[3] == jockey]
        
        # # デバッグ情報の表示
        # print(f"条件に一致するレース数: {len(filtered_races)}")
        # print(f"一致したレース: {filtered_races}")
        
        # # 結果をカウント（レース名と場所の組み合わせ）
        # result = self.subcount_combinations(filtered_races, (0, 1), min_count=1)
        
        # return result
        
    def search_year_distance_jockeys(self, raceyear, seldist, min_count=2):
        """ 指定年度で特定の距離において2回以上勝利した騎手を検索 """
        all_races = get_allrace_data(raceyear)
        winning_jockeys = [race[3] for race in all_races if race[2] == seldist]
        jockey_win_count = Counter(winning_jockeys)

        result = {
            jockey: count for jockey, count in sorted(jockey_win_count.items(), reverse=True)
            if count >= min_count
        }

        return result
    

# print(get_allrace_data(2019))
# def format_distance(dist):
#     """距離表記を '芝2,000メートル' のようにカンマ付きに変換"""
#     return re.sub(r'(\d{4})メートル', lambda m: f"{m.group(1)[:1]},{m.group(1)[1:]}メートル", dist)

# クラスのインスタンスを作成
# analyzer = RaceDataAnalyzer()
# メソッドを呼び出す
# dist =  format_distance("芝2000メートル")
# result = analyzer.search_year_jockey_distance(2019, "坂井瑠星",dist)
# print(result)