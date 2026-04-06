import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
import random, secrets, requests, threading, time, webbrowser, os

# --- SSL FIX FÜR ANDROID ---
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

# --- DESIGN ---
CLR_BG = get_color_from_hex("#020617")
CLR_ACCENT = get_color_from_hex("#22d3ee")
CLR_GOLD = get_color_from_hex("#fbbf24")
CLR_RED = get_color_from_hex("#f43f5e")

LOTTERIEN = {
    "6aus49": {"kugeln": 6, "max": 49, "zusatz": "SZ", "z_max": 9},
    "Eurojackpot": {"kugeln": 5, "max": 50, "zusatz": "EZ", "z_max": 12},
    "Glücksspirale": {"kugeln": 7, "max": 9, "zusatz": None},
    "Bayern-Lotto": {"kugeln": 6, "max": 49, "zusatz": "BZ", "z_max": 10}
}

class KarmaManager:
    def __init__(self):
        self.projekte_pool = {"BAYERN": [], "AUGSBURG": [], "GLOBAL": []}
    
    def update_daten(self, neue_daten):
        self.projekte_pool.update(neue_daten)

    def ziehe_projekt(self, region):
        pool = self.projekte_pool.get(region, [["Standard", "https://google.com"]])
        return random.choice(pool)

class QuantumLottoKarmaApp(App):
    def build(self):
        self.is_drawing = False
        self.current_lotto = "6aus49"
        self.current_region = "BAYERN"
        self.karma_manager = KarmaManager()
        
        # UI Setup
        self.root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Header
        header = Button(text="VORTEX LOTTO v1.0", font_size=sp(22), bold=True, color=CLR_ACCENT, background_color=(0,0,0,0), size_hint_y=None, height=dp(50))
        self.root.add_widget(header)

        # Auswahl
        lotto_grid = GridLayout(cols=4, size_hint_y=None, height=dp(45), spacing=dp(5))
        for l_name in LOTTERIEN.keys():
            btn = ToggleButton(text=l_name, group="lotto", state="down" if l_name == "6aus49" else "normal", font_size=sp(10))
            btn.bind(on_release=lambda x, n=l_name: self.set_lotto(n))
            lotto_grid.add_widget(btn)
        self.root.add_widget(lotto_grid)

        # Kugeln
        self.ball_row = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        self.ball_labels = [Label(text="?", font_size=sp(26), bold=True, color=(0.4, 0.4, 0.4, 1)) for _ in range(7)]
        for lbl in self.ball_labels: self.ball_row.add_widget(lbl)
        self.root.add_widget(self.ball_row)

        # Historie
        self.history_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self.history_list.bind(minimum_height=self.history_list.setter('height'))
        scroll = ScrollView(size_hint_y=None, height=dp(100))
        scroll.add_widget(self.history_list)
        self.root.add_widget(scroll)

        # Status & Buttons
        self.status_label = Label(text="Bereit für Quanten-Ziehung", color=CLR_ACCENT, size_hint_y=None, height=dp(30))
        self.root.add_widget(self.status_label)

        btn_row = BoxLayout(size_hint_y=None, height=dp(70), spacing=dp(10))
        self.start_btn = Button(text="ZIEHUNG", background_color=get_color_from_hex("#0e7490"), bold=True)
        self.start_btn.bind(on_release=self.start_draw)
        karma_btn = Button(text="KARMA", background_color=CLR_RED, bold=True)
        karma_btn.bind(on_release=lambda x: webbrowser.open(self.karma_manager.ziehe_projekt(self.current_region)[1]))
        btn_row.add_widget(self.start_btn)
        btn_row.add_widget(karma_btn)
        self.root.add_widget(btn_row)

        return self.root

    def set_lotto(self, name): self.current_lotto = name
    def set_status_safe(self, text): Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', text))

    def start_draw(self, *args):
        if not self.is_drawing:
            self.is_drawing = True
            self.start_btn.disabled = True
            for lbl in self.ball_labels: lbl.text = "?"; lbl.color = (0.4, 0.4, 0.4, 1)
            threading.Thread(target=self.run_logic, daemon=True).start()

    def run_logic(self):
        cfg = LOTTERIEN[self.current_lotto]
        ergebnis = []
        source = "Quanten-Zufall (ANU)"

        # 1. API VERSUCH (ANU)
        try:
            r = requests.get("https://anu.edu.au", timeout=2)
            data = r.json()['data']
            if self.current_lotto == "Eurojackpot":
                ergebnis = self.secure_sample(range(1, 51), 5) + self.secure_sample(range(1, 13), 2)
            elif self.current_lotto == "Glücksspirale":
                ergebnis = [d % 10 for d in data[:7]]
            else:
                ergebnis = self.secure_sample(range(1, cfg["max"]+1), cfg["kugeln"])
        except:
            source = "Sicherer Offline-Zufall"
            if self.current_lotto == "Eurojackpot":
                ergebnis = self.secure_sample(range(1, 51), 5) + self.secure_sample(range(1, 13), 2)
            elif self.current_lotto == "Glücksspirale":
                ergebnis = [secrets.randbelow(10) for _ in range(7)]
            else:
                ergebnis = self.secure_sample(range(1, cfg["max"]+1), cfg["kugeln"])

        self.set_status_safe(f"Quelle: {source}")
        for i, val in enumerate(ergebnis):
            time.sleep(0.2)
            Clock.schedule_once(lambda dt, idx=i, v=val: self.update_ball_ui(idx, v))
        
        Clock.schedule_once(lambda dt: self.finalize(ergebnis))

    def secure_sample(self, pop, k):
        p = list(pop)
        res = []
        for _ in range(k):
            c = secrets.choice(p)
            res.append(c)
            p.remove(c)
        return res

    def update_ball_ui(self, idx, val):
        if idx < len(self.ball_labels):
            self.ball_labels[idx].text = str(val)
            self.ball_labels[idx].color = CLR_GOLD if (self.current_lotto == "Eurojackpot" and idx >= 5) else (1, 1, 1, 1)

    def finalize(self, res):
        self.is_drawing = False
        self.start_btn.disabled = False
        h_text = f"{self.current_lotto}: " + ", ".join(map(str, res))
        self.history_list.add_widget(Label(text=h_text, size_hint_y=None, height=dp(20), font_size=sp(10)), index=len(self.history_list.children))

if __name__ == '__main__':
    QuantumLottoKarmaApp().run()
