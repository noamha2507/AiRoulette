import random
from ai_handler import AIManager
from models import Bet

class MainController:
    ## MVC Architecture: Controller - הבקרה של המערכת
    ## מנהלת את הדיאלוג בין ה-Model (נתונים) ל-View (תצוגה)
    ## בקר ראשי לניהול לוגיקת המשחק (Controller)
    def __init__(self, player, wheel, db_manager):
        ## self: המופע של הקונטרולר שמנהל את הזרם של המשחק
        self.player = player
        self.wheel = wheel
        self.db = db_manager
        self.ai_manager = AIManager()

    def get_ai_insight(self, last_outcome=None):
        history = self.db.get_player_history(self.player.name, limit=5)
        return self.ai_manager.get_dealer_insight(
            self.player.name, 
            self.player.balance, 
            history, 
            last_outcome
        )

    def process_bet(self, bet_obj: Bet):
        ## ציר 3: פולימורפיזם (Polymorphism) - שיא העוצמה של OOP!
        ## הקונטרולר מקבל אובייקט ולא אכפת לו מה הסוג המדויק שלו (צבע, מספר וכו')
        ## הוא פשוט מפעיל את הממשק המשותף: bet_obj.check_win()
        ## Polymorphism: עיבוד הימור ללא תלות בסוגו הספציפי
        ## קבלת תוצאה מהגלגל
        roll_number, roll_color = self.wheel.spin()
        
        ## Polymorphism: שימוש במתודות האובייקט ללא קשר לסוגו
        is_win = bet_obj.check_win(roll_number, roll_color)
        
        if is_win:
            payout = bet_obj.get_payout(bet_obj.amount)
            new_balance = self.player.balance + payout
            status = "WINNER"
        else:
            new_balance = self.player.balance - bet_obj.amount
            status = "LOST"

        ## Encapsulation: עדכון המודל דרך ה-setter
        self.player.balance = new_balance
        self.db.update_balance(self.player.name, new_balance)

        ## יצירת הודעת תוצאה נקייה (ללא קודי צבע - אחריות ה-View)
        result_msg = f"{status}! Result: {roll_number} {roll_color}."

        ## שמירה להיסטוריה
        self.db.save_game(
            self.player.name, 
            bet_obj.amount, 
            result_msg, 
            type(bet_obj).__name__.replace('Bet', ''), 
            str(bet_obj.selection)
        )
        
        return result_msg
