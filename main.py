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
import random, requests, threading, time, webbrowser, os

# --- SSL FIX ---
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

# --- DESIGN ---
CLR_BG = get_color_from_hex("#020617")
CLR_CARD = get_color_from_hex("#0f172a")
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
        self.projekte_pool = {} 
        self.verfuegbare_stapel = {} 

    def update_daten(self, neue_daten):
        self.projekte_pool = neue_daten
        for region in neue_daten:
            stapel = list(neue_daten[region])
            random.shuffle(stapel)
            self.verfuegbare_stapel[region] = stapel

    def ziehe_projekt(self, region):
        if region not in self.verfuegbare_stapel or not self.verfuegbare_stapel[region]:
            if region in self.projekte_pool and self.projekte_pool[region]:
                self.verfuegbare_stapel[region] = list(self.projekte_pool[region])
                random.shuffle(self.verfuegbare_stapel[region])
            else: return ("Standard-Projekt", "https://google.com")
        return self.verfuegbare_stapel[region].pop()

class QuantumLottoKarmaApp(App):
    def build(self):
        self.is_drawing = False
        self.current_lotto = "6aus49"
        self.current_region = "BAYERN"
        self.karma_manager = KarmaManager()
        
        self.karma_manager.update_daten({
            "BAYERN": [["Sternstunden e.V.", "https://sternstunden.de"]],
            "GLOBAL": [["UNICEF", "https://unicef.de"]],
            "AUGSBURG": [["Zoo Augsburg", "https://zoo-augsburg.com"]]
        })

        self.root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))

        header_btn = Button(text="VORTEX LOTTO v0.9", font_size=sp(22), bold=True, color=CLR_ACCENT, background_color=(0,0,0,0), size_hint_y=None, height=dp(50))
        header_btn.bind(on_release=self.show_info_popup)
        self.root.add_widget(header_btn)

        lotto_grid = GridLayout(cols=4, size_hint_y=None, height=dp(45), spacing=dp(5))
        for l_name in LOTTERIEN.keys():
            btn = ToggleButton(text=l_name, group="lotto", state="down" if l_name == "6aus49" else "normal", font_size=sp(10))
            btn.bind(on_release=lambda x, n=l_name: self.set_lotto(n))
            lotto_grid.add_widget(btn)
        self.root.add_widget(lotto_grid)

        self.ball_row = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        self.ball_labels = [Label(text="?", font_size=sp(26), bold=True, color=(0.4, 0.4, 0.4, 1)) for _ in range(7)]
        for lbl in self.ball_labels: self.ball_row.add_widget(lbl)
        self.root.add_widget(self.ball_row)

        self.root.add_widget(Label(text="HISTORIE", font_size=sp(11), color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=dp(15)))
        self.history_scroll = ScrollView(size_hint_y=None, height=dp(100))
        self.history_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self.history_list.bind(minimum_height=self.history_list.setter('height'))
        self.history_scroll.add_widget(self.history_list)
        self.root.add_widget(self.history_scroll)

        region_grid = GridLayout(cols=3, size_hint_y=None, height=dp(40), spacing=dp(5))
        for r_name in ["BAYERN", "AUGSBURG", "GLOBAL"]:
            btn = ToggleButton(text=r_name, group="region", state="down" if r_name == "BAYERN" else "normal")
            btn.bind(on_release=lambda x, n=r_name: self.set_region(n))
            region_grid.add_widget(btn)
        self.root.add_widget(region_grid)

        self.status_label = Label(text="System bereit...", color=CLR_ACCENT, size_hint_y=None, height=dp(30))
        self.root.add_widget(self.status_label)

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
    def set_status_safe(self, text): Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', text))

    def start_draw(self, *args):
        if not self.is_drawing:
            self.is_drawing = True
            self.start_btn.disabled = True
            for lbl in self.ball_labels: 
                lbl.text = "?"
                lbl.color = (0.4, 0.4, 0.4, 1)
            threading.Thread(target=self.run_logic, daemon=True).start()

    def run_logic(self):
        cfg = LOTTERIEN[self.current_lotto]
        ergebnis = []

        # --- SPEZIAL-LOGIK EUROJACKPOT ---
        if self.current_lotto == "Eurojackpot":
            haupt = random.sample(range(1, 51), 5) # 5 aus 50 ohne Doppelte
            extra = random.sample(range(1, 13), 2) # 2 aus 12 ohne Doppelte
            ergebnis = haupt + extra # Unsortiert zusammengefügt

        # --- SPEZIAL-LOGIK GLÜCKSSPIRALE ---
        elif self.current_lotto == "Glücksspirale":
            # 7 Stellen 0-9, Doppelte sind hier explizit erlaubt (Losnummer)
            ergebnis = [random.randint(0, 9) for _ in range(7)]

        # --- STANDARD-LOGIK (6aus49, etc.) ---
        else:
            ergebnis = random.sample(range(1, cfg["max"] + 1), cfg["kugeln"])
            if cfg["zusatz"]:
                ergebnis.append(random.randint(0, cfg["z_max"]))

        # --- UI UPDATE (Schrittweise Anzeige) ---
        for i, zahl in enumerate(ergebnis):
            time.sleep(0.2) # Kleiner Verzögerungs-Effekt
            Clock.schedule_once(lambda dt, idx=i, val=zahl: self.update_ball_ui(idx, val))

        Clock.schedule_once(lambda dt: self.finalize_draw(ergebnis))

    def update_ball_ui(self, index, wert):
        if index < len(self.ball_labels):
            self.ball_labels[index].text = str(wert)
            # Eurozahlen beim Eurojackpot gold markieren
            if self.current_lotto == "Eurojackpot" and index >= 5:
                self.ball_labels[index].color = CLR_GOLD
            else:
                self.ball_labels[index].color = (1, 1, 1, 1)

    def finalize_draw(self, zahlen):
        self.is_drawing = False
        self.start_btn.disabled = False
        self.set_status_safe(f"{self.current_lotto} bereit.")
        
        # In Historie schreiben
        res_text = ", ".join(map(str, zahlen))
        h_lbl = Label(text=f"{self.current_lotto}: {res_text}", size_hint_y=None, height=dp(25), font_size=sp(11))
        self.history_list.add_widget(h_lbl, index=len(self.history_list.children))

    def open_karma(self, instance):
        projekt = self.karma_manager.ziehe_projekt(self.current_region)
        webbrowser.open(projekt[1])
        self.status_label.text = f"Karma: {projekt[0]}"

    def show_info_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        lbl = Label(text="Vortex Lotto Karma Project\nNon-Profit Tool für Zufallswerte.\nEntwickler: senci33-wq", halign='center')
        close_btn = Button(text="Schließen", size_hint_y=None, height=dp(40))
        content.add_widget(lbl); content.add_widget(close_btn)
        popup = Popup(title="Info", content=content, size_hint=(0.8, 0.5))
        close_btn.bind(on_release=popup.dismiss); popup.open()

if __name__ == '__main__':
    QuantumLottoKarmaApp().run()
