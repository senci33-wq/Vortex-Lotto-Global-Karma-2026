import os, json, re, threading, requests, shutil
import numpy as np
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock, mainthread
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

T = {"bg": "#020617", "ej": "#22d3ee", "lotto": "#10b981", "gs": "#fbbf24", "acc": "#f43f5e", "white": "#ffffff"}

class VortexUltraApp(App):
    def build(self):
        Window.softinput_mode = 'pan'
        Window.clearcolor = get_color_from_hex(T["bg"])
        self.icon = "icon.png"
        self.db_path = "vortex_master_db.json"
        
        self.cf = {
            "EJ": {"n": "Eurojackpot", "c": T["ej"], "mc": 5, "mm": 50, "ec": 2, "em": 12, "u": "https://www.lotto-bayern.de/eurojackpot/gewinnzahlen"},
            "L649": {"n": "Lotto 6aus49", "c": T["lotto"], "mc": 6, "mm": 49, "ec": 1, "em": 9, "u": "https://www.lotto-bayern.de/lotto6aus49/gewinnzahlen"},
            "GS": {"n": "Glücksspirale", "c": T["gs"], "mc": 7, "mm": 9, "ec": 0, "em": 0, "u": "https://www.lotto-bayern.de/gluecksspirale/gewinnzahlen"},
            "FR": {"n": "Freiheit+", "c": T["ej"], "mc": 7, "mm": 38, "ec": 0, "em": 0, "u": "https://lotto.web.de/freiheitplus/zahlen-quoten"}
        }
        self.data = self.convert_db(self.load_raw())
        
        root = BoxLayout(orientation='vertical', padding=10, spacing=8)
        head = BoxLayout(size_hint_y=None, height=60, spacing=10)
        head.add_widget(Label(text="VORTEX SAFE V8.8", font_size='22sp', bold=True, color=get_color_from_hex(T["ej"])))
        self.s_btn = Button(text="SYNC", size_hint_x=0.3, background_color=get_color_from_hex(T["acc"]), bold=True)
        self.s_btn.bind(on_release=lambda x: self.sync())
        head.add_widget(self.s_btn); root.add_widget(head)

        self.tp = TabbedPanel(do_default_tab=False, background_color=(0,0,0,0))
        self.lbs, self.ips = {}, {}
        self.custom_inputs = {}

        for k, c in self.cf.items():
            tab = TabbedPanelItem(text=k)
            lay = BoxLayout(orientation='vertical', padding=[5, 10, 5, 5], spacing=10)
            
            ctrl = BoxLayout(orientation='vertical', size_hint_y=None, height=130, spacing=8)
            row = BoxLayout(size_hint_y=None, height=60, spacing=5)
            self.ips[k] = TextInput(hint_text="Folge...", multiline=False, size_hint_x=0.8, font_size='18sp', padding=[10, 12, 10, 12])
            a_btn = Button(text="+", size_hint_x=0.2, background_color=get_color_from_hex(T["lotto"]), bold=True)
            a_btn.bind(on_release=lambda x, key=k: self.add(key))
            row.add_widget(self.ips[k]); row.add_widget(a_btn)
            
            c_btn = Button(text="QUANTUM ANALYSE", size_hint_y=None, height=60, background_color=get_color_from_hex(c["c"]), bold=True)
            c_btn.bind(on_release=lambda x, key=k: self.calc(key))
            ctrl.add_widget(row); ctrl.add_widget(c_btn); lay.add_widget(ctrl)

            sc = ScrollView(size_hint_y=1.0)
            self.lbs[k] = Label(text="Bereit.", halign='center', valign='top', markup=True, size_hint_y=None)
            self.lbs[k].bind(texture_size=self.lbs[k].setter('size'))
            sc.add_widget(self.lbs[k]); lay.add_widget(sc); tab.add_widget(lay); self.tp.add_widget(tab)

        self.tp.add_widget(self.custom_tab())
        root.add_widget(self.tp)
        return root

    def custom_tab(self):
        tab = TabbedPanelItem(text="CUSTOM")
        lay = BoxLayout(orientation='vertical', padding=[5, 10, 5, 5], spacing=8)

        self.add_custom_number_row(lay, "Hauptzahlen min", "m_min", 1)
        self.add_custom_number_row(lay, "Hauptzahlen max", "m_max", 50)
        self.add_custom_number_row(lay, "Hauptzahlen Anzahl", "m_count", 5)
        self.add_custom_check_row(lay, "Hauptzahlen mit Wiederholung", "m_repeat", False)
        self.add_custom_number_row(lay, "Zusatzzahlen min", "e_min", 0)
        self.add_custom_number_row(lay, "Zusatzzahlen max", "e_max", 9)
        self.add_custom_number_row(lay, "Zusatzzahlen Anzahl", "e_count", 0)
        self.add_custom_check_row(lay, "Zusatzzahlen mit Wiederholung", "e_repeat", False)

        g_btn = Button(text="INDIVIDUELL GENERIEREN", size_hint_y=None, height=52, background_color=get_color_from_hex(T["acc"]), bold=True)
        g_btn.bind(on_release=lambda x: self.calc_custom())
        lay.add_widget(g_btn)

        sc = ScrollView(size_hint_y=1.0)
        self.custom_lb = Label(text="Beispiel: 1-50 (5 Zahlen), 0-9 (7 Zusatzzahlen), mit/ohne Wiederholung.", halign='left', valign='top', markup=True, size_hint_y=None)
        self.custom_lb.bind(texture_size=self.custom_lb.setter('size'))
        sc.add_widget(self.custom_lb); lay.add_widget(sc)
        tab.add_widget(lay)
        return tab

    def add_custom_number_row(self, parent, text, key, default):
        row = BoxLayout(size_hint_y=None, height=42, spacing=8)
        row.add_widget(Label(text=text, halign='left', valign='middle'))
        ti = TextInput(text=str(default), multiline=False, input_filter='int', size_hint_x=0.35)
        self.custom_inputs[key] = ti
        row.add_widget(ti)
        parent.add_widget(row)

    def add_custom_check_row(self, parent, text, key, default=False):
        row = BoxLayout(size_hint_y=None, height=42, spacing=8)
        row.add_widget(Label(text=text, halign='left', valign='middle'))
        cb = CheckBox(active=default, size_hint=(None, None), size=(40, 40))
        self.custom_inputs[key] = cb
        row.add_widget(cb)
        parent.add_widget(row)

    def load_raw(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f: return json.load(f)
        return {}

    def convert_db(self, raw):
        games = raw.get("games", {k: [] for k in self.cf})
        for gk in games:
            for entry in games[gk]:
                if "main" in entry: entry["m"] = entry.pop("main")
                if "extra" in entry: entry["e"] = entry.pop("extra")
        return games

    def add(self, k):
        t = self.ips[k].text.strip()
        try:
            n = [int(x) for x in re.split(r'[|,\s;]+', t) if x.isdigit()]
            if len(n) >= self.cf[k]["mc"]:
                self.data[k].insert(0, {"m": n[:self.cf[k]["mc"]], "e": n[self.cf[k]["mc"]:]})
                self.save_db(); self.ips[k].text = ""; self.ips[k].focus = False
                self.lbs[k].text = "[color=#10b981]Gespeichert![/color]"
        except: pass

    def save_db(self):
        with open(self.db_path, "w") as f: json.dump({"games": self.data}, f, indent=4)

    def sync(self):
        self.s_btn.text = "..."; threading.Thread(target=self.f_task, daemon=True).start()

    def f_task(self):
        h = {'User-Agent': 'Mozilla/5.0'}
        for k, cfg in self.cf.items():
            try:
                r = requests.get(cfg["u"], headers=h, timeout=10)
                p = r.text.split("Gezogene Reihenfolge")[1][:600] if "Gezogene Reihenfolge" in r.text else r.text
                cl = [int(x) for x in re.findall(r'(\d{1,2})', p)]
                if len(cl) >= cfg["mc"]:
                    m, e = cl[:cfg["mc"]], cl[cfg["mc"]:cfg["mc"]+cfg["ec"]]
                    if not any(x.get("m") == m for x in self.data[k]): self.data[k].insert(0, {"m": m, "e": e})
            except: continue
        self.done()

    @mainthread
    def done(self): self.save_db(); self.s_btn.text = "SYNC"

    def calc(self, k): threading.Thread(target=self.logic, args=(k,), daemon=True).start()

    def calc_custom(self): threading.Thread(target=self.custom_logic, daemon=True).start()

    def logic(self, k):
        cfg = self.cf[k]; hist = self.data.get(k, [])
        if not hist: self.upd(k, "Keine Daten."); return
        mc, mm, ec, em = cfg["mc"], cfg["mm"], cfg["ec"], cfg["em"]
        
        mat = np.ones((mc, mm + 1))
        peaks = []
        for p in range(mc):
            pd = [x["m"][p] for x in hist if "m" in x and len(x["m"]) > p]
            if pd:
                c = np.bincount(pd, minlength=mm+1)
                mat[p] = 1.0 / (c + 0.7)
            if k != "GS": mat[p, 0] = 0
            peaks.append(int(np.argmax(mat[p])))

        e_peaks = []
        if ec > 0:
            emat = np.ones((ec, em + 1))
            for p in range(ec):
                ed = [x["e"][p] for x in hist if isinstance(x.get("e"), (list, tuple)) and len(x["e"]) > p]
                if ed:
                    c = np.bincount(ed, minlength=em+1)
                    emat[p] = 1.0 / (c + 0.7)
                emat[p, 0] = 0
                e_peaks.append(int(np.argmax(emat[p])))

        res = f"--- [b]{cfg['n']}[/b] ---\n"
        res += f"HOT: [b][color={cfg['c']}]{' '.join(f'{x:02d}' for x in peaks)}[/color][/b]\n"
        if e_peaks:
            res += f"EURO: [b][color={cfg['c']}]{' '.join(f'{x:02d}' for x in e_peaks)}[/color][/b]\n"
        self.upd(k, res)

    def custom_logic(self):
        try:
            m_min = int(self.custom_inputs["m_min"].text)
            m_max = int(self.custom_inputs["m_max"].text)
            m_count = int(self.custom_inputs["m_count"].text)
            m_repeat = self.custom_inputs["m_repeat"].active
            e_min = int(self.custom_inputs["e_min"].text)
            e_max = int(self.custom_inputs["e_max"].text)
            e_count = int(self.custom_inputs["e_count"].text)
            e_repeat = self.custom_inputs["e_repeat"].active
        except (ValueError, KeyError, AttributeError):
            self.upd_custom("[color=#f43f5e]Bitte gültige Zahlen eingeben.[/color]")
            return

        try:
            main_nums = self.pick_numbers(m_min, m_max, m_count, m_repeat)
            extra_nums = self.pick_numbers(e_min, e_max, e_count, e_repeat) if e_count > 0 else []
            res = "--- [b]Individuelle Auswahl[/b] ---\n"
            res += f"MAIN ({m_min}-{m_max}, n={m_count}, Wiederholung={'Ja' if m_repeat else 'Nein'}): "
            res += f"[b][color={T['ej']}]{self.format_nums(main_nums, m_max)}[/color][/b]\n"
            if e_count > 0:
                res += f"EXTRA ({e_min}-{e_max}, n={e_count}, Wiederholung={'Ja' if e_repeat else 'Nein'}): "
                res += f"[b][color={T['lotto']}]{self.format_nums(extra_nums, e_max)}[/color][/b]\n"
            self.upd_custom(res)
        except ValueError as ex:
            self.upd_custom(f"[color=#f43f5e]{str(ex)}[/color]")

    def pick_numbers(self, vmin, vmax, count, repeat):
        if count < 0: raise ValueError("Anzahl darf nicht negativ sein.")
        if count == 0: return []
        if vmin > vmax: raise ValueError("Min darf nicht größer als Max sein.")
        span = vmax - vmin + 1
        if not repeat and count > span:
            raise ValueError("Ohne Wiederholung dürfen nicht mehr Zahlen als Bereichsgröße gewählt werden.")
        rng = np.random.default_rng()
        if repeat:
            return [int(x) for x in rng.integers(vmin, vmax + 1, size=count).tolist()]
        return [int(x) for x in rng.choice(np.arange(vmin, vmax + 1), size=count, replace=False).tolist()]

    def format_nums(self, nums, vmax):
        width = max(1, len(str(max(nums))) if nums else len(str(max(vmax, 0))))
        return " ".join(f"{x:0{width}d}" for x in nums)

    @mainthread
    def upd(self, k, t): self.lbs[k].text = t

    @mainthread
    def upd_custom(self, t): self.custom_lb.text = t

if __name__ == "__main__":
    VortexUltraApp().run()
