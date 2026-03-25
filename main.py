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

# --- SSL FIX FÜR ANDROID ---
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

# --- DESIGN ---
CLR_CARD = get_color_from_hex("#0f172a")
CLR_ACCENT = get_color_from_hex("#22d3ee")
CLR_ACTIVE = get_color_from_hex("#0e7490")
CLR_GOLD = get_color_from_hex("#fbbf24")
CLR_GREEN = get_color_from_hex("#22c55e")
CLR_RED = get_color_from_hex("#f43f5e")

LOTTO_PRESETS = {
    "6aus49": ["49", "49", "49", "49", "49", "49", "10"],
    "EUROJACKPOT": ["50", "50", "50", "50", "50", "12", "12"],
    "FREIHEIT+": ["38", "38", "38", "38", "38", "38", "38"],
    "GLÜCKSSPIRALE": ["9", "9", "9", "9", "9", "9", "9"]
}

SPENDEN_PROJEKTE = {
    "GLOBAL": [("UNICEF", "https://www.unicef.de"), ("WWF", "https://www.wwf.de"), ("Ärzte ohne Grenzen", "https://www.aerzte-ohne-grenzen.de")],
    "NATIONAL": [("NABU", "https://www.nabu.de"), ("DKMS", "https://www.dkms.de"), ("DRK", "https://www.drk.de")],
    "AUGSBURG": [("Zoo Augsburg", "https://www.zoo-augsburg.com"), ("Tierheim", "https://www.tierheim-augsburg.de"), ("Fuggerei", "https://www.fuggerei.de")]
}

class QuantumLottoKarmaApp(App):
    def build(self):
        self.is_drawing = False
        self.current_region = "GLOBAL"
        self.current_preset = "6aus49"
        self.quantum_success = False

        self.root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))

        # HEADER
        header = BoxLayout(size_hint_y=None, height=dp(50))
        header.add_widget(Label(text="QUANTUM LOTTO", font_size=sp(22), bold=True, color=CLR_ACCENT))
        self.expert_btn = ToggleButton(text="EXPERT", size_hint_x=None, width=dp(80), background_color=CLR_CARD, color=CLR_GOLD)
        self.expert_btn.bind(on_release=self.toggle_expert)
        header.add_widget(self.expert_btn)
        self.root.add_widget(header)

        # REGIONEN
        region_grid = GridLayout(cols=3, size_hint_y=None, height=dp(40), spacing=dp(5))
        self.reg_btns = {}
        for r_name in SPENDEN_PROJEKTE.keys():
            btn = ToggleButton(text=r_name, group="region", state="down" if r_name == "GLOBAL" else "normal", background_color=CLR_CARD)
            btn.bind(on_release=lambda x, n=r_name: self.set_region(n))
            self.reg_btns[r_name] = btn
            region_grid.add_widget(btn)
        self.root.add_widget(region_grid)

        # SYSTEME
        preset_grid = GridLayout(cols=2, size_hint_y=None, height=dp(85), spacing=dp(5))
        self.pre_btns = {}
        for name in ["6aus49", "EUROJACKPOT", "FREIHEIT+", "GLÜCKSSPIRALE"]:
            btn = Button(text=name, font_size=sp(11), background_color=CLR_CARD, bold=True)
            btn.bind(on_release=lambda x, n=name: self.apply_preset(n))
            self.pre_btns[name] = btn
            preset_grid.add_widget(btn)
        self.root.add_widget(preset_grid)

        # EXPERT INPUTS
        self.expert_section = BoxLayout(orientation='vertical', size_hint_y=None, height=0, opacity=0)
        self.inputs = [TextInput(text="49", multiline=False, input_type='number', background_color=(0.1, 0.1, 0.2, 1), foreground_color=CLR_GOLD) for _ in range(7)]
        for ti in self.inputs: self.expert_section.add_widget(ti)
        self.root.add_widget(self.expert_section)

        self.root.add_widget(Label(size_hint_y=1))

        # KUGELN
        self.ball_row = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        self.ball_labels = [Label(text="?", font_size=sp(24), bold=True, color=(0.3, 0.3, 0.3, 1)) for _ in range(7)]
        for lbl in self.ball_labels: self.ball_row.add_widget(lbl)
        self.root.add_widget(self.ball_row)

        status_box = BoxLayout(size_hint_y=None, height=dp(30))
        self.qrng_light = Label(text="•", font_size=sp(45), size_hint_x=None, width=dp(40), color=CLR_RED)
        self.status_label = Label(text="Bereit.", color=CLR_ACCENT, bold=True)
        status_box.add_widget(self.qrng_light); status_box.add_widget(self.status_label)
        self.root.add_widget(status_box)

        # BUTTONS
        btn_row = BoxLayout(size_hint_y=None, height=dp(65), spacing=dp(10))
        self.start_btn = Button(text="START", background_color=CLR_ACTIVE, bold=True)
        self.start_btn.bind(on_release=self.start_draw)
        karma_btn = Button(text="KARMA", background_color=CLR_RED, bold=True)
        karma_btn.bind(on_release=self.open_karma)
        btn_row.add_widget(self.start_btn); btn_row.add_widget(karma_btn)
        self.root.add_widget(btn_row)

        return self.root

    def kill_kb(self):
        Window.release_all_keyboards()
        for ti in self.inputs: ti.focus = False

    def set_region(self, name):
        self.kill_kb()
        self.current_region = name

    def apply_preset(self, name):
        self.kill_kb()
        self.current_preset = name
        for i, v in enumerate(LOTTO_PRESETS[name]): self.inputs[i].text = v

    def toggle_expert(self, instance):
        self.kill_kb()
        self.expert_section.height = dp(260) if instance.state == 'down' else 0
        self.expert_section.opacity = 1 if instance.state == 'down' else 0

    def start_draw(self, *args):
        self.kill_kb()
        if not self.is_drawing:
            self.qrng_light.color = CLR_RED
            self.status_label.text = "Quanten-Pool wird geladen..."
            self.quantum_success = True
            threading.Thread(target=self.run_logic).start()

    def run_logic(self):
        self.is_drawing = True
        res = []
        for i in range(7):
            lim = int(self.inputs[i].text) if self.inputs[i].text.isdigit() else 49
            pool = list(range(1, lim+1))
            val = self.get_q(pool)
            res.append(val)
            Clock.schedule_once(lambda dt, idx=i, v=val: self.update_ball(idx, v))
            time.sleep(0.15)
        self.is_drawing = False

    def update_ball(self, idx, v):
        self.ball_labels[idx].text = str(v)
        self.ball_labels[idx].color = CLR_ACCENT

    def get_q(self, pool):
        try:
            # Offizielle v1 API mit deinem Key
            api_key = "BfPlcBrXfz5JKtQs0nlTN7OBJx2nGsuI5WUaKtvR"
            url = f"https://quantumnumbers.anu.edu.au/api/v1/random?length=1&type=uint8&apiKey={api_key}"
            r = requests.get(url, timeout=2.5)
            return pool[r.json()['data'][0] % len(pool)]
        except Exception:
            self.quantum_success = False
            return secrets.choice(pool)

    def open_karma(self, instance):
        self.kill_kb()
        p = random.choice(SPENDEN_PROJEKTE.get(self.current_region))
        webbrowser.open(p[1])

if __name__ == '__main__':
    QuantumLottoKarmaApp().run()
