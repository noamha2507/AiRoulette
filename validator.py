## מודולציה פיזית (Physical Modularity)
## עקרון OOP: לכידות גבוהה (High Cohesion)
## מחלקה זו אחראית בלעדית על אימות קלטי המשתמש כדי למנוע שגיאות זמן הרצה.
class Validator:
    ## עקרונות OOP: שיטות סטטיות (Static Methods) לביצוע ולידציה ללא צורך ביצירת אובייקט.
    ## הדבר מאפשר שימוש חוזר בקוד ללא תלות במצב המערכת (Stateless).
    @staticmethod
    def validate_number(val, min_val, max_val):
        try:
            num = int(val)
            return min_val <= num <= max_val
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_amount(val, balance):
        try:
            amt = int(val)
            return 0 < amt <= balance
        except (ValueError, TypeError):
            return False
