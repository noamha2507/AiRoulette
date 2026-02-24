import random

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

    def set_balance(self, amount):
        """מעדכנת את היתרה (בשימוש ע"י הקונטרולר)"""
        self.balance = amount

class Wheel:
    """מחלקת גלגל הרולטה המנהלת את המספרים והצבעים (0-36)"""
    def __init__(self):
        # פריסת רולטה אירופאית סטנדרטית
        self.numbers = {
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
        result_color = self.numbers[result_number]
        return result_number, result_color