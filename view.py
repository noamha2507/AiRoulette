import os
import sys
import time
import random
import re

## תבנית MVC: שכבת התצוגה (View)
## מחלקה זו אחראית בלעדית על כל מה שהמשתמש רואה בטרמינל.
## יישום עקרון "הפרדת תחומי אחריות" (Separation of Concerns) - הלוגיקה והנתונים מופרדים מהעיצוב.
class CasinoView:
    def __init__(self):
        ## צבעי ANSI לשימוש חוזר ברחבי התצוגה
        self.GOLD = "\033[38;5;214m"
        self.PURPLE = "\033[38;5;141m"
        self.CYAN = "\033[38;5;117m"
        self.GREEN = "\033[38;5;46m"
        self.RED = "\033[38;5;196m"
        self.WHITE = "\033[38;5;255m"
        self.DARK = "\033[38;5;236m"
        self.RESET = "\033[0m"

    ## הסרת קודים של ANSI לצורך חישוב אורך טקסט נקי
    def strip_ansi(self, text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    ## ניקוי המסך בהתאם למערכת ההפעלה
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    ## הדפסת תיבת טקסט מעוצבת
    ## SoC: פונקציה זו מרכזת את כל נושא המסגור והעיצוב הגרפי
    def print_box(self, lines, color=None, width=75, title=None):
        if color is None: color = self.PURPLE
        top_border = f"{color}┏"
        if title:
            top_border += f"━ {self.GOLD}{title} {color}" + "━" * (width - 6 - len(title))
        else:
            top_border += "━" * (width - 2)
        top_border += "┓"
        print(top_border)
        
        for line in lines:
            visible_len = len(self.strip_ansi(line))
            padding = (width - 4) - visible_len
            print(f"{color}┃ {self.RESET}{line}" + " " * padding + f" {color}┃")
        print(f"┗" + "━" * (width - 2) + f"┛{self.RESET}")

    ## אפקט הקלדה של הדילר
    def type_effect(self, text, color=None, speed=0.01):
        if color is None: color = self.CYAN
        sys.stdout.write(f"{self.GOLD}DEALER AI ➤ {self.RESET}{color}")
        for char in text or "":
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print(f"{self.RESET}")

    ## הדפסת כותרת המשחק הגדולה
    def print_header(self):
        self.clear_screen()
        logo = [
            rf"{self.GOLD}    ___     ____     ____   ____  __  __ __     ______ ______ ______ ______ ",
            rf"{self.GOLD}   /   |   /  _/    / __ \ / __ \/ / / // /    / ____//_  __//_  __// ____/",
            rf"{self.GOLD}  / /| |   / /     / /_/ // / / / / / // /    / __/    / /    / /  / __/   ",
            rf"{self.GOLD} / ___ | _/ /     / _, _// /_/ / /_/ // /___ / /___   / /    / /  / /___   ",
            rf"{self.GOLD}/_/  |_|/___/    /_/ |_| \____/\____//_____//_____/  /_/    /_/  /_____/  ",
            "",
            rf"{self.PURPLE}           - EXCLUSIVE HIGH-STAKES VIRTUAL EXPERIENCE -           "
        ]
        self.print_box(logo, color=self.PURPLE, width=80)

    ## הצגת היסטוריית הפעולות בטבלה מעוצבת
    def show_history_table(self, history):
        if not history:
            self.print_box(["No recent action. The table is waiting..."], color=self.PURPLE, title="RECENT ACTION", width=80)
            return

        table_lines = [
            f"{self.GOLD}{'ID':^4} {'TYPE':<12} {'PICK':<10} {'BET':<10} {'STATUS':<10} {'RESULT':<15}{self.RESET}",
            f"{self.PURPLE}" + "━" * 76 + f"{self.RESET}"
        ]
        
        for i, row in enumerate(history, 1):
            _, _, amt, res_raw, ts, b_type, select = row
            clean_res = res_raw.replace('\033[92m','').replace('\033[91m','').replace('\033[93m','').replace('\033[0m','')
            status = "WINNER" if "WINNER" in clean_res else "LOST"
            status_color = self.GREEN if status == "WINNER" else self.RED
            outcome = clean_res.split("Result: ")[1] if "Result: " in clean_res else clean_res
            table_lines.append(f"{self.CYAN}{i:^4} {str(b_type).capitalize():<12} {str(select):<10} ${str(amt):<9} {status_color}{status:<10}{self.RESET} {outcome:<15}")
        
        self.print_box(table_lines, color=self.PURPLE, title="RECENT ACTION", width=80)

    ## אנימציית סיבוב הגלגל
    def spin_animation(self, target_num, target_color):
        frames = ["◐", "◓", "◑", "◒"]
        wheel_nums = list(range(37))
        random.shuffle(wheel_nums)
        
        print(f"\n{self.CYAN}  Initiating wheel rotation...{self.RESET}")
        
        ## שלב תאוצה
        for i in range(10):
            num = random.choice(wheel_nums)
            color = self.RED if random.random() > 0.5 else self.DARK
            sys.stdout.write(f"\r  {color} [ {num:2} ] {frames[i % 4]} {self.RESET}")
            sys.stdout.flush()
            time.sleep(0.08 - (i * 0.005))
            
        ## מהירות גבוהה
        for i in range(20):
            num = random.choice(wheel_nums)
            color = self.RED if random.random() > 0.5 else self.DARK
            sys.stdout.write(f"\r  {color} [ {num:2} ] {frames[i % 4]} {self.RESET}")
            sys.stdout.flush()
            time.sleep(0.03)

        ## האטה והמתנה לתוצאה
        for i in range(15):
            num = random.choice(wheel_nums)
            color = self.RED if random.random() > 0.5 else self.DARK
            sys.stdout.write(f"\r  {color} [ {num:2} ] {frames[i % 4]} {self.RESET}")
            sys.stdout.flush()
            time.sleep(0.03 + (i * 0.02))

        res_color = self.RED if target_color == "Red" else self.DARK
        if target_color == "Green": res_color = self.GREEN
        
        print(f"\r  {self.GOLD}✨ THE BALL HAS LANDED: {res_color}[ {target_num} {target_color} ]{self.RESET} \n")

    ## הודעת חגיגה או הפסד לאחר הגרלה
    def celebration(self, is_win):
        if is_win:
            print(f"{self.GREEN}   💰 ✧✧✧ EXCELLENT! YOU HAVE WON THE ROUND ✧✧✧ 💰{self.RESET}")
        else:
            print(f"{self.RED}   ⚖ ✧✧✧ FORTUNE WAS NOT WITH YOU THIS TIME ✧✧✧ ⚖{self.RESET}")
