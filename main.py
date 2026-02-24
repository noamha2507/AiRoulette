import sys
import time
import os
import random
import re
from models import Player, Wheel
from database import DatabaseManager
from MainController import MainController

class SessionStats:
    """מעקב אחר נתוני הסשן הנוכחי עבור הדשבורד"""
    def __init__(self):
        self.total_bets = 0
        self.wins = 0
        self.history = []
        self.hot_numbers = {}

    def update(self, num, result_type):
        """מעדכן סטטיסטיקה לאחר כל הימור"""
        self.total_bets += 1
        if result_type == "WINNER":
            self.wins += 1
        self.history.append(num)
        self.hot_numbers[num] = self.hot_numbers.get(num, 0) + 1
    
    def get_win_rate(self):
        """מחשב אחוז זכיות"""
        if self.total_bets == 0: return 0
        return (self.wins / self.total_bets) * 100

    def get_best_numbers(self):
        """מחזיר את 3 המספרים שהופיעו הכי הרבה"""
        sorted_nums = sorted(self.hot_numbers.items(), key=lambda x: x[1], reverse=True)
        return [str(n[0]) for n in sorted_nums[:3]]

# --- עזרי UI ותצוגה ---

def strip_ansi(text):
    """מסירה קודי צבע ANSI לצורך חישוב אורך טקסט נקי"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def print_box(lines, color="\033[38;5;141m", width=75, title=None):
    """מדפיסה מסגרת מעוצבת (דשבורד) סביב הטקסט"""
    RESET = "\033[0m"
    GOLD = "\033[38;5;214m"
    top_border = f"{color}┏"
    if title:
        top_border += f"━ {GOLD}{title} {color}" + "━" * (width - 6 - len(title))
    else:
        top_border += "━" * (width - 2)
    top_border += "┓"
    print(top_border)
    
    for line in lines:
        visible_len = len(strip_ansi(line))
        padding = (width - 4) - visible_len
        print(f"{color}┃ {RESET}{line}" + " " * padding + f" {color}┃")
    print(f"┗" + "━" * (width - 2) + f"┛{RESET}")

def clear_screen():
    """מנקה את המסך לתצוגה חלקה"""
    os.system('cls' if os.name == 'nt' else 'clear')

def type_effect(text, color="\033[38;5;117m", speed=0.01):
    """אפקט הקלדה עבור הדילר"""
    RESET = "\033[0m"
    GOLD = "\033[38;5;214m"
    sys.stdout.write(f"{GOLD}DEALER AI ➤ {RESET}{color}")
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print(f"{RESET}")

def print_header():
    """הדפסת הלוגו המרכזי בראש המשחק"""
    GOLD = "\033[38;5;214m"
    PURPLE = "\033[38;5;141m"
    clear_screen()
    logo = [
        rf"{GOLD}    ___     ____     ____   ____  __  __ __     ______ ______ ______ ______ ",
        rf"{GOLD}   /   |   /  _/    / __ \ / __ \/ / / // /    / ____//_  __//_  __// ____/",
        rf"{GOLD}  / /| |   / /     / /_/ // / / / / / // /    / __/    / /    / /  / __/   ",
        rf"{GOLD} / ___ | _/ /     / _, _// /_/ / /_/ // /___ / /___   / /    / /  / /___   ",
        rf"{GOLD}/_/  |_|/___/    /_/ |_| \____/\____//_____//_____/  /_/    /_/  /_____/  ",
        "",
        rf"{PURPLE}           - EXCLUSIVE HIGH-STAKES VIRTUAL EXPERIENCE -           "
    ]
    print_box(logo, color=PURPLE, width=80)

def show_history_table(history):
    """מציגה טבלת היסטוריית הימורים מעוצבת"""
    PURPLE = "\033[38;5;141m"
    CYAN = "\033[38;5;117m"
    GREEN = "\033[38;5;46m"
    RED = "\033[38;5;196m"
    GOLD = "\033[38;5;214m"
    RESET = "\033[0m"
    
    if not history:
        print_box(["No recent action. The table is waiting..."], color=PURPLE, title="RECENT ACTION", width=80)
        return

    table_lines = [
        f"{GOLD}{'ID':^4} {'TYPE':<12} {'PICK':<10} {'BET':<10} {'STATUS':<10} {'RESULT':<15}{RESET}",
        f"{PURPLE}" + "━" * 76 + f"{RESET}"
    ]
    
    for i, row in enumerate(history, 1):
        _, _, amt, res_raw, ts, b_type, select = row
        clean_res = res_raw.replace('\033[92m','').replace('\033[91m','').replace('\033[93m','').replace('\033[0m','')
        status = "WINNER" if "WINNER" in clean_res else "LOST"
        status_color = GREEN if status == "WINNER" else RED
        outcome = clean_res.split("Result: ")[1] if "Result: " in clean_res else clean_res
        table_lines.append(f"{CYAN}{i:^4} {str(b_type).capitalize():<12} {str(select):<10} ${str(amt):<9} {status_color}{status:<10}{RESET} {outcome:<15}")
    
    print_box(table_lines, color=PURPLE, title="RECENT ACTION", width=80)

# --- אנימציות ---

def spin_animation(target_num, target_color):
    """אנימציית סיבוב גלגל עם שלבי תאוצה והאטה"""
    GOLD = "\033[38;5;214m"
    CYAN = "\033[38;5;117m"
    RED = "\033[38;5;196m"
    GREEN = "\033[38;5;46m"
    DARK = "\033[38;5;236m"
    RESET = "\033[0m"
    
    frames = ["◐", "◓", "◑", "◒"]
    wheel_nums = list(range(37))
    random.shuffle(wheel_nums)
    
    print(f"\n{CYAN}  Initiating wheel rotation...{RESET}")
    
    # שלב תאוצה
    for i in range(10):
        num = random.choice(wheel_nums)
        color = RED if random.random() > 0.5 else DARK
        sys.stdout.write(f"\r  {color} [ {num:2} ] {frames[i % 4]} {RESET}")
        sys.stdout.flush()
        time.sleep(0.08 - (i * 0.005))
        
    # מהירות גבוהה
    for i in range(20):
        num = random.choice(wheel_nums)
        color = RED if random.random() > 0.5 else DARK
        sys.stdout.write(f"\r  {color} [ {num:2} ] {frames[i % 4]} {RESET}")
        sys.stdout.flush()
        time.sleep(0.03)

    # האטה והמתנה לתוצאה
    for i in range(15):
        num = random.choice(wheel_nums)
        color = RED if random.random() > 0.5 else DARK
        sys.stdout.write(f"\r  {color} [ {num:2} ] {frames[i % 4]} {RESET}")
        sys.stdout.flush()
        time.sleep(0.03 + (i * 0.02))

    res_color = RED if target_color == "Red" else DARK
    if target_color == "Green": res_color = GREEN
    
    print(f"\r  {GOLD}✨ THE BALL HAS LANDED: {res_color}[ {target_num} {target_color} ]{RESET} \n")

def celebration(is_win):
    """הודעה חגיגית לאחר זכייה או הפסד"""
    GOLD = "\033[38;5;214m"
    GREEN = "\033[38;5;46m"
    RED = "\033[38;5;196m"
    RESET = "\033[0m"
    
    if is_win:
        print(f"{GREEN}   💰 ✧✧✧ EXCELLENT! YOU HAVE WON THE ROUND ✧✧✧ 💰{RESET}")
    else:
        print(f"{RED}   ⚖ ✧✧✧ FORTUNE WAS NOT WITH YOU THIS TIME ✧✧✧ ⚖{RESET}")

# --- לולאת המשחק המרכזית ---

def main():
    GOLD = "\033[38;5;214m"
    PURPLE = "\033[38;5;141m"
    CYAN = "\033[38;5;117m"
    GREEN = "\033[38;5;46m"
    RED = "\033[38;5;196m"
    WHITE = "\033[38;5;255m"
    RESET = "\033[0m"

    print_header()
    db = DatabaseManager()
    stats = SessionStats()
    
    # וידוא זהות שחקן
    sys.stdout.write(f"{GOLD}➤ IDENTITY CONFIRMATION: {RESET}")
    sys.stdout.flush()
    player_name = input().strip() or "Vogue HighRoller"

    current_balance = db.load_player_data(player_name)
    player = Player(player_name, current_balance)
    wheel = Wheel()
    controller = MainController(player, wheel, db)

    last_outcome_summary = None

    while True:
        print_header()
        
        # שכבה 1: נתוני חשבון וביצועים
        win_rate = f"{stats.get_win_rate():.1f}%"
        hot_nums = ", ".join(stats.get_best_numbers()) or "---"
        
        overview = [
            f"{WHITE}PLAYER: {GOLD}{player.name.ljust(22)} {WHITE}VAULT: {GREEN}${format(player.get_balance(), ',')}",
            f"{WHITE}WIN RATE: {CYAN}{win_rate.ljust(19)} {WHITE}HOT LIST: {GOLD}{hot_nums}"
        ]
        print_box(overview, color=PURPLE, title="SESSION INTELLIGENCE", width=80)
        
        # שכבה 2: הדילר וסטטוס אחרון
        insight = controller.get_ai_insight(last_outcome_summary)
        type_effect(insight)
        
        if last_outcome_summary:
            is_win = "WINNER" in last_outcome_summary
            celebration(is_win)
            print(f" {GOLD}➤ {last_outcome_summary}{RESET}")
            last_outcome_summary = None

        # שכבה 3: תפריט פעולות
        menu_items = [
            f"{CYAN}➊ Specific Number  {WHITE}(Range: 0-36)",
            f"{CYAN}➋ Color Harmony    {WHITE}(Red/Black)",
            f"{CYAN}➌ Parity Bet       {WHITE}(Even/Odd)",
            f"{PURPLE}➍ View Ledger      {WHITE}(History)",
            f"{RED}➎ Terminate        {WHITE}(Cash Out)"
        ]
        print_box(menu_items, color=PURPLE, title="MARKET OPERATIONS", width=42)
        
        choice = input(f"\n{GOLD}COMMAND ➤ {RESET}").strip()

        # סיום המשחק
        if choice == "5" or choice == "➎":
            print(f"\n{CYAN}Banker: Final assessment complete. Payout of ${player.get_balance()} issued.{RESET}")
            break
        
        # צפייה בהיסטוריה
        if choice == "4" or choice == "➍":
            history = db.get_player_history(player.name)
            show_history_table(history)
            input(f"\n{GOLD}Press Enter to return to the table...{RESET}")
            continue

        if choice not in ["1", "2", "3", "➊", "➋", "➌"]:
            continue

        # ניהול מצבי חוסר נזילות
        if player.get_balance() <= 0:
            print(f"{RED}⚠ Liquidity Crisis. Request a $1,000 bailout? (y/n){RESET}")
            if input().lower() == 'y':
                player.set_balance(1000)
                db.update_balance(player.name, 1000)
            continue

        try:
            # הגדרת סוג ההימור והקלט
            if choice in ["1", "➊"]:
                target = input(f"{CYAN}Target Integer (0-36): {RESET}").strip()
                if not target.isdigit() or not (0 <= int(target) <= 36):
                    print(f"{RED}⚠ Protocol Error: Integer overflow (0-36).{RESET}")
                    time.sleep(1)
                    continue
                b_type = "number"
            elif choice in ["2", "➋"]:
                target = input(f"{CYAN}Target Harmony (Red/Black): {RESET}").strip().capitalize()
                if target not in ["Red", "Black"]:
                    print(f"{RED}⚠ Protocol Error: Unknown harmony.{RESET}")
                    time.sleep(1)
                    continue
                b_type = "color"
            elif choice in ["3", "➌"]:
                target = input(f"{CYAN}Target Parity (Even/Odd): {RESET}").strip().lower()
                if target not in ["even", "odd"]:
                    print(f"{RED}⚠ Protocol Error: Parity mismatch.{RESET}")
                    time.sleep(1)
                    continue
                b_type = "even_odd"

            # קלט סכום ההימור
            amt_input = input(f"{CYAN}Capital Allocation: ${RESET}").strip()
            if not amt_input.isdigit():
                print(f"{RED}⚠ Protocol Error: Quantitative value required.{RESET}")
                time.sleep(1)
                continue
            amount = int(amt_input)

            if amount > player.get_balance() or amount <= 0:
                print(f"{RED}⚠ Protocol Error: Over-leveraged or invalid allocation.{RESET}")
                time.sleep(1)
                continue

            # ביצוע ההימור
            roll_number, roll_color = wheel.spin()
            spin_animation(roll_number, roll_color)
            result = controller.process_bet(b_type, target, amount)
            
            # עדכון סטטיסטיקה
            stats.update(roll_number, "WINNER" if "WINNER" in result else "LOST")
            last_outcome_summary = result
            
        except Exception as e:
            print(f"{RED}⚠ System Fault: {e}{RESET}")
            time.sleep(2)

if __name__ == "__main__":
    main()