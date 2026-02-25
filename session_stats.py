## הפרדת תחומי אחריות (Separation of Concerns)
## לכידות גבוהה (High Cohesion): מחלקה זו אחראית אך ורק על ניהול הסטטיסטיקה של הסשן הנוכחי.
class SessionStats:
    def __init__(self):
        ## self: המופע שמרכז את הסטטיסטיקה של הסשן הנוכחי בלבד.
        self.total_bets = 0
        self.wins = 0
        self.history = []
        self.hot_numbers = {}

    def update(self, num, result_type):
        self.total_bets += 1
        if result_type == "WINNER":
            self.wins += 1
        self.history.append(num)
        self.hot_numbers[num] = self.hot_numbers.get(num, 0) + 1
    
    def get_win_rate(self):
        if self.total_bets == 0: return 0
        ## חישוב אחוז הצלחה כחלק מאחריות ניהול הנתונים של המחלקה.
        return (self.wins / self.total_bets) * 100

    def get_best_numbers(self):
        ## שליפת המספרים הנפוצים ביותר דרך מיון נתוני המופע.
        sorted_nums = sorted(self.hot_numbers.items(), key=lambda x: x[1], reverse=True)
        return [str(n[0]) for n in sorted_nums[:3]]
