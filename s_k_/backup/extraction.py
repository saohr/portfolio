# このファイルいらない気がする
from collections import Counter, defaultdict
from allRaceData import get_allrace_data

# 2016年～2024年のデータを取得
race_data = [race for year in range(2016, 2025) for race in get_allrace_data(year)]

def count_combinations(race_data, num=2, group_by="jockey", search_params=None):
    """
    指定された競馬レースデータから特定の要素の組み合わせの出現回数をカウントする

    :param race_data: [(レース名, 場所, 距離, 騎手)] のリスト
    :param num: 指定した回数以上のデータのみ出力
    :param group_by: "jockey" (騎手ごと) または "distance" (距離ごと) の出力方式
    :param search_params: { "jockey": "騎手名", "distance": "距離", "place": "場所", "race": "レース名" } でフィルタリング
    :return: 各組み合わせの出現回数
    """
    # データフィルタリング（辞書のキーごとに検索）
    if search_params:
        race_data = [
            (race, place, distance, jockey) for race, place, distance, jockey in race_data
            if all(search_params.get(k, v) == v for k, v in zip(["race", "place", "distance", "jockey"], (race, place, distance, jockey)) if search_params.get(k) is not None)
        ]

    # 各組み合わせのカウント
    counts = {
        "jockey_place": Counter((jockey, place) for _, place, _, jockey in race_data),
        "jockey_distance": Counter((jockey, distance) for _, _, distance, jockey in race_data),
        "race_jockey": Counter((race, jockey) for race, _, _, jockey in race_data),
    }

    # num回以上のデータのみ取得
    filtered_jockey_distance = {k: v for k, v in counts["jockey_distance"].items() if v >= num}

    # 出力データの整形
    grouped_data = defaultdict(list)
    for (jockey, distance), count in filtered_jockey_distance.items():
        if group_by == "jockey":
            grouped_data[jockey].append((distance, count))
        else:
            grouped_data[distance].append((jockey, count))

    return {
        "騎手と場所の組み合わせ": counts["jockey_place"],
        f"{num}回以上あった騎手と距離の組み合わせ": grouped_data,
        f"{num}回以上あったレース名と騎手の組み合わせ": {k: v for k, v in counts["race_jockey"].items() if v >= num}
    }

# ==== 【検索例】 ====
# search_params = {race, place, distance, jockey}
search_params = {"race":"小倉大賞典","jockey": "C.ルメール"}

count_result = count_combinations(race_data, num=2, group_by="jockey", search_params=search_params)

# 結果の表示
for category, data in count_result.items():
    print(f"\n{category}:")
    if isinstance(data, dict):
        for key, values in data.items():
            if isinstance(values, list):  # 騎手ごと or 距離ごとに出力
                print(f"{key}: {', '.join(f'{dist} ({cnt}回)' for dist, cnt in values)}")
            else:
                print(f"{key}: {values}回")
