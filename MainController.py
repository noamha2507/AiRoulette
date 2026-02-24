import random
try:
    from ollama import Client
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False

class MainController:
    """בקר ראשי המנהל את הלוגיקה של המשחק, האינטראקציה עם ה-AI וההימורים"""
    def __init__(self, player, wheel, db_manager):
        self.player = player
        self.wheel = wheel
        self.db = db_manager
        self.model_name = "llama3.2:1b"
        if HAS_OLLAMA:
            self.client = Client(host='http://127.0.0.1:11434')
        else:
            self.client = None
        
        # הגדרת צבעים להודעות מערכת
        self.GREEN = "\033[92m"
        self.RED = "\033[91m"
        self.CYAN = "\033[96m"
        self.RESET = "\033[0m"

    def get_ai_insight(self, last_outcome=None):
        """מייצרת תובנה מהדילר (AI) או משתמשת בגיבוי חכם אם השרת לא זמין"""
        try:
            history = self.db.get_player_history(self.player.name, limit=5)
            wins = sum(1 for h in history if "WINNER" in h[3])
            losses = len(history) - wins
            balance = self.player.get_balance()
            
            # בניית הקשר עבור ה-AI
            context = f"Wins: {wins}, Losses: {losses}."
            if last_outcome: context += f" Last result was a {last_outcome}."
            
            prompt = (f"You are 'The Dealer', a high-stakes Casino AI. "
                      f"Player: {self.player.name}. Balance: ${balance}. {context} "
                      f"Task: One witty, charismatic sentence (under 12 words) to the player. "
                      f"Be slightly provocative but encouraging. No internal monologue or quotes.")
            
            # רשימת משפטי גיבוי (Fallbacks) לפי מצב השחקן
            fallbacks = [
                "The wheel is cold, but your luck might be heating up.",
                "Place your bets. Fortune favors the bold... usually.",
                "A gentleman always knows when to double down.",
                "The house always wins, but you're putting up a fight.",
                "Feel that? That's the sound of the ball deciding your fate.",
                "Is it a strategy, or just blind faith? I like it either way."
            ]
            
            # התאמת משפטי הגיבוי למצב הכספי והביצועים
            if balance < 200:
                fallbacks = ["Living on the edge, aren't we?", "One big win could change everything.", "Careful now, the vault is looking empty."]
            elif wins > 3:
                fallbacks = ["You're on fire! Don't let the wheel cool down.", "The pit boss is starting to sweat. Keep going.", "Is this skill, or are you just luckier than most?"]
            elif losses > 3:
                fallbacks = ["Rough patch? The wheel owes you one.", "Statistics say you're due for a win. Probably.", "Don't let them see you blink. Bet big."]

            try:
                # ניסיון פנייה למודל Ollama
                if self.client:
                    response = self.client.generate(model=self.model_name, prompt=prompt)
                    comment = response['response'].strip().split('\n')[0].replace('"', '')
                    return comment
                else:
                    return random.choice(fallbacks)
            except:
                # חזרה לגיבוי אקראי במקרה של שגיאת תקשורת
                return random.choice(fallbacks)
        except:
            return "Place your bets! The wheel is hungry."

    def process_bet(self, bet_type, selection, amount):
        """מעבדת את ההימור: מחשבת תוצאה, מעדכנת מאזן ושומרת להיסטוריה"""
        # קבלת תוצאה מהגלגל
        roll_number, roll_color = self.wheel.spin()
        win = False
        
        # חישוב זכייה לפי סוג ההימור
        if bet_type == "number":
            win = (int(selection) == roll_number)
            payout = amount * 35
        elif bet_type == "color":
            win = (selection.capitalize() == roll_color)
            payout = amount
        elif bet_type == "even_odd":
            is_even = (roll_number % 2 == 0 and roll_number != 0)
            win = (selection.lower() == "even" and is_even) or (selection.lower() == "odd" and not is_even and roll_number != 0)
            payout = amount

        # בניית הודעת תוצאה ועדכון המאזן
        if win:
            new_balance = self.player.get_balance() + payout
            result_msg = f"{self.GREEN}WINNER! Result: {roll_number} {roll_color}.{self.RESET}"
        else:
            new_balance = self.player.get_balance() - amount
            result_msg = f"{self.RED}LOST. Result: {roll_number} {roll_color}.{self.RESET}"

        # שמירה למסד הנתונים ועדכון אובייקט השחקן
        self.player.set_balance(new_balance)
        self.db.update_balance(self.player.name, new_balance)
        self.db.save_game(self.player.name, amount, result_msg, bet_type.capitalize(), str(selection))
        
        return result_msg
