import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
import random, secrets, requests, threading, time, webbrowser, os

# --- SSL FIX FÜR ANDROID ---
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

# --- DESIGN FARBEN ---
CLR_BG = get_color_from_hex("#020617")
CLR_CARD = get_color_from_hex("#0f172a")
CLR_ACCENT = get_color_from_hex("#22d3ee")
CLR_GOLD = get_color_from_hex("#fbbf24")
CLR_RED = get_color_from_hex("#f43f5e")

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
        self.current_region = "BAYERN"
        self.letztes_projekt = None # Speicher für die Anti-Wiederholung

        self.root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))

        # 1. HEADER
        self.root.add_widget(Label(
            text="VORTEX LOTTO v0.4", 
            font_size=sp(22), 
            bold=True, 
            color=CLR_ACCENT, 
            size_hint_y=None, 
            height=dp(50)
        ))

        # 2. REGIONEN-AUSWAHL
        region_grid = GridLayout(cols=3, size_hint_y=None, height=dp(45), spacing=dp(5))
        for r_name in SPENDEN_PROJEKTE.keys():
            btn = ToggleButton(
                text=r_name, 
                group="region", 
                state="down" if r_name == "BAYERN" else "normal",
                background_color=CLR_CARD
            )
            btn.bind(on_release=lambda x, n=r_name: self.set_region(n))
            region_grid.add_widget(btn)
        self.root.add_widget(region_grid)

        self.root.add_widget(Label(size_hint_y=1)) 

        # 3. LOTTO-KUGELN (7 Stück)
        self.ball_row = BoxLayout(size_hint_y=None, height=dp(65), spacing=dp(5))
        self.ball_labels = [
            Label(text="?", font_size=sp(30), bold=True, color=(0.4, 0.4, 0.4, 1)) 
            for _ in range(7)
        ]
        for lbl in self.ball_labels: self.ball_row.add_widget(lbl)
        self.root.add_widget(self.ball_row)

        self.status_label = Label(
            text="Bereit für die Quanten-Ziehung.", 
            color=CLR_ACCENT, 
            size_hint_y=None, 
            height=dp(40)
        )
        self.root.add_widget(self.status_label)

        # 4. AKTIONS-BUTTONS
        btn_row = BoxLayout(size_hint_y=None, height=dp(75), spacing=dp(10))
        
        self.start_btn = Button(
            text="ZIEHUNG STARTEN", 
            background_color=get_color_from_hex("#0e7490"), 
            bold=True
        )
        self.start_btn.bind(on_release=self.start_draw)
        
        karma_btn = Button(
            text="KARMA PROJEKT", 
            background_color=CLR_RED, 
            bold=True
        )
        karma_btn.bind(on_release=self.open_karma)
        
        btn_row.add_widget(self.start_btn)
        btn_row.add_widget(karma_btn)
        self.root.add_widget(btn_row)

        return self.root

    def set_region(self, name):
        self.current_region = name
        self.status_label.text = f"Region gewechselt zu: {name}"

    def open_karma(self, instance):
        projekte = SPENDEN_PROJEKTE.get(self.current_region)
        
        # --- ANTI-WIEDERHOLUNGS-LOGIK ---
        if len(projekte) > 1:
            neues_projekt = random.choice(projekte)
            # Ziehe so lange neu, bis es ein anderes Projekt als zuvor ist
            while neues_projekt == self.letztes_projekt:
                neues_projekt = random.choice(projekte)
        else:
            neues_projekt = projekte[0]

        self.letztes_projekt = neues_projekt
        webbrowser.open(neues_projekt[1])
        self.status_label.text = f"Projekt geöffnet: {neues_projekt[0]}"

    def start_draw(self, *args):
        if not self.is_drawing:
            self.start_btn.disabled = True
            # Reset der Kugeln
            for lbl in self.ball_labels: lbl.text = "?"
            threading.Thread(target=self.run_logic).start()

    def run_logic(self):
        self.is_drawing = True
        gezogene_zahlen = []
        
        for i in range(7):
            pool = list(range(1, 50))
            
            # --- DUBLETTEN-CHECK ---
            while True:
                val = self.get_q(pool)
                # Nur die ersten 6 Zahlen (Lottozahlen) dürfen nicht doppelt sein
                if i < 6:
                    if val not in gezogene_zahlen:
                        gezogene_zahlen.append(val)
                        break
                else:
                    # Die 7. Zahl (Superzahl) darf alles sein
                    break
            
            Clock.schedule_once(lambda dt, idx=i, v=val: self.update_ball(idx, v))
            time.sleep(0.3)
            
        self.status_label.text = "Ziehung erfolgreich abgeschlossen!"
        self.is_drawing = False
        self.start_btn.disabled = False

    def update_ball(self, idx, v):
        self.ball_labels[idx].text = str(v)
        self.ball_labels[idx].color = CLR_ACCENT if idx < 6 else CLR_GOLD

    def get_q(self, pool):
        try:
            # Quanten-Zahlen API (ANU)
            api_key = "BfPlcBrXfz5JKtQs0nlTN7OBJx2nGsuI5WUaKtvR"
            url = f"https://quantumnumbers.anu.edu.au/api/v1/random?length=1&type=uint8&apiKey={api_key}"
            r = requests.get(url, timeout=2.0)
            return pool[r.json()['data'][0] % len(pool)]
        except:
            # Backup: Sicherer Zufall, falls API offline
            return secrets.choice(pool)

if __name__ == '__main__':
    QuantumLottoKarmaApp().run()
