import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
import random, secrets, requests, threading, time, webbrowser, os

# --- SSL FIX FÜR ANDROID ---
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

# --- DESIGN ---
CLR_BG = get_color_from_hex("#020617")
CLR_CARD = get_color_from_hex("#0f172a")
CLR_ACCENT = get_color_from_hex("#22d3ee")
CLR_GOLD = get_color_from_hex("#fbbf24")
CLR_RED = get_color_from_hex("#f43f5e")

# --- KONFIGURATION (Editierbare Listen) ---
LOTTERIEN = {
    "6aus49": {"kugeln": 6, "max": 49, "zusatz": "SZ", "z_max": 9},
    "Eurojackpot": {"kugeln": 5, "max": 50, "zusatz": "EZ", "z_max": 12},
    "Glücksspirale": {"kugeln": 7, "max": 9, "zusatz": None},
    "Bayern-Lotto": {"kugeln": 6, "max": 49, "zusatz": "BZ", "z_max": 10}
}

SPENDEN_PROJEKTE = {
    "BAYERN": [
        ("Spenden für Bayern", "https://share.google/Xuehkxs9BatunONIq"),
        ("Sternstunden e.V.", "https://www.sternstunden.de"),
        ("LBV Bayern", "https://www.lbv.de")
    ],
    "AUGSBURG": [
        ("Zoo Augsburg", "https://www.zoo-augsburg.com"), 
        ("Bunter Kreis", "https://www.bunter-kreis.de"),
        ("Tierheim Augsburg", "https://www.tierheim-augsburg.de")
    ],
    "GLOBAL": [
        ("UNICEF", "https://www.unicef.de"), 
        ("WWF", "https://www.wwf.de")
    ]
}

class QuantumLottoKarmaApp(App):
    def build(self):
        self.is_drawing = False
        self.current_lotto = "6aus49"
        self.current_region = "BAYERN"
        self.letztes_projekt = None
        self.historie = [] # Hier werden die Ziehungen gespeichert

        self.root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))

        # 1. HEADER
        self.root.add_widget(Label(text="VORTEX LOTTO v0.4", font_size=sp(22), bold=True, color=CLR_ACCENT, size_hint_y=None, height=dp(40)))

        # 2. LOTTERIE AUSWAHL
        lotto_grid = GridLayout(cols=4, size_hint_y=None, height=dp(45), spacing=dp(5))
        for l_name in LOTTERIEN.keys():
            btn = ToggleButton(text=l_name, group="lotto", state="down" if l_name == "6aus49" else "normal", font_size=sp(12))
            btn.bind(on_release=lambda x, n=l_name: self.set_lotto(n))
            lotto_grid.add_widget(btn)
        self.root.add_widget(lotto_grid)

        # 3. KUGEL-DISPLAY
        self.ball_row = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        self.ball_labels = [Label(text="?", font_size=sp(24), bold=True, color=(0.4, 0.4, 0.4, 1)) for _ in range(7)]
        for lbl in self.ball_labels: self.ball_row.add_widget(lbl)
        self.root.add_widget(self.ball_row)

        # 4. HISTORIE (Scroll-Liste)
        self.root.add_widget(Label(text="HISTORIE", font_size=sp(12), color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=dp(20)))
        self.history_scroll = ScrollView(size_hint_y=None, height=dp(100))
        self.history_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self.history_list.bind(minimum_height=self.history_list.setter('height'))
        self.history_scroll.add_widget(self.history_list)
        self.root.add_widget(self.history_scroll)

        # 5. REGIONEN & STATUS
        region_grid = GridLayout(cols=3, size_hint_y=None, height=dp(40), spacing=dp(5))
        for r_name in SPENDEN_PROJEKTE.keys():
            btn = ToggleButton(text=r_name, group="region", state="down" if r_name == "BAYERN" else "normal")
            btn.bind(on_release=lambda x, n=r_name: self.set_region(n))
            region_grid.add_widget(btn)
        self.root.add_widget(region_grid)

        self.status_label = Label(text="Quanten-System bereit.", color=CLR_ACCENT, size_hint_y=None, height=dp(30))
        self.root.add_widget(self.status_label)

        # 6. ACTION BUTTONS
        btn_row = BoxLayout(size_hint_y=None, height=dp(70), spacing=dp(10))
        self.start_btn = Button(text="ZIEHUNG", background_color=get_color_from_hex("#0e7490"), bold=True)
        self.start_btn.bind(on_release=self.start_draw)
        karma_btn = Button(text="KARMA", background_color=CLR_RED, bold=True)
        karma_btn.bind(on_release=self.open_karma)
        btn_row.add_widget(self.start_btn)
        btn_row.add_widget(karma_btn)
        self.root.add_widget(btn_row)

        return self.root

    def set_lotto(self, name): self.current_lotto = name
    def set_region(self, name): self.current_region = name

    def open_karma(self, instance):
        projekte = SPENDEN_PROJEKTE.get(self.current_region)
        neues = random.choice(projekte)
        if len(projekte) > 1:
            while neues == self.letztes_projekt: neues = random.choice(projekte)
        self.letztes_projekt = neues
        webbrowser.open(neues[1])

    def start_draw(self, *args):
        if not self.is_drawing:
            self.start_btn.disabled = True
            for lbl in self.ball_labels: lbl.text = "?"
            threading.Thread(target=self.run_logic).start()

    def run_logic(self):
        self.is_drawing = True
        config = LOTTERIEN[self.current_lotto]
        gezogene = []
        
        # Hauptzahlen
        for i in range(config["kugeln"]):
            pool = list(range(1, config["max"] + 1))
            while True:
                val = self.get_q(pool)
                if val not in gezogene:
                    gezogene.append(val)
                    break
            Clock.schedule_once(lambda dt, idx=i, v=val: self.update_ball(idx, v, False))
            time.sleep(0.3)
        
        # Zusatzzahl (falls vorhanden)
        zusatz_val = None
        if config["zusatz"]:
            z_pool = list(range(1, config["z_max"] + 1))
            zusatz_val = self.get_q(z_pool)
            Clock.schedule_once(lambda dt, v=zusatz_val: self.update_ball(6, v, True))
        
        # In Historie speichern
        res_str = f"{self.current_lotto}: " + ", ".join(map(str, sorted(gezogene)))
        if zusatz_val: res_str += f" | {config['zusatz']}: {zusatz_val}"
        Clock.schedule_once(lambda dt: self.add_to_history(res_str))

        self.is_drawing = False
        self.start_btn.disabled = False

    def update_ball(self, idx, v, is_zusatz):
        self.ball_labels[idx].text = str(v)
        self.ball_labels[idx].color = CLR_GOLD if is_zusatz else CLR_ACCENT

    def add_to_history(self, text):
        lbl = Label(text=text, font_size=sp(11), size_hint_y=None, height=dp(20), color=(0.8, 0.8, 0.8, 1))
        self.history_list.add_widget(lbl, index=len(self.history_list.children))

    def get_q(self, pool):
        try:
            api_key = "BfPlcBrXfz5JKtQs0nlTN7OBJx2nGsuI5WUaKtvR"
            url = f"https://quantumnumbers.anu.edu.au/api/v1/random?length=1&type=uint8&apiKey={api_key}"
            r = requests.get(url, timeout=2.0)
            return pool[r.json()['data'][0] % len(pool)]
        except:
            return secrets.choice(pool)

if __name__ == '__main__':
    QuantumLottoKarmaApp().run()
