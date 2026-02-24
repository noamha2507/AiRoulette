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
        
        # הגדרת צבעים להודעות מערכת
        self.GREEN = "\033[92m"
        self.RED = "\033[91m"
        self.CYAN = "\033[96m"
        self.GOLD = "\033[93m"
        self.RESET = "\033[0m"

    def get_ai_insight(self, last_outcome=None):
        """מייצרת תובנה מהדילר (שימוש ב-AIManager)"""
        history = self.db.get_player_history(self.player.name, limit=5)
        return self.ai_manager.get_dealer_insight(
            self.player.name, 
            self.player.get_balance(), 
            history, 
            last_outcome
        )

    def process_bet(self, bet_obj: Bet):
        """פולימורפיזם: מעבדת הימור לפי דרישות הסילבוס (check_win ו-get_payout)"""
        # קבלת תוצאה מהגלגל
        roll_number, roll_color = self.wheel.spin()
        
        # שימוש במתודות הפולימורפיות החדשות
        is_win = bet_obj.check_win(roll_number, roll_color)
        
        if is_win:
            payout = bet_obj.get_payout(bet_obj.amount)
            new_balance = self.player.get_balance() + payout
            result_msg = f"{self.GREEN}WINNER! Result: {roll_number} {roll_color}.{self.RESET}"
        else:
            new_balance = self.player.get_balance() - bet_obj.amount
            result_msg = f"{self.RED}LOST. Result: {roll_number} {roll_color}.{self.RESET}"

        # עדכון מאזן ושמירה
        self.player.set_balance(new_balance)
        self.db.update_balance(self.player.name, new_balance)

        # שמירה למסד הנתונים
        self.db.save_game(
            self.player.name, 
            bet_obj.amount, 
            result_msg, 
            type(bet_obj).__name__.replace('Bet', ''), 
            str(bet_obj.selection)
        )
        
        return result_msg
