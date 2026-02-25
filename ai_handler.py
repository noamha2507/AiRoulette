import random

try:
    from ollama import Client
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False

class AIManager:
    ## AI Agent: סוכן אינטליגנטי המנהל את הקשר עם ה-LLM
    ## משתמש בשרת אינפרנס מקומי (Ollama) כ"מוח" של המערכת
    ## ניהול הקשר עם ה-AI ותובנות הדילר (Separation of Concerns)
    def __init__(self, model_name="llama3.2:1b", host='http://127.0.0.1:11434'):
        ## self: המופע של מנהל ה-AI ששומר על הקשר עם השרת
        self.model_name = model_name
        if HAS_OLLAMA:
            self.client = Client(host=host)
        else:
            self.client = None
            
        self.fallbacks = [
            "The wheel is cold, but your luck might be heating up.",
            "Place your bets. Fortune favors the bold... usually.",
            "A gentleman always knows when to double down.",
            "The house always wins, but you're putting up a fight.",
            "Feel that? That's the sound of the ball deciding your fate.",
            "Is it a strategy, or just blind faith? I like it either way."
        ]

    def get_dealer_insight(self, player_name, balance, history, last_outcome=None):
        ## הענקת הקשר (Context): ה-AI מקבל את מצב השחקן וההיסטוריה כדי להפיק תובנה חכמה
        ## יצירת הערה ייחודית מהדילר לפי מצב השחקן
        wins = sum(1 for h in history if "WINNER" in h[3])
        losses = len(history) - wins
        
        context = f"Wins: {wins}, Losses: {losses}."
        if last_outcome: 
            context += f" Last result was a {last_outcome}."
        
        prompt = (f"You are 'The Dealer', a high-stakes Casino AI. "
                  f"Player: {player_name}. Balance: ${balance}. {context} "
                  f"Task: One witty, charismatic sentence (under 12 words) to the player. "
                  f"Be slightly provocative but encouraging. No internal monologue or quotes.")

        ## הגדרת גיבויים דינמיים למקרה ששרת ה-AI לא זמין
        ## Low Coupling: המערכת ממשיכה לתפקד גם ללא המוח המרכזי (Ollama)
        current_fallbacks = list(self.fallbacks)
        if balance < 200:
            current_fallbacks = ["Living on the edge, aren't we?", "One big win could change everything.", "Careful now, the vault is looking empty."]
        elif wins > 3:
            current_fallbacks = ["You're on fire! Don't let the wheel cool down.", "The pit boss is starting to sweat. Keep going."]
        elif losses > 3:
            current_fallbacks = ["Rough patch? The wheel owes you one.", "Statistics say you're due for a win. Probably."]
        
        ## הוספת גיוון רנדומלי מהרשימה הכללית כדי למנוע חזרתיות
        random.shuffle(current_fallbacks)

        try:
            ## ניסיון פנייה לשרת ה-Ollama המקומי
            if HAS_OLLAMA and self.client:
                response = self.client.generate(model=self.model_name, prompt=prompt)
                return response['response'].strip().split('\n')[0].replace('"', '')
            
            ## אם השרת לא זמין, השתמש באחד ממשפטי הגיבוי באופן רנדומלי
            return random.choice(current_fallbacks)
        except:
            ## במקרה של שגיאת תקשורת, חזרה לגיבוי
            return random.choice(current_fallbacks)
