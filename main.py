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

# --- FARBEN ---
CLR_BG = get_color_from_hex("#020617")
CLR_ACCENT = get_color_from_hex("#22d3ee")
CLR_GOLD = get_color_from_hex("#fbbf24")
CLR_RED = get_color_from_hex("#f43f5e")

class QuantumLottoKarmaApp(App):
    def build(self):
        self.is_drawing = False
        self.current_lotto = "6aus49"
        self.current_region = "BAYERN" # Standard-Startwert
        self.karma_manager = KarmaManager()

        self.root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Titel
        self.root.add_widget(Label(text="VORTEX LOTTO 1.1.2", font_size=sp(22), bold=True, 
                                   color=CLR_ACCENT, size_hint_y=None, height=dp(40)))

        # 1. LOTTERIE AUSWAHL
        self.lotto_grid = GridLayout(cols=4, size_hint_y=None, height=dp(50), spacing=dp(5))
        for l_name in LOTTERIEN.keys():
            btn = ToggleButton(text=l_name, group="lotto", 
                               state="down" if l_name == "6aus49" else "normal", font_size=sp(9))
            btn.bind(on_release=lambda x, n=l_name: self.set_lotto(n))
            self.lotto_grid.add_widget(btn)
        self.root.add_widget(self.lotto_grid)

        # 2. KUGEL DISPLAY
        self.ball_row = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        self.ball_labels = [Label(text=" ", font_size=sp(26), bold=True) for _ in range(7)]
        for lbl in self.ball_labels: self.ball_row.add_widget(lbl)
        self.root.add_widget(self.ball_row)

        # 3. HISTORIE
        self.history_scroll = ScrollView(size_hint_y=None, height=dp(100))
        self.history_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self.history_list.bind(minimum_height=self.history_list.setter('height'))
        self.history_scroll.add_widget(self.history_list)
        self.root.add_widget(self.history_scroll)

        # 4. DYNAMISCHES REGIONEN-GRID (In ScrollView für viele Länder)
        self.region_scroll = ScrollView(size_hint_y=None, height=dp(80))
        self.region_grid = GridLayout(cols=3, size_hint_y=None, spacing=dp(5))
        self.region_grid.bind(minimum_height=self.region_grid.setter('height'))
        self.region_scroll.add_widget(self.region_grid)
        self.root.add_widget(self.region_scroll)

        self.status_label = Label(text="System bereit.", color=CLR_ACCENT, size_hint_y=None, height=dp(30))
        self.root.add_widget(self.status_label)

        # 5. ACTION BUTTONS
        btn_row = BoxLayout(size_hint_y=None, height=dp(70), spacing=dp(10))
        self.start_btn = Button(text="ZIEHUNG", background_color=get_color_from_hex("#0e7490"), bold=True)
        self.start_btn.bind(on_release=self.start_draw)
        
        karma_btn = Button(text="KARMA", background_color=CLR_RED, bold=True)
        karma_btn.bind(on_release=self.open_karma)
        
        btn_row.add_widget(self.start_btn)
        btn_row.add_widget(karma_btn)
        self.root.add_widget(btn_row)

        # Start Online-Abfrage
        threading.Thread(target=self.fetch_remote_projects, daemon=True).start()
        
        return self.root

    def fetch_remote_projects(self):
        try:
            url = "https://raw.githubusercontent.com/senci33-wq/Vortex-Lotto-Global-Karma-2026/main/projekte.json"
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                self.karma_manager.update_daten(data)
                # Buttons im Haupt-Thread bauen
                Clock.schedule_once(lambda dt: self.build_region_buttons(data.keys()))
        except:
            self.status_label.text = "Offline: Fallback-Projekte aktiv."

    def build_region_buttons(self, keys):
        self.region_grid.clear_widgets()
        # Alphabetisch sortieren für bessere Übersicht
        for k in sorted(keys):
            btn = ToggleButton(text=str(k), group="region", 
                               state="down" if k == self.current_region else "normal", 
                               size_hint_y=None, height=dp(35), font_size=sp(10))
            btn.bind(on_release=lambda x, n=k: self.set_region(n))
            self.region_grid.add_widget(btn)

    def set_lotto(self, name):
        self.current_lotto = name
        for lbl in self.ball_labels: 
            lbl.text = " "
        self.status_label.text = f"Modus: {name}"

    def set_region(self, name):
        self.current_region = name
        self.status_label.text = f"Region: {name}"

    def open_karma(self, instance):
        # Holt Projekt-Tupel (Name, URL) aus dem KarmaManager
        projekt = self.karma_manager.ziehe_projekt(self.current_region)
        if projekt:
            webbrowser.open(projekt[1])
            self.status_label.text = f"Karma: {projekt[0]}"

    def start_draw(self, *args):
        if not self.is_drawing:
            self.start_btn.disabled = True
            for lbl in self.ball_labels: lbl.text = "·"
            threading.Thread(target=self.run_logic).start()

    def run_logic(self):
        self.is_drawing = True
        config = LOTTERIEN[self.current_lotto]
        h_count = config["kugeln"]
        z_count = config.get("z_kugeln", 0)
        
        # Hauptzahlen
        gezogene_h = []
        for i in range(h_count):
            while True:
                val = self.get_q(list(range(1, config["max"] + 1)))
                if val not in gezogene_h:
                    gezogene_h.append(val)
                    break
            Clock.schedule_once(lambda dt, idx=i, v=val: self.update_ui_ball(idx, v, False))
            time.sleep(0.3)

        # Zusatzzahlen (ohne Lücke)
        gezogene_z = []
        for j in range(z_count):
            while True:
                val = self.get_q(list(range(1, config["z_max"] + 1)))
                if val not in gezogene_z:
                    gezogene_z.append(val)
                    break
            Clock.schedule_once(lambda dt, idx=h_count+j, v=val: self.update_ui_ball(idx, v, True))
            time.sleep(0.3)

        # Überflüssige Kugeln leeren
        for k in range(h_count + z_count, 7):
            Clock.schedule_once(lambda dt, idx=k: self.update_ui_ball(idx, "", False))

        # Historie füllen
        res = f"{self.current_lotto}: " + ", ".join(map(str, sorted(gezogene_h)))
        if gezogene_z:
            res += f" | {config['zusatz']}: " + ", ".join(map(str, sorted(gezogene_z)))
        Clock.schedule_once(lambda dt: self.add_to_history(res))
        
        self.is_drawing = False
        Clock.schedule_once(lambda dt: self.enable_ui())

    def update_ui_ball(self, idx, v, is_z):
        self.ball_labels[idx].text = str(v)
        self.ball_labels[idx].color = CLR_GOLD if is_z else CLR_ACCENT

    def enable_ui(self):
        self.start_btn.disabled = False
        self.status_label.text = "Ziehung beendet."

    def add_to_history(self, text):
        lbl = Label(text=text, font_size=sp(10), size_hint_y=None, height=dp(25), color=(0.7,0.7,0.7,1))
        self.history_list.add_widget(lbl, index=0)

    def get_q(self, pool):
        try:
            # Quanten-Zufall API
            r = requests.get("https://quantumnumbers.anu.edu.au/api/v1/random?length=1&type=uint8&apiKey=BfPlcBrXfz5JKtQs0nlTN7OBJx2nGsuI5WUaKtvR", timeout=1.5)
            return pool[r.json()['data'][0] % len(pool)]
        except:
            return secrets.choice(pool)

