import random
from ai_handler import AIManager
from models import Bet

class MainController:
    """בקר ראשי המנהל את הלוגיקה של המשחק, האינטראקציה עם ה-AI וההימורים"""
    def __init__(self, player, wheel, db_manager):
        self.player = player
        self.wheel = wheel
        self.db = db_manager
        self.ai_manager = AIManager()

    def get_ai_insight(self, last_outcome=None):
        """מייצרת תובנה מהדילר (שימוש ב-AIManager)"""
        history = self.db.get_player_history(self.player.name, limit=5)
        return self.ai_manager.get_dealer_insight(
            self.player.name, 
            self.player.balance, 
            history, 
            last_outcome
        )

    def process_bet(self, bet_obj: Bet):
        """
        מעבדת הימור באמצעות פולימורפיזם (Polymorphism) מלא.
        נצמדת לארכיטקטורת MVC - ה-Controller מנהל לוגיקה בלבד ללא עיצוב.
        """
        # קבלת תוצאה מהגלגל
        roll_number, roll_color = self.wheel.spin()
        
        # שימוש פולימורפי במתודות האובייקט ללא קשר לסוגו הספציפי
        is_win = bet_obj.check_win(roll_number, roll_color)
        
        if is_win:
            payout = bet_obj.get_payout(bet_obj.amount)
            new_balance = self.player.balance + payout
            status = "WINNER"
        else:
            new_balance = self.player.balance - bet_obj.amount
            status = "LOST"

        # עדכון המודל (Encapsulation דרך setter)
        self.player.balance = new_balance
        self.db.update_balance(self.player.name, new_balance)

        # יצירת הודעת תוצאה נקייה (ללא קודי צבע - אחריות ה-View)
        result_msg = f"{status}! Result: {roll_number} {roll_color}."

        # שמירה להיסטוריה
        self.db.save_game(
            self.player.name, 
            bet_obj.amount, 
            result_msg, 
            type(bet_obj).__name__.replace('Bet', ''), 
            str(bet_obj.selection)
        )
        
        return result_msg
