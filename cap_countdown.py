Python
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os

# 預設各年份的會考日期（通常為5月中旬的週六、週日，這裡以第一天上午 08:00 為基準）
EXAM_DATES = {
    "2027": "2027-05-15 08:00:00",
    "2028": "2028-05-20 08:00:00",
    "2029": "2029-05-19 08:00:00",
    "2030": "2030-05-18 08:00:00"
}
CONFIG_FILE = "countdown_config.txt"

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("國中教育會考倒數計時器")
        
        # --- 視窗美化與常駐設定 ---
        self.root.overrideredirect(True)      # 隱藏標題列與視窗邊框
        self.root.attributes("-topmost", True)  # 永遠置頂（常駐桌面最上層）
        self.root.attributes("-alpha", 0.88)   # 88% 半透明度，提升質感
        self.root.configure(bg="#1e1e24")      # 極致深灰背景
        self.root.geometry("320x150+100+100")  # 初始視窗大小與位置
        
        # 綁定滑鼠事件，讓無邊框視窗可以隨意拖曳移動
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.drag_window)
        
        # --- 介面元件佈局 ---
        self.top_frame = tk.Frame(root, bg="#1e1e24")
        self.top_frame.pack(fill="x", padx=15, pady=8)
        
        # 讀取上次記憶的年份，若無則預設 2027
        saved_year = self.load_config()
        self.year_var = tk.StringVar(value=saved_year)
        
        # 美化下拉選單
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TCombobox", fieldbackground="#2a2a35", background="#2a2a35", foreground="white")
        
        self.dropdown = ttk.Combobox(self.top_frame, textvariable=self.year_var, values=list(EXAM_DATES.keys()), width=6, state="readonly")
        self.dropdown.pack(side="left")
        self.dropdown.bind("<<ComboboxSelected>>", self.on_year_change)
        
        # 標題標籤
        self.title_label = tk.Label(self.top_frame, text="年會考倒數", fg="#aaaaaa", bg="#1e1e24", font=("Microsoft JhengHei", 10, "bold"))
        self.title_label.pack(side="left", padx=5)
        
        # 右上角關閉按鈕 (X)
        self.close_btn = tk.Button(self.top_frame, text="×", fg="#ff5555", bg="#1e1e24", bd=0, font=("Arial", 14, "bold"), command=root.quit, cursor="hand2")
        self.close_btn.pack(side="right")
        
        # 倒數計時主要顯示區域
        self.time_label = tk.Label(root, text="", fg="#ffb86c", bg="#1e1e24", font=("Helvetica", 22, "bold"))
        self.time_label.pack(expand=True, fill="both", pady=5)
        
        # 初始化時間並啟動時鐘
        self.update_target_time()
        self.update_clock()

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def drag_window(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def update_target_time(self):
        selected_year = self.year_var.get()
        date_str = EXAM_DATES.get(selected_year, f"{selected_year}-05-15 08:00:00")
        self.target_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    def on_year_change(self, event=None):
        self.update_target_time()
        self.save_config(self.year_var.get())

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    year = f.read().strip()
                    if year in EXAM_DATES:
                        return year
            except:
                pass
        return "2027"

    def save_config(self, year):
        try:
            with open(CONFIG_FILE, "w") as f:
                f.write(year)
        except:
            pass

    def update_clock(self):
        now = datetime.now()
        time_diff = self.target_time - now
        
        if time_diff.total_seconds() <= 0:
            self.time_label.config(text="考試開始！\n祝各位考生金榜題名！", fg="#50fa7b", font=("Microsoft JhengHei", 16, "bold"))
        else:
            days = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            # 格式化輸出：天、時、分、秒
            time_str = f"{days} 天\n{hours:02d} 時 {minutes:02d} 分 {seconds:02d} 秒"
            self.time_label.config(text=time_str)
            
        # 每 1000 毫秒 (1秒) 自動刷新一次介面
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()
