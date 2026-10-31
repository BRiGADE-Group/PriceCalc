import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
import requests, time, asyncio, threading
import os, sys ,pygame

class cfg():
    about_txt = "App Name : PriceCalc\nApp Version : v1.0\nAuthor : 0xSenko\nContributor(s) : Oxyru\nMessage : Greetz to mah gamers fellas!"
    APPIDS = []

class AutoLoopPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("280x100")
        self.root.resizable(False, False)

        pygame.mixer.init()

        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.track_path = os.path.join(script_dir, "music.mp3")
        self.is_playing = False

        tk.Label(self.root, font=("Arial", 9, "italic"), text="Now Playing : sacio - cheeze surfer [2016]\n@djodin2194 on YT!").pack()

        self.status_label = tk.Label(self.root, font=("Arial", 9, "italic"), pady=8)
        # self.status_label.pack()

        self.btn = tk.Button(
            self.root, 
            text="⏸ Pause", 
            font=("Arial", 11, "bold"), 
            width=12, 
            command=self.toggle_playback,
            bg="#f44336",
            fg="white"
        )
        self.btn.pack(pady=5)

        self.auto_start()

    def auto_start(self):
        if os.path.exists(self.track_path):
            try:
                pygame.mixer.music.load(self.track_path)
                pygame.mixer.music.play(loops=-1) # -1 loops forever
                self.is_playing = True
                self.status_label.config(text="Looping: music.mp3")
            except Exception as e:
                self.status_label.config(text="Error loading music file.")
        else:
            self.status_label.config(text="Error: Place 'music.mp3' in this folder!")
            self.btn.config(text="❌ No File", bg="#555555", state=tk.DISABLED)

    def toggle_playback(self):
        if not self.is_playing:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.btn.config(text="⏸ Pause", bg="#f44336")
        else:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.btn.config(text="▶ Play", bg="#2196F3")

def load_appids(filepath):
    try:
        cfg.APPIDS = [line.strip() for line in open(filepath) if line.strip()]
        return cfg.APPIDS
    except TypeError:
        return cfg.APPIDS

def log(text, entry_1):
    entry_1.configure(state=tk.NORMAL)
    entry_1.insert(tk.END, text+"\n")
    entry_1.see(tk.END)
    entry_1.configure(state=tk.DISABLED)
    
async def calc(entry_1, entry_2):
    if not cfg.APPIDS: 
        return
    
    entry_2.configure(state=tk.DISABLED)
    try:
        COUNTRIES = [ 
            "ar","au","br","ca","cl","cn","co","cz","de","eg",
            "fr","gb","gr","hu","il","in","id","it","jp","kr",
            "mx","my","nl","no","nz","ph","pl","ro","ru","sa",
            "sg","za","es","se","ch","tw","tr","ua","us","ve","vn"
            ]

        rows = requests.get("https://api.frankfurter.dev/v2/rates?base=USD", timeout=10).json()
        fx = {row["quote"]: row["rate"] for row in rows}
        log(f"FX : {len(fx)} currencies loaded\n", entry_1)

        country_prices = {}

        for i, cc in enumerate(COUNTRIES):
            url = (
                f"https://store.steampowered.com/api/appdetails"
                f"?appids={','.join(map(str, cfg.APPIDS))}"
                f"&cc={cc}&filters=price_overview"
            )
            try:
                data = requests.get(url, timeout=15).json()
            except Exception as e:
                log(f"[{i+1:2d}/{len(COUNTRIES)}] {cc} — error: {e}", entry_1)
                continue

            prices = []
            for appid in cfg.APPIDS:
                app_data = data.get(str(appid), {})
                if not app_data.get("success"):
                    continue
                d = app_data.get("data")
                if not isinstance(d, dict):
                    continue
                po = d.get("price_overview")
                if not po:
                    continue
                usd = (po["final"] / 100) / fx.get(po["currency"], 1)
                prices.append(usd)

            if prices:
                country_prices[cc] = sum(prices) / len(prices) 
                log(f"[{i+1:2d}/{len(COUNTRIES)}] {cc} — avg ${country_prices[cc]:.2f} ({len(prices)} games)", entry_1)

            time.sleep(1.5)  

        log(f"\n{'Rank':<5}{'Country':<10}{'Avg (USD)':<12}", entry_1)
        log("-" * 27, entry_1)
        for rank, (cc, avg) in enumerate(sorted(country_prices.items(), key=lambda x: x[1]), 1):
            log(f"{rank:<5}{cc:<10}${avg:.2f}", entry_1)

        best = sorted(country_prices.items(), key=lambda x: x[1])[0]
        log(f"\nCheapest: {best[0]} at ${best[1]:.2f}/game", entry_1)

        entry_2.configure(state=tk.NORMAL)
    except Exception as e:
        print(e)
        entry_2.configure(state=tk.NORMAL)
    finally:
        entry_2.configure(state=tk.NORMAL)

