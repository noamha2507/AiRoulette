import time
from models import Player, Wheel, NumberBet, ColorBet, EvenOddBet
from database import DatabaseManager
from MainController import MainController
from view import CasinoView
from validator import Validator
from session_stats import SessionStats

## תבנית MVC: קובץ זה משמש כ-Entry Point (נקודת כניסה) מרכזית.
## מודולציה פיזית (Physical Modularity): הקובץ אינו מכיל הגדרות מחלקות אלא רק תיאום (Orchestration).
## עקרון ה-Single Responsibility: קובץ זה אחראי אך ורק על אתחול המערכת והרצת הלולאה הראשית.

def main():
    ## אתחול רכיבי המערכת (Instantiation)
    ## כל רכיב נמצא בקובץ נפרד להשגת לכידות גבוהה (High Cohesion).
    view = CasinoView()
    db = DatabaseManager()
    stats = SessionStats()
    wheel = Wheel()
    
    view.print_header()
    
    ## קבלת קלט ראשוני דרך שכבת התצוגה (Encapsulated UI)
    player_name = view.get_input("➤ IDENTITY CONFIRMATION: ") or "Vogue HighRoller"

    current_balance = db.load_player_data(player_name)
    player = Player(player_name, current_balance)
    
    ## הקונטרולר המרכזי שמתזמר את הלוגיקה העסקית
    controller = MainController(player, wheel, db)

    last_outcome_summary = None

    ## לולאת ה-REPL (Read-Eval-Print Loop)
    ## הפרדת תחומי אחריות: הלולאה מנהלת את הזרם, ה-View מנהל את התצוגה.
    while True:
        view.print_header()
        
        ## הכנת נתונים לתצוגה
        win_rate = f"{stats.get_win_rate():.1f}%"
        hot_nums = ", ".join(stats.get_best_numbers()) or "---"
        
        overview = [
            f"{view.WHITE}VAULT INTEL: {view.GOLD}{player}",
            f"{view.WHITE}WIN RATE: {view.CYAN}{win_rate.ljust(19)} {view.WHITE}HOT LIST: {view.GOLD}{hot_nums}"
        ]
        view.print_box(overview, color=view.PURPLE, title="SESSION INTELLIGENCE", width=80)
        
        ## הצגת תובנות הדילר דרך ה-View
        insight = controller.get_ai_insight(last_outcome_summary)
        view.type_effect(insight)
        
        if last_outcome_summary:
            is_win = "WINNER" in last_outcome_summary
            view.celebration(is_win)
            output_color = view.GREEN if is_win else view.RED
            view.print_box([f"{view.GOLD}➤ {output_color}{last_outcome_summary}"], color=view.PURPLE, width=80)
            last_outcome_summary = None

        ## תצוגת תפריט פעולות
        menu_items = [
            f"{view.CYAN}➊ Specific Number  {view.WHITE}(Range: 0-36)",
            f"{view.CYAN}➋ Color Harmony    {view.WHITE}(Red/Black)",
            f"{view.CYAN}➌ Parity Bet       {view.WHITE}(Even/Odd)",
            f"{view.PURPLE}➍ View Ledger      {view.WHITE}(History)",
            f"{view.RED}➎ Terminate        {view.WHITE}(Cash Out)"
        ]
        view.print_box(menu_items, color=view.PURPLE, title="MARKET OPERATIONS", width=42)
        
        choice = view.get_input("\nCOMMAND ➤ ")

        if choice in ["5", "➎"]:
            view.type_effect(f"Banker: Final assessment complete. Payout of ${player.balance} issued.", color=view.CYAN)
            break
        
        if choice in ["4", "➍"]:
            history = db.get_player_history(player.name)
            view.show_history_table(history)
            view.get_input("\nPress Enter to return to the table...")
            continue

        if choice not in ["1", "2", "3", "➊", "➋", "➌"]:
            continue

        ## טיפול במצב של חוסר יתרה
        if player.balance <= 0:
            bailout = view.get_input("⚠ Liquidity Crisis. Request a $1,000 bailout? (y/n)", color=view.RED)
            if bailout.lower() == 'y':
                player.balance = 1000
                db.update_balance(player.name, 1000)
            continue

        try:
            target = None
            bet_class = None

            if choice in ["1", "➊"]:
                target = view.get_input("Target Integer (0-36): ", color=view.CYAN)
                if not Wheel.is_valid_number(target):
                    view.type_effect("⚠ Protocol Error: Integer overflow (0-36).", color=view.RED)
                    time.sleep(1)
                    continue
                bet_class = NumberBet
            elif choice in ["2", "➋"]:
                target = view.get_input("Target Harmony (Red/Black): ", color=view.CYAN).capitalize()
                if target not in ["Red", "Black"]:
                    view.type_effect("⚠ Protocol Error: Unknown harmony.", color=view.RED)
                    time.sleep(1)
                    continue
                bet_class = ColorBet
            elif choice in ["3", "➌"]:
                target = view.get_input("Target Parity (Even/Odd): ", color=view.CYAN).lower()
                if target not in ["even", "odd"]:
                    view.type_effect("⚠ Protocol Error: Parity mismatch.", color=view.RED)
                    time.sleep(1)
                    continue
                bet_class = EvenOddBet

            amt_input = view.get_input("Capital Allocation: $", color=view.CYAN)
            if not Validator.validate_amount(amt_input, player.balance):
                view.type_effect("⚠ Protocol Error: Quantitative value required or balance insufficient.", color=view.RED)
                time.sleep(1)
                continue
            amount = int(amt_input)

            ## פולימורפיזם (Polymorphism): העברת אובייקט הימור אבסטרקטי לקונטרולר
            current_bet = bet_class(target, amount)
            
            roll_number, roll_color = wheel.spin()
            view.spin_animation(roll_number, roll_color)
            result = controller.process_bet(current_bet)
            
            stats.update(roll_number, "WINNER" if "WINNER" in result else "LOST")
            last_outcome_summary = result
            
        except Exception as e:
            view.type_effect(f"⚠ System Fault: {e}", color=view.RED)
            time.sleep(2)

if __name__ == "__main__":
    main()