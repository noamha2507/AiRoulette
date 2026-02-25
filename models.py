import random
from abc import ABC, abstractmethod

## MVC Architecture: Model - שכבת הנתונים והלוגיקה העסקית

class Player:
    ## OOP: מחלקה (Class) - תבנית מופשטת לייצוג שחקן
    ## מחלקת שחקן המנהלת שם ומאזן כספי
    def __init__(self, name, initial_balance=1000):
        ## self: המופע הספציפי שנוצר כרגע בזיכרון (הכתובת של האובייקט)
        ## זה הפרמטר הראשון שתמיד חייב להופיע במתודות של מחלקה
        ## Dunder Method: בנאי (Constructor) המופעל בעת יצירת אובייקט
        self._name = name  ## Encapsulation: הגנה על נתון (שם)
        self._balance = initial_balance  ## OOP: משתנה אובייקט (Object Member) - ספציפי למופע

    @property
    def name(self):
        ## self: מאפשר למתודה לגשת לנתונים של האובייקט הספציפי
        ## Getter לשם השחקן
        return self._name

    @property
    def balance(self):
        ## Encapsulation: Getter לקבלת יתרה
        return self._balance

    @balance.setter
    def balance(self, amount):
        ## ציר 1: כימוס (Encapsulation) - הגנה על הנתונים מפני שינוי לא חוקי
        ## Setter: מאפשר עדכון מבוקר של היתרה (למשל: בדיקה שהסכום לא שלילי)
        if amount < 0:
            raise ValueError("Balance cannot be negative.")
        self._balance = amount

    def __str__(self):
        ## self: מאפשר לייצוג הטקסטואלי להשתמש בערכים האישיים של המופע
        ## Dunder Method: כרטיס ביקור קריא (ייצוג טקסטואלי) המופעל בעת הדפסת האובייקט
        ## משמש בתצוגה ב-main.py
        return f"Player: {self._name}, Balance: ${self._balance:,}"

class Wheel:
    ## ניהול גלגל הרולטה
    ## OOP: משתנה מחלקה (Class Member) - קבוע ומשותף לכל המופעים של הגלגל
    NUMBERS_MAPPING = {
        0: "Green",
        1: "Red", 2: "Black", 3: "Red", 4: "Black", 5: "Red", 6: "Black",
        7: "Red", 8: "Black", 9: "Red", 10: "Black", 11: "Black", 12: "Red",
        13: "Black", 14: "Red", 15: "Black", 16: "Red", 17: "Black", 18: "Red",
        19: "Red", 20: "Black", 21: "Red", 22: "Black", 23: "Red", 24: "Black",
        25: "Red", 26: "Black", 27: "Red", 28: "Black", 29: "Black", 30: "Red",
        31: "Black", 32: "Red", 33: "Black", 34: "Red", 35: "Black", 36: "Red"
    }

    def spin(self):
        ## self: ניגש למשתנה המחלקה NUMBERS_MAPPING דרך המופע הנוכחי
        result_number = random.randint(0, 36)
        result_color = self.NUMBERS_MAPPING[result_number]
        return result_number, result_color

    @staticmethod
    def is_valid_number(num):
        ## Static Method: בדיקת תקינות ללא תלות במופע
        try:
            val = int(num)
            return 0 <= val <= 36
        except (ValueError, TypeError):
            return False

    def __repr__(self):
        ## self: מייצג את "עצמי" לצורך הדפסה טכנית
        ## Dunder Method & Polymorphism: ייצוג טכני פנימי של האובייקט
        return f"<Wheel(TotalNumbers={len(self.NUMBERS_MAPPING)})>"

## --- ירושה ופולימורפיזם: מערכת ההימורים המשודרגת ---

class Bet(ABC):
    ## ציר 2: הורשה (Inheritance) ומחלקה אבסטרקטית
    ## Abstraction: משמשת כ"ממשק" (הסכם) שמחייב את הבנים לממש פונקציות מסוימות
    def __init__(self, selection, amount):
        ## self: הפניה לאובייקט ההימור שזה עתה נוצר
        self.selection = selection
        self.amount = amount

    @abstractmethod
    def check_win(self, roll_number, roll_color):
        ## פולימורפיזם (ציר 3): מתודה אבסטרקטית שתמומש בצורה שונה בכל סוג הימור
        pass

    @abstractmethod
    def get_payout(self, amount):
        ## פולימורפיזם: חישוב זכייה שונה לכל סוג הימור (דריסת מתודות)
        pass

class NumberBet(Bet):
    ## ציר 2: הורשה (Inheritance) - מרחיבה את מחלקת Bet
    ## דריסה (Overriding): מימוש ייחודי של check_win עבור מספר
    def check_win(self, roll_number, roll_color):
        return str(self.selection) == str(roll_number)

    def get_payout(self, amount):
        return amount * 35

class ColorBet(Bet):
    ## הורשה: יורשת מ-Bet ומממשת את ה"הסכם"
    ## דריסה (Overriding): לוגיקת בדיקת זכייה לפי צבע
    def check_win(self, roll_number, roll_color):
        return self.selection.capitalize() == roll_color

    def get_payout(self, amount):
        return amount

class EvenOddBet(Bet):
    ## הורשה ופולימורפיזם: מימוש ייחודי לזוגי/אי-זוגי
    ## דריסה (Overriding): לוגיקה ייחודית במתודה דרוסה
    def check_win(self, roll_number, roll_color):
        if roll_number == 0:
            return False
        is_even = (roll_number % 2 == 0)
        user_wants_even = (self.selection.lower() == "even")
        return is_even == user_wants_even

    def get_payout(self, amount):
        return amount