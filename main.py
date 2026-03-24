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

# --- HERZSTÜCK: 26 ORGANISATIONEN ---
SPENDEN_PROJEKTE = {
    "GLOBAL": [("UNICEF", "https://www.unicef.de"), ("WWF", "https://www.wwf.de"), ("Ärzte ohne Grenzen", "https://www.aerzte-ohne-grenzen.de"), ("Plan International", "https://www.plan.de"), ("Save the Children", "https://www.savethechildren.de"), ("Oxfam", "https://www.oxfam.de"), ("Greenpeace", "https://www.greenpeace.de"), ("Amnesty International", "https://www.amnesty.de")],
    "NATIONAL": [("NABU", "https://www.nabu.de"), ("DKMS", "https://www.dkms.de"), ("Deutsche Krebshilfe", "https://www.krebshilfe.de"), ("DRK", "https://www.drk.de"), ("Weisser Ring", "https://www.weisser-ring.de"), ("Die Arche", "https://www.kinderprojekt-arche.de"), ("Johanniter", "https://www.johanniter.de"), ("Malteser", "https://www.malteser.de"), ("BUND", "https://www.bund.net")],
    "AUGSBURG": [("Zoo Augsburg", "https://www.zoo-augsburg.com"), ("Tierheim", "https://www.tierheim-augsburg.de"), ("Kartei Not", "https://www.kartei-der-not.de"), ("Bunter Kreis", "https://www.bunter-kreis.de"), ("SKM Augsburg", "https://www.skm-augsburg.de"), ("Puppenkiste", "https://www.augsburger-puppenkiste.de"), ("Hospiz Augsburg", "https://www.hospiz-augsburg.de"), ("Augsburger Tafel", "https://www.augsburger-tafel.de"), ("Fuggerei", "https://www.fuggerei.de")]
}

