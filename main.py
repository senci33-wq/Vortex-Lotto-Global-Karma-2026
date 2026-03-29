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
CLR_ACCENT = get_color_from_hex("#22d3ee")
CLR_GOLD = get_color_from_hex("#fbbf24")
CLR_RED = get_color_from_hex("#f43f5e")

# --- LOTTERIE KONFIGURATION ---
# z_kugeln definiert, wie viele Zusatzzahlen gezogen werden
LOTTERIEN = {
    "6aus49": {"kugeln": 6, "max": 49, "zusatz": "SZ", "z_kugeln": 1, "z_max": 9},
    "Eurojackpot": {"kugeln": 5, "max": 50, "zusatz": "EZ", "z_kugeln": 2, "z_max": 12},
    "Glücksspirale": {"kugeln": 7, "max": 9, "zusatz": None, "z_kugeln": 0, "z_max": 0},
    "🗽Freiheit": {"kugeln": 7, "max": 38, "zusatz": None, "z_kugeln": 0, "z_max": 0}
}

class KarmaManager:
    def __init__(self):
        self.projekte_pool = {}
        self.verfuegbare_stapel = {}

    def update_daten(self, neue_daten):
        self.projekte_pool = neue_daten
        self.verfuegbare_stapel = {r: list(p) for r, p in neue_daten.items()}
        for r in self.verfuegbare_stapel: random.shuffle(self.verfuegbare_stapel[r])

    def ziehe_projekt(self, region):
        if region not in self.verfuegbare_stapel or not self.verfuegbare_stapel[region]:
            if region in self.projekte_pool:
                self.verfuegbare_stapel[region] = list(self.projekte_pool[region])
                random.shuffle(self.verfuegbare_stapel[region])
            else: return ("Global Karma Fund", "https://google.com")
        return self.verfuegbare_stapel[region].pop()