def start_async_loop(entry_1, entry_2):
    asyncio.run(calc(entry_1, entry_2))

def window():
    root = tk.Tk()
    root.wm_title("PriceCalc v1")
    window_width = 450
    window_height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def update_stats_from_ui():
        raw_text = entry1.get("1.0", tk.END)
        cfg.APPIDS = [line.strip() for line in raw_text.splitlines() if line.strip()]
        ids = len(cfg.APPIDS)
        
        entry2.configure(state=tk.NORMAL)
        entry2.delete("1.0", tk.END)
        entry2.configure(state=tk.DISABLED)
        
        log(f"Loaded {ids} AppIDs.\nEstimated calculation time : {ids * 1.5}s.", entry2)

    def on_entry1_modified(event):
        update_stats_from_ui()

    def opnai():
        filetypes = (('text files', '*.txt'),)
        filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
        if not filename: return
        load_appids(filename)        
        entry1.delete("1.0", tk.END)
        entry1.insert(tk.END, "".join(f"{key}\n" for key in cfg.APPIDS))
        update_stats_from_ui()

    menu = tk.Menu(root)
    root.config(menu=menu)

    filemenu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="Open AppID list file", command=opnai)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)

    helpmenu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="About", command=lambda: messagebox.showinfo(title="About", message=cfg.about_txt))

    tk.Label(root, text="PriceCalc", font=("Arial", 24, "bold")).pack(pady=10)
    tk.Label(root, text="Current AppID list :", font=("Arial", 10)).pack(anchor="w", padx=20)
    entry1 = tk.Text(
        root, 
        width=40, 
        height=8,
        font=("Consolas", 10),
        bg="#ffffff",
        fg="#333333",
        relief=tk.SUNKEN,
        bd=2,
        padx=5,      
        pady=5
    )
    entry1.pack(pady=(5, 10), padx=20, fill=tk.BOTH, expand=True)
    entry1.bind("<KeyRelease>", on_entry1_modified)
    tk.Button(root, text="Calculate", command=lambda: threading.Thread(target=start_async_loop, args=(entry2,entry1,), daemon=True).start()).pack(pady=5)
    tk.Label(root, text="Execution Logs:", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(10, 0))
    entry2 = tk.Text(
        root, 
        width=40, 
        height=12,
        font=("Consolas", 10),
        bg="#f5f5f5",
        fg="#222222",
        relief=tk.SUNKEN,
        bd=2,
        padx=5,      
        pady=5
    )
    entry2.config(state=tk.DISABLED)
    entry2.pack(pady=(5, 20), padx=20, fill=tk.BOTH, expand=True)

    root.mainloop()

def musicplayer():
    mp = tk.Tk()
    app = AutoLoopPlayer(mp)
    mp.mainloop()

if __name__ == "__main__":
    threading.Thread(target=musicplayer, daemon=True).start()
    window()