class QuantumLottoKarmaApp(App):
    def build(self):
        self.is_drawing = False
        self.current_region = "GLOBAL"
        self.current_preset = "6aus49"
        self.quantum_success = False

        self.root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))

        # 1. HEADER
        header = BoxLayout(size_hint_y=None, height=dp(50))
        header.add_widget(Label(text="QUANTUM LOTTO", font_size=sp(22), bold=True, color=CLR_ACCENT))
        self.expert_btn = ToggleButton(text="EXPERT", size_hint_x=None, width=dp(80), background_color=CLR_CARD, color=CLR_GOLD)
        self.expert_btn.bind(on_release=self.toggle_expert)
        header.add_widget(self.expert_btn)
        self.root.add_widget(header)

        # 2. REGIONEN
        region_grid = GridLayout(cols=3, size_hint_y=None, height=dp(40), spacing=dp(5))
        self.reg_btns = {}
        for r_name in SPENDEN_PROJEKTE.keys():
            btn = ToggleButton(text=r_name, group="region", state="down" if r_name == "GLOBAL" else "normal", background_color=CLR_CARD)
            btn.bind(on_release=lambda x, n=r_name: self.set_region(n))
            self.reg_btns[r_name] = btn
            region_grid.add_widget(btn)
        self.root.add_widget(region_grid)

        # 3. SYSTEME
        preset_grid = GridLayout(cols=2, size_hint_y=None, height=dp(85), spacing=dp(5))
        self.pre_btns = {}
        for name in ["6aus49", "EUROJACKPOT", "FREIHEIT+", "GLÜCKSSPIRALE"]:
            btn = Button(text=name, font_size=sp(11), background_color=CLR_CARD, bold=True)
            btn.bind(on_release=lambda x, n=name: self.apply_preset(n))
            self.pre_btns[name] = btn
            preset_grid.add_widget(btn)
        self.root.add_widget(preset_grid)

        # 4. EXPERT INPUTS
        self.expert_section = BoxLayout(orientation='vertical', size_hint_y=None, height=0, opacity=0)
        self.inputs = [TextInput(text="49", multiline=False, input_type='number', background_color=(0.1, 0.1, 0.2, 1), foreground_color=CLR_GOLD) for _ in range(7)]
        for ti in self.inputs: self.expert_section.add_widget(ti)
        self.root.add_widget(self.expert_section)

        self.root.add_widget(Label(size_hint_y=1))

        # 5. KUGELN & QRNG LED
        self.ball_row = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        self.ball_labels = [Label(text="?", font_size=sp(24), bold=True, color=(0.3, 0.3, 0.3, 1)) for _ in range(7)]
        for lbl in self.ball_labels: self.ball_row.add_widget(lbl)
        self.root.add_widget(self.ball_row)

        status_box = BoxLayout(size_hint_y=None, height=dp(30))
        self.qrng_light = Label(text="•", font_size=sp(45), size_hint_x=None, width=dp(40), color=CLR_RED)
        self.status_label = Label(text="Bereit.", color=CLR_ACCENT, bold=True)
        status_box.add_widget(self.qrng_light); status_box.add_widget(self.status_label)
        self.root.add_widget(status_box)

        # 6. HISTORIE & BUTTONS
        self.hist_label = Label(text="", size_hint_y=0.15, font_size=sp(11), color=(0.5, 0.5, 0.5, 1))
        self.root.add_widget(self.hist_label)

        btn_row = BoxLayout(size_hint_y=None, height=dp(65), spacing=dp(10))
        self.start_btn = Button(text="START", background_color=CLR_ACTIVE, bold=True)
        self.start_btn.bind(on_release=self.start_draw)
        karma_btn = Button(text="KARMA", background_color=CLR_RED, bold=True)
        karma_btn.bind(on_release=self.open_karma)
        btn_row.add_widget(self.start_btn); btn_row.add_widget(karma_btn)
        self.root.add_widget(btn_row)

        Clock.schedule_once(self.ui_refresh, 0.1)
        return self.root

    def ui_refresh(self, dt):
        for name, btn in self.reg_btns.items():
            btn.background_color = CLR_ACTIVE if btn.state == 'down' else CLR_CARD
        for name, btn in self.pre_btns.items():
            btn.background_color = CLR_ACTIVE if self.current_preset == name else CLR_CARD

    def kill_kb(self):
        Window.release_all_keyboards()
        for ti in self.inputs: ti.focus = False

    def set_region(self, name):
        self.kill_kb()
        self.current_region = name
        self.ui_refresh(0)

    def apply_preset(self, name):
        self.kill_kb()
        self.current_preset = name
        for i, v in enumerate(LOTTO_PRESETS[name]): self.inputs[i].text = v
        self.ui_refresh(0)

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
            pool = list(range(1, lim+1)) if self.current_preset != "GLÜCKSSPIRALE" else list(range(10))

            while True:
                val = self.get_q(pool)
                if self.current_preset == "EUROJACKPOT":
                    if i < 5 and val not in res[:5]: break
                    if i >= 5 and val not in res[5:]: break
                elif self.current_preset == "GLÜCKSSPIRALE":
                    break
                else:
                    if val not in res: break

            res.append(val)
            Clock.schedule_once(lambda dt, idx=i, v=val: self.update_ball(idx, v))
            time.sleep(0.15)

        time.sleep(0.8)
        Clock.schedule_once(self.finalize_draw)

    def update_ball(self, idx, v):
        lbl = self.ball_labels[idx]
        lbl.text = str(v)
        if (self.current_preset == "6aus49" and idx == 6) or (self.current_preset == "EUROJACKPOT" and idx >= 5):
            lbl.color = CLR_GOLD
        else:
            lbl.color = CLR_ACCENT

    def finalize_draw(self, dt):
        if self.quantum_success:
            self.qrng_light.color = CLR_GREEN
            q_tag = " (Q)"
            self.status_label.text = "Quanten-Kombination verifiziert"
        else:
            self.qrng_light.color = CLR_RED
            q_tag = ""
            self.status_label.text = "Ziehung beendet (Lokal)"

        self.hist_label.text = f"{datetime.now().strftime('%H:%M')} | {' . '.join(map(str, [l.text for l in self.ball_labels]))}{q_tag}\n" + self.hist_label.text
        self.is_drawing = False

    def get_q(self, pool):
        try:
            r = requests.get("https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8", timeout=2.5)
            data = r.json()
            return pool[data['data'][0] % len(pool)]
        except:
            self.quantum_success = False
            return secrets.choice(pool)

    def open_karma(self, instance):
        self.kill_kb()
        p = random.choice(SPENDEN_PROJEKTE.get(self.current_region))
        webbrowser.open(p[1])

if __name__ == '__main__':
    QuantumLottoKarmaApp().run()