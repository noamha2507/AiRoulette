import random
from abc import ABC, abstractmethod

class Player:
    """מחלקת שחקן המנהלת שם ומאזן כספי"""
    def __init__(self, name, initial_balance=1000):
        self.name = name
        self.balance = initial_balance

    def get_balance(self):
        """מחזירה את היתרה הנוכחית"""
        return self.balance

    def set_balance(self, amount):
        """מעדכנת את היתרה (בשימוש ע"י הקונטרולר)"""
        self.balance = amount

    def __str__(self):
        """Dunder Method: ייצוג טקסטואלי מעוצב לפי דרישות הסילבוס"""
        return f"Player: {self.name}, Balance: ${self.balance:,}"

class Wheel:
    """מחלקת גלגל הרולטה המנהלת את המספרים והצבעים (0-36)"""
    # הגדרת משאבים משותפים כמשתנה מחלקה (Class Attribute) לפי דרישות הסילבוס
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
        """מבצעת סיבוב ומחזירה מספר וצבע אקראיים"""
        result_number = random.randint(0, 36)
        result_color = self.NUMBERS_MAPPING[result_number]
        return result_number, result_color

    def __repr__(self):
        """Dunder Method: ייצוג טכני של אובייקט הגלגל"""
        return f"<Wheel(TotalNumbers=37)>"

# --- ירושה ופולימורפיזם: מערכת ההימורים המשודרגת ---

class Bet(ABC):
    """מחלקת אב אבסטרקטית לכל סוגי ההימורים (לפי סילבוס הקורס)"""
    def __init__(self, selection, amount):
        self.selection = selection
        self.amount = amount

    @abstractmethod
    def check_win(self, roll_number, roll_color):
        """בדיקה האם ההימור זכה"""
        pass

    @abstractmethod
    def get_payout(self, amount):
        """חישוב סכום הזכייה"""
        pass

class NumberBet(Bet):
    """הימור על מספר ספציפי (יחס 1:35)"""
    def check_win(self, roll_number, roll_color):
        return int(self.selection) == roll_number

    def get_payout(self, amount):
        return amount * 35

class ColorBet(Bet):
    """הימור על צבע (Red/Black - יחס 1:1)"""
    def check_win(self, roll_number, roll_color):
        return self.selection.capitalize() == roll_color

    def get_payout(self, amount):
        return amount

class EvenOddBet(Bet):
    """הימור על זוגי/אי-זוגי (יחס 1:1)"""
    def check_win(self, roll_number, roll_color):
        if roll_number == 0:
            return False
        is_even = (roll_number % 2 == 0)
        user_wants_even = (self.selection.lower() == "even")
        return is_even == user_wants_even

    def get_payout(self, amount):
        return amount