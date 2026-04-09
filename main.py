import os, json, re, threading, requests, shutil
import numpy as np
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock, mainthread
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

T = {"bg": "#020617", "ej": "#22d3ee", "lotto": "#10b981", "gs": "#fbbf24", "acc": "#f43f5e", "white": "#ffffff"}

class VortexUltraApp(App):
    def build(self):
        Window.softinput_mode = 'pan'
        Window.clearcolor = get_color_from_hex(T["bg"])
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

        root.add_widget(self.tp)
        return root

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

        res = f"--- [b]{cfg['n']}[/b] ---\n"
        res += f"HOT: [b][color={cfg['c']}]{' '.join(f'{x:02d}' for x in peaks)}[/color][/b]\n"
        self.upd(k, res)

    @mainthread
    def upd(self, k, t): self.lbs[k].text = t

if __name__ == "__main__":
    VortexUltraApp().run()
