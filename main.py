import sys
import time
from models import Player, Wheel, NumberBet, ColorBet, EvenOddBet
from database import DatabaseManager
from MainController import MainController
from view import CasinoView

## תבנית MVC: קובץ זה משמש כ-Entry Point וכ-Controller-Initiator.
## בביצוע Refactoring זה, אנו משיגים "צימוד נמוך" (Low Coupling) - הלוגיקה לא תלויה במימוש ה-UI.
## כל האינטראקציה עם המשתמש מתבצעת דרך המופע של CasinoView.

class Validator:
    ## עקרונות OOP: שיטות סטטיות (Static Methods) לביצוע ולידציה ללא צורך ביצירת אובייקט.
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

class SessionStats:
    ## לכידות גבוהה (High Cohesion): מחלקה זו אחראית אך ורק על ניהול הסטטיסטיקה של הסשן.
    def __init__(self):
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
        return (self.wins / self.total_bets) * 100

    def get_best_numbers(self):
        sorted_nums = sorted(self.hot_numbers.items(), key=lambda x: x[1], reverse=True)
        return [str(n[0]) for n in sorted_nums[:3]]

def main():
    ## אתחול רכיבי ה-MVC
    view = CasinoView()
    db = DatabaseManager()
    stats = SessionStats()
    
    view.print_header()
    
    ## וידוא זהות שחקן דרך ה-View
    sys.stdout.write(f"{view.GOLD}➤ IDENTITY CONFIRMATION: {view.RESET}")
    sys.stdout.flush()
    player_name = input().strip() or "Vogue HighRoller"

    current_balance = db.load_player_data(player_name)
    
    ## יצירת מודלים (Models)
    player = Player(player_name, current_balance)
    wheel = Wheel()
    
    ## קונטרולר מרכזי האחראי על תיאום בין המודל לתצוגה
    controller = MainController(player, wheel, db)

    last_outcome_summary = None

    ## לולאת ה-REPL המרכזית (Read-Eval-Print Loop)
    while True:
        view.print_header()
        
        ## הצגת נתוני הסשן
        win_rate = f"{stats.get_win_rate():.1f}%"
        hot_nums = ", ".join(stats.get_best_numbers()) or "---"
        
        overview = [
            f"{view.WHITE}VAULT INTEL: {view.GOLD}{player}",
            f"{view.WHITE}WIN RATE: {view.CYAN}{win_rate.ljust(19)} {view.WHITE}HOT LIST: {view.GOLD}{hot_nums}"
        ]
        view.print_box(overview, color=view.PURPLE, title="SESSION INTELLIGENCE", width=80)
        
        ## קבלת תובנות מהדילר (AI)
        insight = controller.get_ai_insight(last_outcome_summary)
        view.type_effect(insight)
        
        if last_outcome_summary:
            is_win = "WINNER" in last_outcome_summary
            view.celebration(is_win)
            color = view.GREEN if is_win else view.RED
            print(f" {view.GOLD}➤ {color}{last_outcome_summary}{view.RESET}")
            last_outcome_summary = None

        ## תפריט הפעולות מבוצע על ידי ה-View
        menu_items = [
            f"{view.CYAN}➊ Specific Number  {view.WHITE}(Range: 0-36)",
            f"{view.CYAN}➋ Color Harmony    {view.WHITE}(Red/Black)",
            f"{view.CYAN}➌ Parity Bet       {view.WHITE}(Even/Odd)",
            f"{view.PURPLE}➍ View Ledger      {view.WHITE}(History)",
            f"{view.RED}➎ Terminate        {view.WHITE}(Cash Out)"
        ]
        view.print_box(menu_items, color=view.PURPLE, title="MARKET OPERATIONS", width=42)
        
        choice = input(f"\n{view.GOLD}COMMAND ➤ {view.RESET}").strip()

        if choice in ["5", "➎"]:
            print(f"\n{view.CYAN}Banker: Final assessment complete. Payout of ${player.balance} issued.{view.RESET}")
            break
        
        if choice in ["4", "➍"]:
            history = db.get_player_history(player.name)
            view.show_history_table(history)
            input(f"\n{view.GOLD}Press Enter to return to the table...{view.RESET}")
            continue

        if choice not in ["1", "2", "3", "➊", "➋", "➌"]:
            continue

        if player.balance <= 0:
            print(f"{view.RED}⚠ Liquidity Crisis. Request a $1,000 bailout? (y/n){view.RESET}")
            if input().lower() == 'y':
                player.balance = 1000
                db.update_balance(player.name, 1000)
            continue

        try:
            target = None
            bet_class = None

            if choice in ["1", "➊"]:
                target = input(f"{view.CYAN}Target Integer (0-36): {view.RESET}").strip()
                if not Wheel.is_valid_number(target):
                    print(f"{view.RED}⚠ Protocol Error: Integer overflow (0-36).{view.RESET}")
                    time.sleep(1)
                    continue
                bet_class = NumberBet
            elif choice in ["2", "➋"]:
                target = input(f"{view.CYAN}Target Harmony (Red/Black): {view.RESET}").strip().capitalize()
                if target not in ["Red", "Black"]:
                    print(f"{view.RED}⚠ Protocol Error: Unknown harmony.{view.RESET}")
                    time.sleep(1)
                    continue
                bet_class = ColorBet
            elif choice in ["3", "➌"]:
                target = input(f"{view.CYAN}Target Parity (Even/Odd): {view.RESET}").strip().lower()
                if target not in ["even", "odd"]:
                    print(f"{view.RED}⚠ Protocol Error: Parity mismatch.{view.RESET}")
                    time.sleep(1)
                    continue
                bet_class = EvenOddBet

            amt_input = input(f"{view.CYAN}Capital Allocation: ${view.RESET}").strip()
            if not Validator.validate_amount(amt_input, player.balance):
                print(f"{view.RED}⚠ Protocol Error: Quantitative value required or balance insufficient.{view.RESET}")
                time.sleep(1)
                continue
            amount = int(amt_input)

            ## פולימורפיזם (Polymorphism): יצירת אובייקט הימור והעברתו לעיבוד בקונטרולר
            current_bet = bet_class(target, amount)
            
            roll_number, roll_color = wheel.spin()
            view.spin_animation(roll_number, roll_color)
            result = controller.process_bet(current_bet)
            
            stats.update(roll_number, "WINNER" if "WINNER" in result else "LOST")
            last_outcome_summary = result
            
        except Exception as e:
            print(f"{view.RED}⚠ System Fault: {e}{view.RESET}")
            time.sleep(2)

if __name__ == "__main__":
    main()