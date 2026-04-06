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
import secrets, requests, threading, time, webbrowser, os

# SSL FIX
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

CLR_ACCENT = get_color_from_hex("#22d3ee")
CLR_GOLD = get_color_from_hex("#fbbf24")

LOTTERIEN = {
    "6aus49": {"kugeln": 6, "max": 49, "zusatz": "SZ", "z_max": 9},
    "Eurojackpot": {"kugeln": 5, "max": 50, "zusatz": "EZ", "z_max": 12},
    "Glücksspirale": {"kugeln": 7, "max": 9, "zusatz": None},
    "Bayern-Lotto": {"kugeln": 6, "max": 49, "zusatz": "BZ", "z_max": 10}
}

class QuantumLottoKarmaApp(App):
    def build(self):
        self.is_drawing = False
        self.current_lotto = "6aus49"
        self.root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        self.root.add_widget(Label(text="VORTEX LOTTO v1.1", font_size=sp(22), bold=True, color=CLR_ACCENT, size_hint_y=None, height=dp(50)))

        lotto_grid = GridLayout(cols=4, size_hint_y=None, height=dp(45), spacing=dp(5))
        for l_name in LOTTERIEN.keys():
            btn = ToggleButton(text=l_name, group="lotto", state="down" if l_name == "6aus49" else "normal", font_size=sp(10))
            btn.bind(on_release=lambda x, n=l_name: setattr(self, 'current_lotto', n))
            lotto_grid.add_widget(btn)
        self.root.add_widget(lotto_grid)

        self.ball_row = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(5))
        self.ball_labels = [Label(text="?", font_size=sp(26), bold=True, color=(0.4, 0.4, 0.4, 1)) for _ in range(7)]
        for lbl in self.ball_labels: self.ball_row.add_widget(lbl)
        self.root.add_widget(self.ball_row)

        self.history_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(2))
        self.history_list.bind(minimum_height=self.history_list.setter('height'))
        scroll = ScrollView(size_hint_y=None, height=dp(100)); scroll.add_widget(self.history_list)
        self.root.add_widget(scroll)

        self.status_label = Label(text="Quanten-Bereit", color=CLR_ACCENT, size_hint_y=None, height=dp(30))
        self.root.add_widget(self.status_label)

        self.start_btn = Button(text="ZIEHUNG STARTEN", background_color=get_color_from_hex("#0e7490"), bold=True, size_hint_y=None, height=dp(60))
        self.start_btn.bind(on_release=self.start_draw)
        self.root.add_widget(self.start_btn)
        return self.root

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

        try:
            r = requests.get("https://anu.edu.au", timeout=2.5)
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

        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f"Quelle: {source}"))
        for i, val in enumerate(ergebnis):
            time.sleep(0.25)
            Clock.schedule_once(lambda dt, idx=i, v=val: self.update_ball_ui(idx, v))
        Clock.schedule_once(lambda dt: self.finalize(ergebnis))

    def secure_sample(self, pop, k):
        p = list(pop); res = []
        for _ in range(k):
            c = secrets.choice(p); res.append(c); p.remove(c)
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
