# JRAからスクレイピングしたデータに、入力したグレード・重賞名に一致するものがあるか調べる

class Keyget:
    def __init__(self, race_data, racegrade, racename):
        self.race_data = race_data
        self.racegrade = racegrade
        self.racename = racename

    def get_racekey(self):
        racegradePlus = "G" + str(self.racegrade)
        full_racename = racegradePlus + self.racename
        
        for key, value in self.race_data.items():
            if value == full_racename:
                return key
        print("該当するレースが見つかりません。")
        return None