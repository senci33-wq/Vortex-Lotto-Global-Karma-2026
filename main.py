import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
import random, secrets, requests, threading, time, webbrowser, json, os
from datetime import datetime

# --- SSL FIX ---
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

# --- DESIGN ---
CLR_CARD = get_color_from_hex("#0f172a")
CLR_ACCENT = get_color_from_hex("#22d3ee")
CLR_ACTIVE = get_color_from_hex("#0e7490")
CLR_GOLD = get_color_from_hex("#fbbf24")
CLR_RED = get_color_from_hex("#f43f5e")

SPENDEN_PROJEKTE = {
    "GLOBAL": [
        ("UNICEF", "https://www.unicef.de"), 
        ("WWF", "https://www.wwf.de")
    ],
    "BAYERN": [
        ("Spenden für Bayern", "https://share.google/Xuehkxs9BatunONIq"),
        ("Sternstunden e.V.", "https://www.sternstunden.de"),
        ("LBV Naturschutz", "https://www.lbv.de")
    ],
    "AUGSBURG": [
        ("Zoo Augsburg", "https://www.zoo-augsburg.com"), 
        ("Tierheim", "https://www.tierheim-augsburg.de"),
        ("Fuggerei", "https://www.fuggerei.de")
    ]
}

class QuantumLottoKarmaApp(App):
    def build(self):
        self.is_drawing = False
        self.current_region = "GLOBAL"
        self.quantum_success = True

        self.root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))

        # HEADER
        self.root.add_widget(Label(text="VORTEX LOTTO v0.3", font_size=sp(22), bold=True, color=CLR_ACCENT, size_hint_y=None, height=dp(50)))

        # REGIONEN-AUSWAHL (Jetzt mit BAYERN)
        region_grid = GridLayout(cols=3, size_hint_y=None, height=dp(45), spacing=dp(5))
        for r_name in SPENDEN_PROJEKTE.keys():
            btn = ToggleButton(text=r_name, group="region", 
                               state="down" if r_name == "GLOBAL" else "normal",
                               background_color=CLR_CARD)
            btn.bind(on_release=lambda x, n=r_name: self.set_region(n))
            region_grid.add_widget(btn)
        self.root.add_widget(region_grid)

        self.root.add_widget(Label(size_hint_y=1)) # Spacer

        # KUGELN
        self.ball_row = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        self.ball_labels = [Label(text="?", font_size=sp(26), bold=True, color=(0.3, 0.3, 0.3, 1)) for _ in range(7)]
        for lbl in self.ball_labels: self.ball_row.add_widget(lbl)
        self.root.add_widget(self.ball_row)

        self.status_label = Label(text="Bereit für dein Karma-Los.", color=CLR_ACCENT, size_hint_y=None, height=dp(30))
        self.root.add_widget(self.status_label)

        # AKTIONEN
        btn_row = BoxLayout(size_hint_y=None, height=dp(70), spacing=dp(10))
        start_btn = Button(text="START", background_color=CLR_ACTIVE, bold=True)
        start_btn.bind(on_release=self.start_draw)
        
        karma_btn = Button(text="KARMA SPENDEN", background_color=CLR_RED, bold=True)
        karma_btn.bind(on_release=self.open_karma)
        
        btn_row.add_widget(start_btn)
        btn_row.add_widget(karma_btn)
        self.root.add_widget(btn_row)

        return self.root

    def set_region(self, name):
        self.current_region = name
        self.status_label.text = f"Region: {name} aktiv"

    def open_karma(self, instance):
        projekte = SPENDEN_PROJEKTE.get(self.current_region)
        p = random.choice(projekte)
        self.status_label.text = f"Öffne: {p[0]}"
        webbrowser.open(p[1])

    def start_draw(self, *args):
        if not self.is_drawing:
            threading.Thread(target=self.run_logic).start()

    def run_logic(self):
        self.is_drawing = True
        for i in range(7):
            val = self.get_q(list(range(1, 50)))
            Clock.schedule_once(lambda dt, idx=i, v=val: self.update_ball(idx, v))
            time.sleep(0.2)
        self.is_drawing = False

    def update_ball(self, idx, v):
        self.ball_labels[idx].text = str(v)
        self.ball_labels[idx].color = CLR_ACCENT if idx < 6 else CLR_GOLD

    def get_q(self, pool):
        try:
            api_key = "BfPlcBrXfz5JKtQs0nlTN7OBJx2nGsuI5WUaKtvR"
            url = f"https://quantumnumbers.anu.edu.au/api/v1/random?length=1&type=uint8&apiKey={api_key}"
            r = requests.get(url, timeout=2.5)
            return pool[r.json()['data'][0] % len(pool)]
        except Exception:
            return secrets.choice(pool)

if __name__ == '__main__':
    QuantumLottoKarmaApp().run()