class QuantumLottoKarmaApp(App):
    def build(self):
        self.is_drawing = False
        self.current_lotto = "6aus49"
        self.current_region = "BAYERN"
        self.karma_manager = KarmaManager()
        
        # Fallback Daten
        self.karma_manager.update_daten({
            "BAYERN": [("Sternstunden e.V.", "https://www.sternstunden.de")],
            "GLOBAL": [("UNICEF", "https://www.unicef.de")],
            "AUGSBURG": [("Bunter Kreis", "https://www.bunter-kreis.de")]
        })

        threading.Thread(target=self.fetch_remote_projects, daemon=True).start()

        self.root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))

        # 1. HEADER
        self.root.add_widget(Label(text="VORTEX LOTTO v0.7", font_size=sp(22), bold=True, color=CLR_ACCENT, size_hint_y=None, height=dp(40)))

        # 2. LOTTERIE AUSWAHL
        lotto_grid = GridLayout(cols=4, size_hint_y=None, height=dp(45), spacing=dp(5))
        for l_name in LOTTERIEN.keys():
            btn = ToggleButton(text=l_name, group="lotto", state="down" if l_name == "6aus49" else "normal", font_size=sp(10))
            btn.bind(on_release=lambda x, n=l_name: self.set_lotto(n))
            lotto_grid.add_widget(btn)
        self.root.add_widget(lotto_grid)

        # 3. KUGEL-DISPLAY
        self.ball_row = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        self.ball_labels = [Label(text=" ", font_size=sp(26), bold=True) for _ in range(7)]
        for lbl in self.ball_labels: self.ball_row.add_widget(lbl)
        self.root.add_widget(self.ball_row)

        # 4. HISTORIE
        self.root.add_widget(Label(text="LETZTE ZIEHUNGEN", font_size=sp(11), color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=dp(15)))
        self.history_scroll = ScrollView(size_hint_y=None, height=dp(100))
        self.history_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self.history_list.bind(minimum_height=self.history_list.setter('height'))
        self.history_scroll.add_widget(self.history_list)
        self.root.add_widget(self.history_scroll)

        # 5. REGIONEN & STATUS
        region_grid = GridLayout(cols=3, size_hint_y=None, height=dp(40), spacing=dp(5))
        for r_name in ["BAYERN", "AUGSBURG", "GLOBAL"]:
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

    def fetch_remote_projects(self):
        try:
            url = "https://raw.githubusercontent.com/senci33-wq/Vortex-Lotto-Global-Karma-2026/main/projekte.json"
            r = requests.get(url, timeout=5)
            if r.status_code == 200: self.karma_manager.update_daten(r.json())
        except: pass

    def set_lotto(self, name):
        self.current_lotto = name
        for lbl in self.ball_labels: lbl.text = " "

    def set_region(self, name): self.current_region = name

    def open_karma(self, instance):
        p_name, p_url = self.karma_manager.ziehe_projekt(self.current_region)
        webbrowser.open(p_url)
        self.status_label.text = f"Karma: {p_name}"

    def start_draw(self, *args):
        if not self.is_drawing:
            self.start_btn.disabled = True
            for lbl in self.ball_labels: 
                lbl.text = "·"
                lbl.color = (0.4, 0.4, 0.4, 1)
            threading.Thread(target=self.run_logic).start()

    def run_logic(self):
        self.is_drawing = True
        config = LOTTERIEN[self.current_lotto]
        gezogene_haupt = []
        gezogene_zusatz = []

        # 1. Hauptzahlen
        for i in range(config["kugeln"]):
            pool = list(range(1, config["max"] + 1))
            while True:
                val = self.get_q(pool)
                if val not in gezogene_haupt:
                    gezogene_haupt.append(val)
                    break
            Clock.schedule_once(lambda dt, idx=i, v=val: self.update_ball(idx, v, False))
            time.sleep(0.3)

        # 2. Zusatzzahlen (EZ, SZ etc.)
        if config.get("z_kugeln", 0) > 0:
            z_pool_base = list(range(1, config["z_max"] + 1))
            for j in range(config["z_kugeln"]):
                while True:
                    z_val = self.get_q(z_pool_base)
                    if z_val not in gezogene_zusatz:
                        gezogene_zusatz.append(z_val)
                        break
                # Berechne Position: Direkt nach den Hauptzahlen
                pos = config["kugeln"] + j
                Clock.schedule_once(lambda dt, p=pos, v=z_val: self.update_ball(p, v, True))
                time.sleep(0.3)

        # UI Cleanup: Alle restlichen Kugeln (falls vorhanden) leeren
        for k in range(len(gezogene_haupt) + len(gezogene_zusatz), 7):
            Clock.schedule_once(lambda dt, idx=k: self.update_ball(idx, None, False))

        # Historie
        res_str = f"{self.current_lotto}: " + ", ".join(map(str, sorted(gezogene_haupt)))
        if gezogene_zusatz:
            res_str += f" | {config['zusatz']}: " + ", ".join(map(str, sorted(gezogene_zusatz)))
        Clock.schedule_once(lambda dt: self.add_to_history(res_str))

        self.is_drawing = False
        Clock.schedule_once(lambda dt: self.enable_button())

    def enable_button(self):
        self.start_btn.disabled = False
        self.status_label.text = "Quanten-Ziehung abgeschlossen."

    def update_ball(self, idx, v, is_zusatz):
        if idx < len(self.ball_labels):
            self.ball_labels[idx].text = str(v) if v is not None else ""
            self.ball_labels[idx].color = CLR_GOLD if is_zusatz else CLR_ACCENT

    def add_to_history(self, text):
        lbl = Label(text=text, font_size=sp(10), size_hint_y=None, height=dp(25), color=(0.7, 0.7, 0.7, 1))
        self.history_list.add_widget(lbl, index=len(self.history_list.children))

    def get_q(self, pool):
        try:
            api_key = "BfPlcBrXfz5JKtQs0nlTN7OBJx2nGsuI5WUaKtvR"
            url = f"https://quantumnumbers.anu.edu.au/api/v1/random?length=1&type=uint8&apiKey={api_key}"
            r = requests.get(url, timeout=1.5)
            return pool[r.json()['data'][0] % len(pool)]
        except: return secrets.choice(pool)

if __name__ == '__main__':
    QuantumLottoKarmaApp().run()
