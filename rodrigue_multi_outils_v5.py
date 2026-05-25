#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════
  RODRIGUE – Multi-Outils Pro v5.0
  Application Ultra-Complète · 48 Fonctionnalités
  Design Épuré · Sidebar Navigation · Thème Sobre
═══════════════════════════════════════════════════════════════════
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import math
import requests
import os
import struct
import socket
import json
import random
import string
import hashlib
import base64
import platform
import time
from datetime import datetime, timedelta
from fractions import Fraction
import threading
import webbrowser
import uuid as uuid_mod
import re
from collections import Counter

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════
#   PALETTE DE COULEURS & CONFIGURATION
# ═══════════════════════════════════════════════════════════════
COULEURS = {
    "bg":            "#111118",
    "sidebar":       "#161620",
    "sidebar_hover": "#1e1e2c",
    "surface":       "#191924",
    "card":          "#21212e",
    "card_border":   "#2c2c3a",
    "accent":        "#6b6bff",
    "accent_light":  "#8a8aff",
    "accent_dim":    "#5050cc",
    "text":          "#e4e4ee",
    "subtext":       "#7e7e98",
    "input_bg":      "#1c1c2a",
    "btn":           "#2a2a3c",
    "result_fg":     "#90ddb0",
}

SIDEBAR_TOOLS = [
    ("calc",       "🧮", "Calculatrice"),
    ("sci",        "🔬", "Scientifique"),
    ("storage",    "💾", "Stockage"),
    ("units",      "📏", "Unités"),
    ("currency",   "💱", "Devises"),
    ("geometry",   "📐", "Géométrie"),
    ("stats",      "📊", "Statistiques"),
    ("security",   "🔐", "Sécurité"),
    ("dates",      "📅", "Dates"),
    ("timer",      "⏱️", "Minuteur"),
    ("network",    "🌐", "Réseau"),
    ("text",       "📝", "Texte"),
    ("colors",     "🎨", "Couleurs"),
    ("bases",      "🔢", "Bases"),
    ("percent",    "📊", "Pourcentages"),
    ("health",     "🏥", "IMC Santé"),
    ("loan",       "💰", "Emprunt"),
    ("roman",      "Ⅶ", "Romains"),
    ("random",     "🧬", "Aléatoire"),
    ("cipher",     "🤫", "Chiffrement"),
    ("electric",   "⚡", "Électricité"),
    ("tip",        "🧮", "Pourboire"),
    ("equations",  "📐", "Équations"),
    ("weather",    "🌡️", "Météo"),
    ("wordcount",  "🔤", "Compteur"),
    ("physics",    "ℏ",  "Physique"),
    ("bitwise",    "🔓", "Bitwise"),
    ("triangle",   "📐", "Triangle"),
    ("roi",        "📈", "Rentabilité"),
    ("timestamp",  "⏰", "Timestamp"),
    ("weighted",   "⚖️", "Moy. Pondérée"),
    ("charfreq",   "🔣", "Fréquence"),
    ("discount",   "🏷️", "Remise"),
    ("slope",      "📈", "Pente"),
    ("bizdays",    "🗓️", "Jours Ouvr."),
    ("bintext",    "💾", "Binaire←→Txt"),
    ("speed",      "🏎️", "Vitesse"),
    ("fuel",       "⛽", "Carburant"),
    # ── V5.0 : 10 nouveaux outils ──
    ("json",       "📋", "JSON"),
    ("regex",      "🔍", "Regex"),
    ("nbletters",  "🔤", "Nb→Lettres"),
    ("age",        "🎂", "Âge"),
    ("compound",   "📈", "Int. Composés"),
    ("morse",      "📡", "Code Morse"),
    ("gcdlcm",     "🔗", "PGCD/PPCM"),
    ("uuidgen",    "🆔", "UUID"),
    ("hourcalc",   "⏰", "Calcul Heures"),
    ("gps",        "📍", "GPS DMS/Déc"),
]


# ═══════════════════════════════════════════════════════════════
#   CALCULATRICE SCIENTIFIQUE (Moteur)
# ═══════════════════════════════════════════════════════════════
class ScientificCalculator:
    CONSTANTS = {"π": math.pi, "e": math.e, "φ": (1+math.sqrt(5))/2}

    def __init__(self):
        self.history = []
        self.memory = 0.0
        self.angle_mode = "deg"

    def set_angle_mode(self, mode):
        self.angle_mode = mode

    def _to_rad(self, x):
        return math.radians(x) if self.angle_mode == "deg" else x

    def _from_rad(self, x):
        return math.degrees(x) if self.angle_mode == "deg" else x

    def evaluate(self, expr: str):
        try:
            expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-").replace("^", "**")
            safe = {
                "sin": lambda x: math.sin(self._to_rad(x)),
                "cos": lambda x: math.cos(self._to_rad(x)),
                "tan": lambda x: math.tan(self._to_rad(x)),
                "asin": lambda x: self._from_rad(math.asin(x)),
                "acos": lambda x: self._from_rad(math.acos(x)),
                "atan": lambda x: self._from_rad(math.atan(x)),
                "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
                "log": math.log10, "ln": math.log, "log2": math.log2,
                "sqrt": math.sqrt, "abs": abs,
                "floor": math.floor, "ceil": math.ceil, "round": round,
                "exp": math.exp, "factorial": math.factorial,
                "gcd": math.gcd, "lcm": lambda a, b: abs(a*b)//math.gcd(a,b),
                "mod": lambda a, b: a % b, "pow": pow,
                "pi": math.pi, "e": math.e, "phi": (1+math.sqrt(5))/2,
            }
            result = eval(expr, {"__builtins__": {}}, safe)
            if isinstance(result, float):
                if abs(result) < 1e-10: result = 0
                elif abs(result) >= 1e10 or (abs(result) < 1e-4 and result != 0):
                    result = f"{result:.6e}"
                else:
                    result = round(result, 10)
                    if result == int(result): result = int(result)
            return result, None
        except ZeroDivisionError: return None, "Division par zéro"
        except ValueError as e: return None, f"Erreur de valeur: {e}"
        except SyntaxError: return None, "Expression invalide"
        except Exception as e: return None, f"Erreur: {e}"


# ═══════════════════════════════════════════════════════════════
#   GÉNÉRATEUR DE MOTS DE PASSE
# ═══════════════════════════════════════════════════════════════
class PasswordGenerator:
    @staticmethod
    def generate(length=16, upper=True, lower=True, digits=True, special=True, exclude_similar=False):
        chars = ""
        if lower: chars += "abcdefghjkmnpqrstuvwxyz" if exclude_similar else "abcdefghijklmnopqrstuvwxyz"
        if upper: chars += "ABCDEFGHJKMNPQRSTUVWXYZ" if exclude_similar else "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if digits: chars += "23456789" if exclude_similar else "0123456789"
        if special: chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not chars: return None
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def check_strength(password):
        score, feedback = 0, []
        if len(password) >= 8: score += 1
        else: feedback.append("Au moins 8 caractères")
        if len(password) >= 12: score += 1
        if len(password) >= 16: score += 1
        if any(c.islower() for c in password): score += 1
        else: feedback.append("Ajoutez des minuscules")
        if any(c.isupper() for c in password): score += 1
        else: feedback.append("Ajoutez des majuscules")
        if any(c.isdigit() for c in password): score += 1
        else: feedback.append("Ajoutez des chiffres")
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 1
        else: feedback.append("Ajoutez des spéciaux")
        levels = ["Très faible","Faible","Moyen","Fort","Très fort","Excellent"]
        return score, levels[min(score, len(levels)-1)], feedback


# ═══════════════════════════════════════════════════════════════
#   CONVERTISSEUR D'UNITÉS
# ═══════════════════════════════════════════════════════════════
class UnitConverter:
    UNITS = {
        "Longueur":    {"mm":0.001,"cm":0.01,"m":1,"km":1000,"in":0.0254,"ft":0.3048,"yd":0.9144,"mi":1609.344,"nmi":1852},
        "Masse":       {"mg":0.001,"g":1,"kg":1000,"t":1e6,"oz":28.3495,"lb":453.592,"ct":0.2},
        "Température": {"°C":"celsius","°F":"fahrenheit","K":"kelvin"},
        "Volume":      {"mL":0.001,"L":1,"m³":1000,"gal US":3.78541,"gal UK":4.54609,"fl oz":0.0295735},
        "Aire":        {"mm²":1e-6,"cm²":1e-4,"m²":1,"km²":1e6,"ha":1e4,"ac":4046.86,"ft²":0.092903,"in²":6.4516e-4},
        "Vitesse":     {"m/s":1,"km/h":0.277778,"mph":0.44704,"kn":0.514444,"c":299792458},
        "Temps":       {"ms":1e-3,"s":1,"min":60,"h":3600,"j":86400,"sem":604800},
        "Données":     {"bit":1/8,"B":1,"KB":1024,"MB":1024**2,"GB":1024**3,"TB":1024**4,"PB":1024**5},
        "Pression":    {"Pa":1,"hPa":100,"kPa":1000,"bar":1e5,"psi":6894.76,"atm":101325},
        "Énergie":     {"J":1,"kJ":1000,"cal":4.184,"kcal":4184,"Wh":3600,"kWh":3.6e6,"BTU":1055.06},
    }
    @staticmethod
    def convert(value, from_u, to_u, cat):
        if cat not in UnitConverter.UNITS: return None, "Catégorie inconnue"
        u = UnitConverter.UNITS[cat]
        if from_u not in u or to_u not in u: return None, "Unité inconnue"
        if cat == "Température": return UnitConverter._convert_temp(value, from_u, to_u)
        return value * u[from_u] / u[to_u], None
    @staticmethod
    def _convert_temp(v, f, t):
        c = v if f=="°C" else (v-32)*5/9 if f=="°F" else v-273.15
        if t=="°C": return c, None
        if t=="°F": return c*9/5+32, None
        return c+273.15, None


# ═══════════════════════════════════════════════════════════════
#   APPLICATION PRINCIPALE
# ═══════════════════════════════════════════════════════════════
class MultiOutilsPro:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("⚡ Rodrigue – Multi-Outils Pro v5.0")
        self.root.configure(bg=COULEURS["bg"])
        self.root.geometry("1100x750")
        self.root.minsize(850, 600)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x, y = (sw-1100)//2, (sh-750)//2
        self.root.geometry(f"1100x750+{x}+{y}")

        self.calc_engine = ScientificCalculator()
        self.taux = {"USD":600.0,"EUR":655.95,"GBP":850.0,"CAD":440.0,"XOF":1.0}
        self.history_file = "historique_rodrigue_v5.txt"
        self.timer_running = False
        self.stopwatch_running = False
        self.sidebar_wide = True
        self.current_tool = "calc"
        self._scroll_canvas = None

        self._build_ui()
        self._load_rates()
        self._update_clock()
        self._open_tool("calc")

    # ─────────── BUILD UI ───────────
    def _build_ui(self):
        # Status bar (bottom)
        self.status_bar = tk.Frame(self.root, bg=COULEURS["card_border"], height=26)
        self.status_bar.pack(side="bottom", fill="x")
        self.status_bar.pack_propagate(False)
        self.status_left = tk.Label(self.status_bar, text="", bg=COULEURS["card_border"],
                                    fg=COULEURS["subtext"], font=("Segoe UI", 9))
        self.status_left.pack(side="left", padx=10)
        self.status_right = tk.Label(self.status_bar, text="", bg=COULEURS["card_border"],
                                     fg=COULEURS["subtext"], font=("Segoe UI", 9))
        self.status_right.pack(side="right", padx=10)

        # Main container
        self.main_frame = tk.Frame(self.root, bg=COULEURS["bg"])
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(self.main_frame, bg=COULEURS["sidebar"], width=195)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Sidebar title
        tk.Label(self.sidebar, text="⚡ Rodrigue", font=("Segoe UI", 13, "bold"),
                 bg=COULEURS["accent"], fg="white", anchor="w", padx=12, pady=8
                 ).pack(fill="x", pady=(0, 2))
        tk.Label(self.sidebar, text="Multi-Outils Pro v5.0", font=("Segoe UI", 8),
                 bg=COULEURS["sidebar"], fg=COULEURS["subtext"], anchor="w", padx=12
                 ).pack(fill="x", pady=(0, 6))

        sep = tk.Frame(self.sidebar, bg=COULEURS["card_border"], height=1)
        sep.pack(fill="x", padx=8, pady=4)

        # Scrollable sidebar buttons
        self._scroll_canvas = tk.Canvas(self.sidebar, bg=COULEURS["sidebar"],
                                        highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(self.sidebar, orient="vertical", command=self._scroll_canvas.yview,
                                 bg=COULEURS["sidebar"], troughcolor=COULEURS["sidebar"],
                                 activebackground=COULEURS["accent"])
        self.sidebar_inner = tk.Frame(self._scroll_canvas, bg=COULEURS["sidebar"])

        self.sidebar_inner.bind("<Configure>",
            lambda e: self._scroll_canvas.configure(scrollregion=self._scroll_canvas.bbox("all")))
        self._scroll_canvas.create_window((0, 0), window=self.sidebar_inner, anchor="nw")
        self._scroll_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self._scroll_canvas.pack(side="left", fill="both", expand=True)

        # Bind mouse wheel on canvas
        self._scroll_canvas.bind("<Enter>", self._bind_scroll)
        self._scroll_canvas.bind("<Leave>", self._unbind_scroll)

        self.sidebar_buttons = {}
        self.sidebar_labels = {}
        for tid, icon, label in SIDEBAR_TOOLS:
            btn = tk.Frame(self.sidebar_inner, bg=COULEURS["sidebar"], cursor="hand2", padx=4, pady=2)
            btn.pack(fill="x", pady=1, padx=4)
            lbl = tk.Label(btn, text=f" {icon}  {label}", font=("Segoe UI", 9),
                           bg=COULEURS["sidebar"], fg=COULEURS["subtext"], anchor="w", padx=6, pady=4)
            lbl.pack(fill="x")
            self.sidebar_buttons[tid] = btn
            self.sidebar_labels[tid] = lbl
            btn.bind("<Enter>", lambda e, b=btn, l=lbl: (
                l.config(bg=COULEURS["sidebar_hover"]),
                b.config(bg=COULEURS["sidebar_hover"])))
            btn.bind("<Leave>", lambda e, b=btn, l=lbl, t=tid: self._sidebar_leave(b, l, t))
            for w in (btn, lbl):
                w.bind("<Button-1>", lambda e, t=tid: self._open_tool(t))

        # Content area
        self.content = tk.Frame(self.main_frame, bg=COULEURS["surface"])
        self.content.pack(side="left", fill="both", expand=True)

        # Menu bar
        self._build_menu()

        # Resize
        self.root.bind("<Configure>", self._on_resize)

    # ─────────── MENU BAR ───────────
    def _build_menu(self):
        mb = tk.Menu(self.root, bg=COULEURS["card"], fg=COULEURS["text"],
                     activebackground=COULEURS["accent"], activeforeground="white",
                     font=("Segoe UI", 10), relief="flat", tearoff=0)

        # ── Fichier ──
        m_file = tk.Menu(mb, tearoff=0, bg=COULEURS["card"], fg=COULEURS["text"],
                         activebackground=COULEURS["accent"], activeforeground="white",
                         font=("Segoe UI", 10))
        m_file.add_command(label="📋 Historique", command=self._menu_history)
        m_file.add_command(label="🗑  Vider l'historique", command=self._menu_clear_history)
        m_file.add_command(label="💾 Exporter l'historique", command=self._menu_export_history)
        m_file.add_separator()
        m_file.add_command(label="🚪 Quitter", command=self.root.quit)
        mb.add_cascade(label="  Fichier  ", menu=m_file)

        # ── Outils ──
        m_tools = tk.Menu(mb, tearoff=0, bg=COULEURS["card"], fg=COULEURS["text"],
                          activebackground=COULEURS["accent"], activeforeground="white",
                          font=("Segoe UI", 10))
        m_tools.add_command(label="🔄 Actualiser taux de change", command=self._menu_refresh_rates)
        m_tools.add_command(label="📡 Mon IP publique", command=self._menu_public_ip)
        m_tools.add_separator()
        m_tools.add_command(label="💻 Infos système", command=self._menu_sysinfo)
        mb.add_cascade(label="  Outils  ", menu=m_tools)

        # ── Navigation rapide ──
        m_nav = tk.Menu(mb, tearoff=0, bg=COULEURS["card"], fg=COULEURS["text"],
                        activebackground=COULEURS["accent"], activeforeground="white",
                        font=("Segoe UI", 10))
        for tid, icon, label in SIDEBAR_TOOLS:
            m_nav.add_command(label=f"{icon}  {label}",
                              command=lambda t=tid: self._open_tool(t))
        mb.add_cascade(label="  Navigation  ", menu=m_nav)

        # ── Aide ──
        m_help = tk.Menu(mb, tearoff=0, bg=COULEURS["card"], fg=COULEURS["text"],
                         activebackground=COULEURS["accent"], activeforeground="white",
                         font=("Segoe UI", 10))
        m_help.add_command(label="ℹ️  À propos", command=self._menu_about)
        m_help.add_command(label="⌨️  Raccourcis clavier", command=self._menu_shortcuts)
        m_help.add_separator()
        m_help.add_command(label="📖  Liste des 48 outils", command=self._menu_tools_list)
        mb.add_cascade(label="  Aide  ", menu=m_help)

        self.root.config(menu=mb)

    # ── Menu Actions ──
    def _menu_history(self):
        if not os.path.exists(self.history_file):
            messagebox.showinfo("Historique", "L'historique est vide.")
            return
        win = tk.Toplevel(self.root)
        win.title("📋 Historique")
        win.geometry(f"700x500")
        win.configure(bg=COULEURS["bg"])
        win.transient(self.root)
        # Header
        tk.Label(win, text="📋 Historique des calculs", font=("Segoe UI", 13, "bold"),
                 bg=COULEURS["accent"], fg="white", padx=12, pady=8).pack(fill="x")
        st = scrolledtext.ScrolledText(win, font=("Consolas", 10),
                                       bg=COULEURS["card"], fg=COULEURS["text"],
                                       relief="flat", insertbackground=COULEURS["accent"],
                                       selectbackground=COULEURS["accent_dim"])
        st.pack(fill="both", expand=True, padx=10, pady=10)
        with open(self.history_file, encoding="utf-8") as f:
            st.insert("end", f.read())
        st.config(state="disabled")
        tk.Button(win, text="Fermer", command=win.destroy, font=("Segoe UI", 10, "bold"),
                  fg="white", bg=COULEURS["accent"], relief="flat", padx=20, pady=6,
                  cursor="hand2").pack(pady=(0, 10))

    def _menu_clear_history(self):
        if os.path.exists(self.history_file):
            if messagebox.askyesno("Confirmation", "Supprimer tout l'historique ?"):
                os.remove(self.history_file)
                messagebox.showinfo("Succès", "Historique vidé.")
        else:
            messagebox.showinfo("Info", "L'historique est déjà vide.")

    def _menu_export_history(self):
        if not os.path.exists(self.history_file):
            messagebox.showwarning("Attention", "Aucun historique à exporter.")
            return
        fp = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Texte", "*.txt"), ("Tous", "*.*")],
            initialfile=f"historique_{datetime.now().strftime('%Y%m%d')}.txt")
        if fp:
            import shutil
            shutil.copy(self.history_file, fp)
            messagebox.showinfo("Succès", f"Exporté vers :\n{fp}")

    def _menu_refresh_rates(self):
        self._load_rates()
        src = "live" if self.taux.get("_live") else "hors-ligne"
        messagebox.showinfo("Taux de change", f"Taux actualisés ({src}).")
        if self.current_tool == "currency":
            self._open_tool("currency")

    def _menu_public_ip(self):
        try:
            r = requests.get("https://api.ipify.org?format=json", timeout=5)
            ip = r.json()["ip"]
            messagebox.showinfo("IP Publique", f"🌐 Votre IP publique :\n\n  {ip}")
        except:
            messagebox.showerror("Erreur", "Impossible de récupérer l'IP.")

    def _menu_sysinfo(self):
        info = [
            f"💻 Système : {platform.system()} {platform.release()}",
            f"🖥️ Machine : {platform.machine()}",
            f"🖥️ Processeur : {platform.processor()}",
            f"🐍 Python : {platform.python_version()}",
            f"👤 Utilisateur : {platform.node()}",
        ]
        if PSUTIL_AVAILABLE:
            try:
                cpu_freq = psutil.cpu_freq()
                info.extend([
                    f"💾 CPU : {psutil.cpu_count(logical=False)} cœurs physiques, {psutil.cpu_count()} logiques",
                    f"📊 Fréquence CPU : {cpu_freq.current:.0f} MHz" if cpu_freq else "",
                    f"📊 RAM : {psutil.virtual_memory().total / (1024**3):.1f} GB total, {psutil.virtual_memory().available / (1024**3):.1f} GB disponible",
                    f"💿 Disque : {psutil.disk_usage('/').total / (1024**3):.1f} GB total, {psutil.disk_usage('/').free / (1024**3):.1f} GB libre",
                ])
            except:
                info.append("📊 Infos détaillées non disponibles")
        else:
            info.append("💡 Installez 'psutil' pour plus d'infos : pip install psutil")
        messagebox.showinfo("Infos Système", "\n".join(info))

    def _menu_about(self):
        win = tk.Toplevel(self.root)
        win.title("À propos")
        win.geometry("480x520")
        win.configure(bg=COULEURS["bg"])
        win.resizable(False, False)
        win.transient(self.root)
        # Header
        tk.Label(win, text="", bg=COULEURS["accent"], height=1).pack(fill="x")
        tk.Label(win, text="⚡ Rodrigue – Multi-Outils Pro",
                 font=("Segoe UI", 16, "bold"), bg=COULEURS["bg"], fg=COULEURS["accent_light"]
                 ).pack(pady=(20, 2))
        tk.Label(win, text="Version 5.0 — Édition Épurée",
                 font=("Segoe UI", 10), bg=COULEURS["bg"], fg=COULEURS["subtext"]
                 ).pack(pady=(0, 12))
        # Features list in a card
        card = tk.Frame(win, bg=COULEURS["card"], highlightbackground=COULEURS["card_border"],
                        highlightthickness=1, padx=16, pady=12)
        card.pack(fill="both", expand=True, padx=24, pady=(0, 12))
        features = (
            "🧮 Calculatrice Standard & Scientifique\n"
            "💾 Convertisseur Stockage\n"
            "📏 Convertisseur d'Unités (10 catégories)\n"
            "💱 Convertisseur de Devises (live API)\n"
            "📐 Calculateur Géométrique (9 figures)\n"
            "📊 Statistiques & Probabilités\n"
            "🔐 Mots de passe & Hash (MD5/SHA)\n"
            "📅 Calculateur de Dates\n"
            "⏱️ Chronomètre & Minuteur\n"
            "🌐 Outils Réseau (CIDR/DNS/IP)\n"
            "📝 Outils Texte & Encodage\n"
            "🎨 Convertisseur Couleurs (HEX/RGB/HSL)\n"
            "🔢 Convertisseur de Bases\n"
            "📊 Calculatrice de Pourcentages\n"
            "🏥 IMC & Métabolisme de Base\n"
            "💰 Calculatrice d'Emprunt\n"
            "Ⅶ Nombres Romains\n"
            "🧬 Générateur Aléatoire (dés, loto)\n"
            "🤫 Chiffrement César & ROT13\n"
            "⚡ Loi d'Ohm & Puissance\n"
            "🧮 Calculatrice de Pourboire\n"
            "📐 Solveur d'Équations\n"
            "🌡️ Wind Chill & Heat Index\n"
            "🔤 Compteur de Mots Avancé\n"
            "ℏ Constantes Physiques"
        )
        tk.Label(card, text=features, font=("Segoe UI", 9), bg=COULEURS["card"],
                 fg=COULEURS["text"], justify="left").pack(anchor="w")
        tk.Button(win, text="Fermer", command=win.destroy, font=("Segoe UI", 10, "bold"),
                  fg="white", bg=COULEURS["accent"], relief="flat", padx=20, pady=6,
                  cursor="hand2").pack(pady=(0, 16))

    def _menu_shortcuts(self):
        shortcuts = (
            "⌨️  Raccourcis clavier\n\n"
            "Calculatrice :\n"
            "  • Entrée  =  Calculer\n"
            "  • Échap   =  Effacer (dans certains champs)\n\n"
            "Navigation :\n"
            "  • Tab / Shift+Tab  =  Parcourir les champs\n"
            "  • Ctrl+C / Ctrl+V  =  Copier / Coller\n"
            "  • Alt + lettres     =  Menus (Fichier, Outils, Aide)\n\n"
            "Général :\n"
            "  • Molette  =  Scroller sidebar & contenu\n"
            "  • Redimensionner  =  Sidebar s'adapte automatiquement"
        )
        messagebox.showinfo("Raccourcis clavier", shortcuts)

    def _menu_tools_list(self):
        win = tk.Toplevel(self.root)
        win.title("📖 Liste des 48 outils")
        win.geometry("500x620")
        win.configure(bg=COULEURS["bg"])
        win.resizable(False, False)
        win.transient(self.root)
        tk.Label(win, text="📖 48 Outils Disponibles",
                 font=("Segoe UI", 14, "bold"), bg=COULEURS["accent"], fg="white",
                 padx=12, pady=8).pack(fill="x")
        # Card with list
        card = tk.Frame(win, bg=COULEURS["card"], highlightbackground=COULEURS["card_border"],
                        highlightthickness=1, padx=16, pady=12)
        card.pack(fill="both", expand=True, padx=16, pady=12)
        canvas = tk.Canvas(card, bg=COULEURS["card"], highlightthickness=0, bd=0)
        vsb = tk.Scrollbar(card, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=COULEURS["card"])
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        descriptions = [
            ("🧮", "Calculatrice Standard", "Opérations basiques, mémoire (MC/MR/M+/M-/MS), mode DEG/RAD"),
            ("🔬", "Calculatrice Scientifique", "sin/cos/tan, log/ln, factoriel, constantes (π, e, φ)"),
            ("💾", "Convertisseur Stockage", "bits, B, KB, MB, GB, TB, PB"),
            ("📏", "Convertisseur d'Unités", "10 catégories : longueur, masse, température, vitesse..."),
            ("💱", "Convertisseur Devises", "EUR, USD, GBP, CAD, XOF — taux en temps réel via API"),
            ("📐", "Calculateur Géométrique", "Cercle, Rectangle, Triangle, Sphère, Cylindre, Cône, Cube..."),
            ("📊", "Statistiques & Probabilités", "Moyenne, médiane, variance, écart-type, C(n,k), P(n,k)"),
            ("🔐", "Sécurité", "Générateur de mots de passe + Hash MD5/SHA1/SHA256/SHA512"),
            ("📅", "Calculateur de Dates", "Différence entre dates, ajouter/retirer des jours"),
            ("⏱️", "Minuteur & Chronomètre", "Chronomètre ms, compte à rebours configurable"),
            ("🌐", "Outils Réseau", "CIDR, DNS, IP publique, convertisseur IP"),
            ("📝", "Outils Texte", "Analyse, minuscule/majuscule, Base64, URL encoding"),
            ("🎨", "Convertisseur Couleurs", "HEX ↔ RGB ↔ HSL, preview canvas, complémentaire"),
            ("🔢", "Convertisseur Bases", "Binaire, Octal, Décimal, Hexadécimal + ASCII"),
            ("📊", "Pourcentages", "% d'un nombre, augmentation, réduction, valeur initiale"),
            ("🏥", "IMC & Santé", "IMC, poids idéal, métabolisme de base (BMR)"),
            ("💰", "Calculatrice d'Emprunt", "Mensualité, intérêts totaux, coût de l'emprunt"),
            ("Ⅶ", "Nombres Romains", "Conversion Arabe ↔ Romain (1-3999)"),
            ("🧬", "Générateur Aléatoire", "Nombre aléatoire, dés, pile/face, loto 6/49"),
            ("🤫", "Chiffrement César/ROT13", "Chiffrer/déchiffrer avec décalage personnalisé"),
            ("⚡", "Loi d'Ohm", "Calcul automatique : V=RI, P=VI (2 valeurs → 2 résultats)"),
            ("🧮", "Calculatrice Pourboire", "Note + % + partage par personne"),
            ("📐", "Solveur d'Équations", "2nd degré (discriminant, racines) + 1er degré"),
            ("🌡️", "Indice Météo", "Wind Chill + Heat Index avec niveaux d'alerte"),
            ("🔤", "Compteur Avancé", "Mots, temps lecture/élocution, Flesch score"),
            ("ℏ", "Constantes Physiques", "15 constantes fondamentales + convertisseur eV→J"),
        ]
        for icon, name, desc in descriptions:
            row = tk.Frame(inner, bg=COULEURS["card"], cursor="hand2")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{icon}  {name}", font=("Segoe UI", 10, "bold"),
                     bg=COULEURS["card"], fg=COULEURS["accent_light"], anchor="w"
                     ).pack(anchor="w")
            tk.Label(row, text=f"    {desc}", font=("Segoe UI", 8),
                     bg=COULEURS["card"], fg=COULEURS["subtext"], anchor="w"
                     ).pack(anchor="w", pady=(0, 4))

        tk.Button(win, text="Fermer", command=win.destroy, font=("Segoe UI", 10, "bold"),
                  fg="white", bg=COULEURS["accent"], relief="flat", padx=20, pady=6,
                  cursor="hand2").pack(pady=(0, 12))

    def _bind_scroll(self, event):
        self._scroll_canvas.bind_all("<MouseWheel>",
            lambda e: self._scroll_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self._scroll_canvas.bind_all("<Button-4>",
            lambda e: self._scroll_canvas.yview_scroll(-1, "units"))
        self._scroll_canvas.bind_all("<Button-5>",
            lambda e: self._scroll_canvas.yview_scroll(1, "units"))

    def _unbind_scroll(self, event):
        self._scroll_canvas.unbind_all("<MouseWheel>")
        self._scroll_canvas.unbind_all("<Button-4>")
        self._scroll_canvas.unbind_all("<Button-5>")

    def _sidebar_leave(self, btn, lbl, tid):
        bg = COULEURS["accent_dim"] if tid == self.current_tool else COULEURS["sidebar"]
        lbl.config(bg=bg); btn.config(bg=bg)

    def _highlight_sidebar(self, tid):
        for t, btn in self.sidebar_buttons.items():
            l = self.sidebar_labels[t]
            if t == tid:
                btn.config(bg=COULEURS["accent_dim"])
                l.config(bg=COULEURS["accent_dim"], fg="white")
            else:
                btn.config(bg=COULEURS["sidebar"])
                l.config(bg=COULEURS["sidebar"], fg=COULEURS["subtext"])
        self.current_tool = tid
        name = dict((t[0], t[2]) for t in SIDEBAR_TOOLS).get(tid, "")
        self.status_left.config(text=f"  {name}  |  48 outils disponibles")

    def _open_tool(self, tid):
        self._highlight_sidebar(tid)
        for w in self.content.winfo_children():
            w.destroy()
        builder = getattr(self, f"_build_{tid}", None)
        if builder:
            # Scrollable content
            canvas = tk.Canvas(self.content, bg=COULEURS["surface"], highlightthickness=0, bd=0)
            vsb = tk.Scrollbar(self.content, orient="vertical", command=canvas.yview,
                               bg=COULEURS["surface"], troughcolor=COULEURS["surface"])
            frame = tk.Frame(canvas, bg=COULEURS["surface"])
            frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=frame, anchor="nw")
            canvas.configure(yscrollcommand=vsb.set)
            vsb.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>",
                lambda ev: canvas.yview_scroll(int(-1*(ev.delta/120)), "units")))
            canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
            # Make frame fill canvas width
            canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas.find_all()[0], width=e.width))
            builder(frame)

    def _on_resize(self, event):
        if event.widget is not self.root: return
        w = event.width
        new_wide = w >= 750
        if new_wide != self.sidebar_wide:
            self.sidebar_wide = new_wide
            target = 195 if new_wide else 55
            self.sidebar.config(width=target)
            for tid, lbl in self.sidebar_labels.items():
                icon = dict((t[0], t[1]) for t in SIDEBAR_TOOLS)[tid]
                name = dict((t[0], t[2]) for t in SIDEBAR_TOOLS)[tid]
                lbl.config(text=f" {icon}  {name}" if new_wide else f" {icon} ")

    def _update_clock(self):
        self.status_right.config(text=f"  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  ")
        self.root.after(1000, self._update_clock)

    def _on_close(self):
        self.timer_running = False
        self.stopwatch_running = False
        self.root.destroy()

    # ─────────── LOAD RATES ───────────
    def _load_rates(self):
        try:
            r = requests.get("https://open.er-api.com/v6/latest/EUR", timeout=5)
            data = r.json()
            if data.get("result") == "success":
                rates = data["rates"]
                bx = rates.get("XOF", 655.95)
                self.taux["EUR"] = bx
                self.taux["USD"] = bx / rates.get("USD", 1.09)
                self.taux["GBP"] = bx / rates.get("GBP", 0.86)
                self.taux["CAD"] = bx / rates.get("CAD", 1.47)
                self.taux["_live"] = True
        except: self.taux["_live"] = False

    # ═══════════════════════════════════════════════════════════
    #   HELPERS COMMUNS
    # ═══════════════════════════════════════════════════════════
    def _title(self, parent, text, icon=""):
        tk.Label(parent, text=f" {icon}  {text}" if icon else text,
                 font=("Segoe UI", 16, "bold"), bg=COULEURS["surface"],
                 fg=COULEURS["accent_light"], anchor="w"
                 ).pack(fill="x", padx=16, pady=(16, 4))

    def _subtitle(self, parent, text):
        tk.Label(parent, text=text, font=("Segoe UI", 9),
                 bg=COULEURS["surface"], fg=COULEURS["subtext"], anchor="w"
                 ).pack(fill="x", padx=16, pady=(0, 8))

    def _card(self, parent, **kw):
        pad_x = kw.pop("padx", 14)
        pad_y = kw.pop("pady", 12)
        f = tk.Frame(parent, bg=COULEURS["card"], highlightbackground=COULEURS["card_border"],
                     highlightthickness=1, padx=pad_x, pady=pad_y, **kw)
        f.pack(fill="x", padx=16, pady=6)
        return f

    def _entry(self, parent, placeholder="", **kw):
        e = tk.Entry(parent, font=("Segoe UI", 11), bg=COULEURS["input_bg"],
                     fg=COULEURS["text"], insertbackground=COULEURS["accent"],
                     relief="flat", highlightthickness=1, highlightbackground=COULEURS["card_border"],
                     highlightcolor=COULEURS["accent"], **kw)
        if placeholder:
            e.insert(0, placeholder); e.config(fg=COULEURS["subtext"])
            e.bind("<FocusIn>", lambda ev, p=placeholder, en=e:
                   (en.delete(0,"end"), en.config(fg=COULEURS["text"])) if en.get()==p else None)
            e.bind("<FocusOut>", lambda ev, p=placeholder, en=e:
                   (en.insert(0,p), en.config(fg=COULEURS["subtext"])) if not en.get() else None)
        return e

    def _btn(self, parent, text, cmd, color=None, **kw):
        c = color or COULEURS["accent"]
        b = tk.Button(parent, text=text, command=cmd, font=("Segoe UI", 10, "bold"),
                      fg="white", bg=c, activebackground=COULEURS["accent_light"],
                      relief="flat", cursor="hand2", padx=16, pady=6, **kw)
        return b

    def _btn_row(self, parent, buttons_data):
        fr = tk.Frame(parent, bg=COULEURS["card"])
        fr.pack(fill="x", pady=6)
        for txt, cmd, col in buttons_data:
            self._btn(fr, txt, cmd, col).pack(side="left", padx=3)
        return fr

    def _result(self, parent, text="—"):
        lbl = tk.Label(parent, text=text, font=("Consolas", 10),
                       bg=COULEURS["card"], fg=COULEURS["result_fg"],
                       wraplength=700, justify="left", anchor="w",
                       padx=12, pady=10, highlightbackground=COULEURS["card_border"],
                       highlightthickness=1)
        lbl.pack(fill="x", padx=16, pady=6)
        return lbl

    def _label(self, parent, text, **kw):
        tk.Label(parent, text=text, bg=COULEURS["card"], fg=COULEURS["subtext"],
                 font=("Segoe UI", 9), anchor="w", **kw).pack(anchor="w", pady=(4, 2))

    def _save(self, cat, detail):
        try:
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {cat}: {detail}\n")
        except: pass


    # ═══════════════════════════════════════════════════════════
    #   1. CALCULATRICE STANDARD
    # ═══════════════════════════════════════════════════════════
    def _build_calc(self, parent):
        self._title(parent, "Calculatrice Standard", "🧮")

        # Screen
        scr = self._card(parent, padx=12, pady=10)
        self.calc_hist_var = tk.StringVar()
        tk.Label(scr, textvariable=self.calc_hist_var, font=("Consolas", 9),
                 bg=COULEURS["card"], fg=COULEURS["subtext"], anchor="e").pack(fill="x")
        self.calc_disp = tk.Entry(scr, font=("Consolas", 28), borderwidth=0, justify="right",
                                  bg=COULEURS["card"], fg=COULEURS["text"],
                                  insertbackground=COULEURS["accent"], relief="flat")
        self.calc_disp.pack(fill="x", ipady=10)
        self.calc_disp.bind("<Return>", lambda e: self._calc_eq())

        # Angle + Memory
        fr_am = tk.Frame(parent, bg=COULEURS["surface"])
        fr_am.pack(fill="x", padx=16, pady=4)
        self.angle_var = tk.StringVar(value="deg")
        for t, v in [("DEG","deg"),("RAD","rad")]:
            tk.Radiobutton(fr_am, text=t, variable=self.angle_var, value=v,
                           command=lambda: self.calc_engine.set_angle_mode(self.angle_var.get()),
                           bg=COULEURS["surface"], fg=COULEURS["subtext"],
                           selectcolor=COULEURS["card"], font=("Segoe UI",9),
                           activebackground=COULEURS["surface"]).pack(side="left", padx=6)
        self.mem_lbl = tk.Label(fr_am, text="M: 0", font=("Segoe UI",9),
                                bg=COULEURS["surface"], fg=COULEURS["accent"])
        self.mem_lbl.pack(side="right", padx=8)
        for t, c in [("MC",self._mem_c),("MR",self._mem_r),("M+",self._mem_a),("M-",self._mem_s),("MS",self._mem_st)]:
            tk.Button(fr_am, text=t, command=c, font=("Segoe UI",9), fg=COULEURS["subtext"],
                      bg=COULEURS["surface"], relief="flat", cursor="hand2").pack(side="left")

        # Buttons
        btns = [["C","⌫","%","÷"],["7","8","9","×"],["4","5","6","−"],["1","2","3","+"],["±","0",".","="]]
        gf = tk.Frame(parent, bg=COULEURS["surface"])
        gf.pack(fill="both", expand=True, padx=16, pady=8)
        for r, row in enumerate(btns):
            for c, b in enumerate(row):
                bg = COULEURS["accent"] if b=="=" else COULEURS["btn"]
                tk.Button(gf, text=b, font=("Segoe UI",16,"bold"), fg="white", bg=bg, relief="flat",
                          cursor="hand2", command=lambda x=b: self._calc_click(x)
                          ).grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
            gf.grid_columnconfigure(c, weight=1)
        for i in range(5): gf.grid_rowconfigure(i, weight=1)

    def _calc_click(self, k):
        d = self.calc_disp
        if k=="=": self._calc_eq()
        elif k=="C": d.delete(0,tk.END); self.calc_hist_var.set("")
        elif k=="⌫": d.delete(len(d.get())-1, tk.END)
        elif k=="±":
            v=d.get()
            d.delete(0,tk.END); d.insert(0, v[1:] if v.startswith("-") else "-"+v)
        elif k=="%":
            try:
                r=float(d.get())/100; d.delete(0,tk.END); d.insert(0,str(r))
            except: pass
        else: d.insert(tk.END, k)

    def _calc_eq(self):
        expr = self.calc_disp.get()
        self.calc_engine.set_angle_mode(self.angle_var.get())
        r, e = self.calc_engine.evaluate(expr)
        if e: messagebox.showerror("Erreur", e)
        else:
            self.calc_hist_var.set(f"{expr} =")
            self.calc_disp.delete(0,tk.END); self.calc_disp.insert(0, str(r))
            self._save("CALC", f"{expr} = {r}")

    def _mem_c(self): self.calc_engine.memory=0; self.mem_lbl.config(text="M: 0")
    def _mem_r(self): self.calc_disp.delete(0,tk.END); self.calc_disp.insert(0,str(self.calc_engine.memory))
    def _mem_a(self):
        try: self.calc_engine.memory+=float(self.calc_disp.get()); self.mem_lbl.config(text=f"M: {self.calc_engine.memory}")
        except: pass
    def _mem_s(self):
        try: self.calc_engine.memory-=float(self.calc_disp.get()); self.mem_lbl.config(text=f"M: {self.calc_engine.memory}")
        except: pass
    def _mem_st(self):
        try: self.calc_engine.memory=float(self.calc_disp.get()); self.mem_lbl.config(text=f"M: {self.calc_engine.memory}")
        except: pass


    # ═══════════════════════════════════════════════════════════
    #   2. CALCULATRICE SCIENTIFIQUE
    # ═══════════════════════════════════════════════════════════
    def _build_sci(self, parent):
        self._title(parent, "Calculatrice Scientifique", "🔬")

        scr = self._card(parent, padx=12, pady=10)
        self.sci_hist = tk.StringVar()
        tk.Label(scr, textvariable=self.sci_hist, font=("Consolas",9),
                 bg=COULEURS["card"], fg=COULEURS["subtext"], anchor="e").pack(fill="x")
        self.sci_disp = tk.Entry(scr, font=("Consolas",22), borderwidth=0, justify="right",
                                 bg=COULEURS["card"], fg=COULEURS["text"],
                                 insertbackground=COULEURS["accent"], relief="flat")
        self.sci_disp.pack(fill="x", ipady=8)
        self.sci_disp.bind("<Return>", lambda e: self._sci_eq())

        # Constants
        cf = self._card(parent)
        for n, v in [("π","pi"),("e","e"),("φ","phi")]:
            tk.Button(cf, text=n, font=("Segoe UI",10,"bold"), fg=COULEURS["accent"],
                      bg=COULEURS["card"], relief="flat", cursor="hand2",
                      command=lambda x=v: self.sci_disp.insert(tk.END, x)).pack(side="left", padx=4)

        # Function rows
        for funcs in [
            ["sin","cos","tan","log","ln","√"],
            ["asin","acos","atan","sinh","cosh","tanh"],
            [("x²","^2"),("x³","^3"),("xʸ","^"),("n!","factorial("),("|x|","abs("),("⌊x⌋","floor(")],
        ]:
            ff = tk.Frame(parent, bg=COULEURS["surface"])
            ff.pack(fill="x", padx=16, pady=2)
            for item in funcs:
                if isinstance(item, tuple): txt, val = item
                else: txt, val = item, item+"("
                tk.Button(ff, text=txt, font=("Segoe UI",9), fg=COULEURS["accent"], bg=COULEURS["card"],
                          relief="flat", cursor="hand2",
                          command=lambda v=val: self.sci_disp.insert(tk.END, v)
                          ).pack(side="left", padx=2, expand=True, fill="x")

        btns = [["(",")","^","÷"],["7","8","9","×"],["4","5","6","−"],["1","2","3","+"],["C","0",".","="]]
        gf = tk.Frame(parent, bg=COULEURS["surface"])
        gf.pack(fill="both", expand=True, padx=16, pady=6)
        for r, row in enumerate(btns):
            for c, b in enumerate(row):
                bg = COULEURS["accent"] if b=="=" else COULEURS["btn"]
                tk.Button(gf, text=b, font=("Segoe UI",13,"bold"), fg="white", bg=bg, relief="flat",
                          cursor="hand2", command=lambda x=b: self._sci_click(x)
                          ).grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
            gf.grid_columnconfigure(c, weight=1)
        for i in range(5): gf.grid_rowconfigure(i, weight=1)

    def _sci_click(self, k):
        if k=="=": self._sci_eq()
        elif k=="C": self.sci_disp.delete(0,tk.END); self.sci_hist.set("")
        else:
            m = {"÷":"/","×":"*","−":"-"}
            self.sci_disp.insert(tk.END, m.get(k,k))

    def _sci_eq(self):
        expr = self.sci_disp.get()
        self.calc_engine.set_angle_mode(self.angle_var.get() if hasattr(self,'angle_var') else "deg")
        r, e = self.calc_engine.evaluate(expr)
        if e: messagebox.showerror("Erreur", e)
        else:
            self.sci_hist.set(f"{expr} ="); self.sci_disp.delete(0,tk.END)
            self.sci_disp.insert(0, str(r)); self._save("SCI", f"{expr} = {r}")


    # ═══════════════════════════════════════════════════════════
    #   3. STOCKAGE
    # ═══════════════════════════════════════════════════════════
    def _build_storage(self, parent):
        self._title(parent, "Convertisseur de Stockage", "💾")
        c = self._card(parent)
        self._label(c, "Valeur :")
        self.sto_val = self._entry(c); self.sto_val.pack(fill="x", pady=4)
        fr = tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=6)
        self.sto_from = ttk.Combobox(fr, values=["bits","B","KB","MB","GB","TB","PB"], width=10, font=("Segoe UI",10))
        self.sto_from.set("GB"); self.sto_from.pack(side="left", padx=4)
        tk.Label(fr, text="→", bg=COULEURS["card"], fg=COULEURS["accent"], font=("Segoe UI",14)).pack(side="left")
        self.sto_to = ttk.Combobox(fr, values=["bits","B","KB","MB","GB","TB","PB"], width=10, font=("Segoe UI",10))
        self.sto_to.set("MB"); self.sto_to.pack(side="left", padx=4)
        self._btn(c, "Convertir", self._conv_sto, COULEURS["accent"]).pack(pady=6)
        self.sto_res = self._result(parent)
        # Reference
        ref = self._card(parent)
        tk.Label(ref, text="📊 Référence", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w")
        for r in ["1 Byte = 8 bits","1 KB = 1 024 Bytes","1 MB = 1 024 KB","1 GB = 1 024 MB","1 TB = 1 024 GB"]:
            tk.Label(ref, text=r, bg=COULEURS["card"], fg=COULEURS["subtext"], font=("Consolas",9)).pack(anchor="w")

    def _conv_sto(self):
        try:
            v=float(self.sto_val.get()); f=self.sto_from.get(); t=self.sto_to.get()
            fac={"bits":1,"B":8,"KB":8*1024,"MB":8*1024**2,"GB":8*1024**3,"TB":8*1024**4,"PB":8*1024**5}
            r=v*fac[f]/fac[t]
            txt=f"{v:,.4g} {f} = {r:,.6g} {t}"
            self.sto_res.config(text=txt); self._save("STOCKAGE", txt)
        except: messagebox.showerror("Erreur","Valeur invalide")


    # ═══════════════════════════════════════════════════════════
    #   4. UNITÉS
    # ═══════════════════════════════════════════════════════════
    def _build_units(self, parent):
        self._title(parent, "Convertisseur d'Unités", "📏")
        c = self._card(parent)
        self._label(c, "Catégorie :")
        self.unit_cat = ttk.Combobox(c, values=list(UnitConverter.UNITS.keys()), font=("Segoe UI",10))
        self.unit_cat.set("Longueur"); self.unit_cat.pack(fill="x", pady=4)
        self.unit_cat.bind("<<ComboboxSelected>>", self._upd_units)
        self._label(c, "Valeur :")
        self.unit_val = self._entry(c); self.unit_val.pack(fill="x", pady=4)
        fr = tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=6)
        self.unit_from = ttk.Combobox(fr, width=14, font=("Segoe UI",10)); self.unit_from.pack(side="left", padx=4)
        tk.Label(fr, text="→", bg=COULEURS["card"], fg=COULEURS["accent"], font=("Segoe UI",14)).pack(side="left")
        self.unit_to = ttk.Combobox(fr, width=14, font=("Segoe UI",10)); self.unit_to.pack(side="left", padx=4)
        self._btn(c, "Convertir", self._conv_units, COULEURS["accent"]).pack(pady=6)
        self.unit_res = self._result(parent)
        self._upd_units()

    def _upd_units(self, *_):
        cat=self.unit_cat.get(); us=list(UnitConverter.UNITS.get(cat,{}).keys())
        self.unit_from['values']=us; self.unit_to['values']=us
        if us: self.unit_from.set(us[0]); self.unit_to.set(us[1] if len(us)>1 else us[0])

    def _conv_units(self):
        try:
            v=float(self.unit_val.get()); c=self.unit_cat.get(); f=self.unit_from.get(); t=self.unit_to.get()
            r,e = UnitConverter.convert(v,f,t,c)
            if e: messagebox.showerror("Erreur",e)
            else:
                txt=f"{v:,.4g} {f} = {r:,.6g} {t}"; self.unit_res.config(text=txt); self._save("UNITÉS",txt)
        except: messagebox.showerror("Erreur","Valeur invalide")


    # ═══════════════════════════════════════════════════════════
    #   5. DEVISES
    # ═══════════════════════════════════════════════════════════
    def _build_currency(self, parent):
        live = "🟢 Live" if self.taux.get("_live") else "🔴 Hors-ligne"
        self._title(parent, f"Devises — {live}", "💱")
        c = self._card(parent)
        self._label(c, "Montant :")
        self.cur_val = self._entry(c); self.cur_val.pack(fill="x", pady=4)
        curs = ["EUR","USD","GBP","CAD","XOF (FCFA)","CFA","MAD","TND","NGN","ZAR"]
        fr = tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=6)
        self.cur_from = ttk.Combobox(fr, values=curs, width=14, font=("Segoe UI",10))
        self.cur_from.set("EUR"); self.cur_from.pack(side="left", padx=4)
        tk.Label(fr, text="→", bg=COULEURS["card"], fg=COULEURS["accent"], font=("Segoe UI",14)).pack(side="left")
        self.cur_to = ttk.Combobox(fr, values=curs, width=14, font=("Segoe UI",10))
        self.cur_to.set("XOF (FCFA)"); self.cur_to.pack(side="left", padx=4)
        self._btn_row(c, [("Convertir",self._conv_cur,COULEURS["result_fg"]),("🔄",self._load_rates,COULEURS["btn"])])
        self.cur_res = self._result(parent)
        rc = self._card(parent)
        tk.Label(rc, text="📊 Taux vs FCFA", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        for d in ["EUR","USD","GBP","CAD"]:
            tk.Label(rc, text=f"1 {d} = {self.taux.get(d,0):,.2f} FCFA",
                     bg=COULEURS["card"], fg=COULEURS["text"], font=("Consolas",9)).pack(anchor="w")

    def _conv_cur(self):
        try:
            v=float(self.cur_val.get()); f=self.cur_from.get().split()[0]; t=self.cur_to.get().split()[0]
            fcfa = v if f in ("XOF","CFA") else v*self.taux.get(f,1)
            r = fcfa if t in ("XOF","CFA") else fcfa/self.taux.get(t,1)
            txt=f"{v:,.2f} {f} = {r:,.2f} {t}"; self.cur_res.config(text=txt); self._save("DEVISE",txt)
        except: messagebox.showerror("Erreur","Montant invalide")


    # ═══════════════════════════════════════════════════════════
    #   6. GÉOMÉTRIE
    # ═══════════════════════════════════════════════════════════
    def _build_geometry(self, parent):
        self._title(parent, "Calculateur Géométrique", "📐")
        c = self._card(parent)
        self._label(c, "Figure :")
        figs = ["Cercle","Rectangle","Triangle","Trapèze","Sphère","Cylindre","Cône","Cube","Pyramide"]
        self.geo_fig = ttk.Combobox(c, values=figs, font=("Segoe UI",10)); self.geo_fig.set("Cercle")
        self.geo_fig.pack(fill="x", pady=4)
        self.geo_fig.bind("<<ComboboxSelected>>", self._upd_geo)
        self.geo_ff = tk.Frame(c, bg=COULEURS["card"]); self.geo_ff.pack(fill="x", pady=4)
        self.geo_entries = {}; self._upd_geo()
        self._btn(c, "Calculer", self._calc_geo, COULEURS["accent"]).pack(pady=6)
        self.geo_res = self._result(parent)

    GEO_F = {"Cercle":["Rayon (r)"],"Rectangle":["Longueur","Largeur"],"Triangle":["Base","Hauteur","Côté a","Côté b","Côté c"],
             "Trapèze":["Base 1","Base 2","Hauteur"],"Sphère":["Rayon (r)"],"Cylindre":["Rayon (r)","Hauteur (h)"],
             "Cône":["Rayon (r)","Hauteur (h)"],"Cube":["Côté (a)"],"Pyramide":["Base (b)","Hauteur (h)"]}

    def _upd_geo(self, *_):
        for w in self.geo_ff.winfo_children(): w.destroy()
        self.geo_entries.clear()
        for ch in self.GEO_F.get(self.geo_fig.get(),[]):
            tk.Label(self.geo_ff, text=ch, bg=COULEURS["card"], fg=COULEURS["subtext"],
                     font=("Segoe UI",9)).pack(anchor="w")
            e=self._entry(self.geo_ff); e.pack(fill="x", pady=2); self.geo_entries[ch]=e

    def _calc_geo(self):
        try:
            g=lambda k: float(self.geo_entries[k].get()); fig=self.geo_fig.get(); pi=math.pi; R=[]
            if fig=="Cercle": r=g("Rayon (r)"); R=[f"Rayon: {r}",f"Diamètre: {2*r}",f"Circonférence: {2*pi*r:.4f}",f"Aire: {pi*r**2:.4f}"]
            elif fig=="Rectangle": l,w=g("Longueur"),g("Largeur"); R=[f"Aire: {l*w:.4f}",f"Périmètre: {2*(l+w):.4f}",f"Diagonale: {math.hypot(l,w):.4f}"]
            elif fig=="Triangle":
                b,h,a,bb,c=g("Base"),g("Hauteur"),g("Côté a"),g("Côté b"),g("Côté c")
                s=(a+bb+c)/2; R=[f"Aire (base×h/2): {b*h/2:.4f}",f"Aire (Héron): {math.sqrt(s*(s-a)*(s-bb)*(s-c)):.4f}",f"Périmètre: {a+bb+c:.4f}"]
            elif fig=="Sphère": r=g("Rayon (r)"); R=[f"Volume: {4/3*pi*r**3:.4f}",f"Surface: {4*pi*r**2:.4f}"]
            elif fig=="Cylindre": r,h=g("Rayon (r)"),g("Hauteur (h)"); R=[f"Volume: {pi*r**2*h:.4f}",f"Surface: {2*pi*r*(r+h):.4f}"]
            elif fig=="Cône": r,h=g("Rayon (r)"),g("Hauteur (h)"); ap=math.sqrt(r**2+h**2); R=[f"Volume: {pi*r**2*h/3:.4f}",f"Surface: {pi*r*(r+ap):.4f}"]
            elif fig=="Cube": a=g("Côté (a)"); R=[f"Volume: {a**3:.4f}",f"Surface: {6*a**2:.4f}",f"Diagonale: {a*math.sqrt(3):.4f}"]
            elif fig=="Pyramide": b,h=g("Base (b)"),g("Hauteur (h)"); R=[f"Volume: {b**2*h/3:.4f}",f"Base: {b**2:.4f}"]
            elif fig=="Trapèze": a,b,h=g("Base 1"),g("Base 2"),g("Hauteur"); R=[f"Aire: {(a+b)*h/2:.4f}"]
            self.geo_res.config(text="\n".join(R)); self._save("GEO", f"{fig}: {R[0]}")
        except Exception as e: messagebox.showerror("Erreur",f"Vérifiez les valeurs: {e}")


    # ═══════════════════════════════════════════════════════════
    #   7. STATISTIQUES
    # ═══════════════════════════════════════════════════════════
    def _build_stats(self, parent):
        self._title(parent, "Statistiques & Probabilités", "📊")
        c1 = self._card(parent)
        self._label(c1, "Nombres (virgules) :")
        self.stats_e = self._entry(c1, "10, 20, 30, 40, 50, 60"); self.stats_e.pack(fill="x", pady=4)
        self._btn_row(c1, [("Analyser",self._calc_stats,COULEURS["accent"]),
                           ("Effacer",lambda:(self.stats_e.delete(0,tk.END),self.stats_res.config(text="—")),COULEURS["btn"])])
        self.stats_res = self._result(parent)
        c2 = self._card(parent)
        tk.Label(c2, text="🎲 Combinatoire", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c2, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        for l in ["n =","k ="]:
            tk.Label(fr, text=l, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",10)).pack(side="left")
            e=self._entry(fr, width=8); e.pack(side="left", padx=4)
            if "n" in l: self.comb_n=e
            else: self.comb_k=e
        self._btn_row(c2, [("C(n,k)",self._comb,COULEURS["btn"]),("P(n,k)",self._perm,COULEURS["btn"]),("n!",self._fact,COULEURS["btn"])])
        self.comb_res = self._result(parent)

    def _calc_stats(self):
        try:
            nums=[float(x.strip()) for x in self.stats_e.get().split(",") if x.strip()]
            if not nums: raise ValueError
            n=len(nums); s=sum(nums); mu=s/n; ns=sorted(nums)
            med = ns[n//2] if n%2 else (ns[n//2-1]+ns[n//2])/2
            cnt=Counter(nums); mx=max(cnt.values()); modes=[k for k,v in cnt.items() if v==mx]
            ms=", ".join(map(str,modes)) if mx>1 else "Aucun"
            var=sum((x-mu)**2 for x in nums)/n; sd=math.sqrt(var)
            R=[f"n = {n}",f"Somme: {s:,.4f}",f"Moyenne: {mu:,.4f}",f"Médiane: {med:,.4f}",
               f"Mode: {ms}",f"Min: {min(nums):,.4f}",f"Max: {max(nums):,.4f}",
               f"Étendue: {max(nums)-min(nums):,.4f}",f"Variance: {var:,.4f}",f"Écart-type: {sd:,.4f}"]
            self.stats_res.config(text="\n".join(R)); self._save("STATS",f"n={n}, μ={mu:.2f}, σ={sd:.2f}")
        except Exception as e: messagebox.showerror("Erreur",f"Valeurs invalides: {e}")

    def _comb(self):
        try: n,k=int(self.comb_n.get()),int(self.comb_k.get()); r=math.comb(n,k); self.comb_res.config(text=f"C({n},{k}) = {r:,}"); self._save("COMB",f"C({n},{k})={r}")
        except: messagebox.showerror("Erreur","Entiers requis")
    def _perm(self):
        try: n,k=int(self.comb_n.get()),int(self.comb_k.get()); r=math.perm(n,k); self.comb_res.config(text=f"P({n},{k}) = {r:,}"); self._save("PERM",f"P({n},{k})={r}")
        except: messagebox.showerror("Erreur","Entiers requis")
    def _fact(self):
        try: n=int(self.comb_n.get()); r=math.factorial(n); self.comb_res.config(text=f"{n}! = {r:,}"); self._save("FACT",f"{n}!={r}")
        except: messagebox.showerror("Erreur","Entier requis")


    # ═══════════════════════════════════════════════════════════
    #   8. SÉCURITÉ
    # ═══════════════════════════════════════════════════════════
    def _build_security(self, parent):
        self._title(parent, "Outils de Sécurité", "🔐")
        c1 = self._card(parent)
        tk.Label(c1, text="🔑 Générateur de mot de passe", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c1, bg=COULEURS["card"]); fr.pack(fill="x")
        tk.Label(fr, text="Longueur:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.pwd_len=tk.Spinbox(fr, from_=8, to=64, width=5, font=("Segoe UI",10))
        self.pwd_len.delete(0,tk.END); self.pwd_len.insert(0,"16"); self.pwd_len.pack(side="left", padx=8)
        self._btn(fr,"Générer",self._gen_pwd,COULEURS["result_fg"]).pack(side="left", padx=8)
        self.pwd_res = self._entry(c1); self.pwd_res.pack(fill="x", pady=4)
        self.pwd_str = tk.Label(c1, text="", bg=COULEURS["card"], font=("Segoe UI",9)); self.pwd_str.pack(anchor="w")
        of=tk.Frame(c1, bg=COULEURS["card"]); of.pack(fill="x", pady=4)
        self.pw_u=tk.BooleanVar(value=True); self.pw_l=tk.BooleanVar(value=True)
        self.pw_d=tk.BooleanVar(value=True); self.pw_s=tk.BooleanVar(value=True)
        for t,v in [("ABC",self.pw_u),("abc",self.pw_l),("123",self.pw_d),("!@#",self.pw_s)]:
            tk.Checkbutton(of, text=t, variable=v, bg=COULEURS["card"], fg=COULEURS["text"],
                           selectcolor=COULEURS["surface"], font=("Segoe UI",9)).pack(side="left", padx=4)

        c2 = self._card(parent)
        tk.Label(c2, text="🔒 Hachage", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        self._label(c2, "Texte :")
        self.hash_e = self._entry(c2); self.hash_e.pack(fill="x", pady=4)
        self._btn_row(c2, [("MD5",lambda:self._hash("MD5"),COULEURS["btn"]),("SHA1",lambda:self._hash("SHA1"),COULEURS["btn"]),
                          ("SHA256",lambda:self._hash("SHA256"),COULEURS["btn"]),("SHA512",lambda:self._hash("SHA512"),COULEURS["btn"])])
        self.hash_res = self._result(parent)

    def _gen_pwd(self):
        pwd=PasswordGenerator.generate(int(self.pwd_len.get()),self.pw_u.get(),self.pw_l.get(),self.pw_d.get(),self.pw_s.get())
        if pwd:
            self.pwd_res.delete(0,tk.END); self.pwd_res.insert(0,pwd)
            s,l,_=PasswordGenerator.check_strength(pwd)
            self.pwd_str.config(text=f"Force: {l} ({s}/7)", fg=COULEURS["text"])
            self._save("PWD",f"Généré ({len(pwd)} car.)")

    def _hash(self, algo):
        t=self.hash_e.get()
        if not t: return
        h={"MD5":hashlib.md5,"SHA1":hashlib.sha1,"SHA256":hashlib.sha256,"SHA512":hashlib.sha512}[algo](t.encode()).hexdigest()
        self.hash_res.config(text=f"{algo}:\n{h}"); self._save("HASH",f"{algo}: {h[:32]}...")


    # ═══════════════════════════════════════════════════════════
    #   9. DATES
    # ═══════════════════════════════════════════════════════════
    def _build_dates(self, parent):
        self._title(parent, "Calculateur de Date", "📅")
        now = datetime.now()
        c1 = self._card(parent)
        tk.Label(c1, text=f"Aujourd'hui: {now.strftime('%d/%m/%Y %H:%M:%S')}", bg=COULEURS["card"],
                 fg=COULEURS["accent"], font=("Segoe UI",11,"bold")).pack(anchor="w")
        tk.Label(c1, text=f"Semaine {now.isocalendar()[1]}, Jour {now.timetuple().tm_yday}",
                 bg=COULEURS["card"], fg=COULEURS["subtext"], font=("Segoe UI",9)).pack(anchor="w")

        c2 = self._card(parent)
        tk.Label(c2, text="⏱️ Différence entre dates", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c2, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        tk.Label(fr, text="De:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.dt_from = self._entry(fr, now.strftime("%d/%m/%Y"), width=12); self.dt_from.pack(side="left", padx=4)
        tk.Label(fr, text="À:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.dt_to = self._entry(fr, width=12); self.dt_to.pack(side="left", padx=4)
        self._btn(c2,"Calculer",self._calc_ddate,COULEURS["accent"]).pack(pady=6)
        self.ddate_res = self._result(parent)

        c3 = self._card(parent)
        tk.Label(c3, text="➕➖ Ajouter/Retirer des jours", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr2=tk.Frame(c3, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        tk.Label(fr2, text="Date:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.dt_base = self._entry(fr2, now.strftime("%d/%m/%Y"), width=12); self.dt_base.pack(side="left", padx=4)
        tk.Label(fr2, text="Jours:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.dt_days = self._entry(fr2, "30", width=6); self.dt_days.pack(side="left", padx=4)
        self._btn_row(c3, [("+ Ajouter",self._add_days,COULEURS["result_fg"]),("- Retirer",self._sub_days,COULEURS["btn"])])
        self.dt_add_res = self._result(parent)

    def _calc_ddate(self):
        try:
            fmt="%d/%m/%Y"; d1=datetime.strptime(self.dt_from.get(),fmt); d2=datetime.strptime(self.dt_to.get(),fmt)
            diff=abs(d2-d1); y=diff.days//365; m=(diff.days%365)//30; d=diff.days%30
            R=[f"Différence: {diff.days} jours",f"≈ {y} ans, {m} mois, {d} jours",f"Semaines: {diff.days//7} sem. + {diff.days%7} j.",f"Heures: {diff.days*24:,}"]
            self.ddate_res.config(text="\n".join(R)); self._save("DATE",f"Diff: {diff.days}j")
        except Exception as e: messagebox.showerror("Erreur",f"Format JJ/MM/AAAA: {e}")

    def _add_days(self):
        try:
            b=datetime.strptime(self.dt_base.get(),"%d/%m/%Y"); d=int(self.dt_days.get()); r=b+timedelta(days=d)
            self.dt_add_res.config(text=f"Nouvelle date: {r.strftime('%d/%m/%Y')} ({r.strftime('%A %d %B %Y')})")
            self._save("DATE",f"+{d}j = {r.strftime('%d/%m/%Y')}")
        except Exception as e: messagebox.showerror("Erreur",str(e))

    def _sub_days(self):
        try:
            b=datetime.strptime(self.dt_base.get(),"%d/%m/%Y"); d=int(self.dt_days.get()); r=b-timedelta(days=d)
            self.dt_add_res.config(text=f"Nouvelle date: {r.strftime('%d/%m/%Y')} ({r.strftime('%A %d %B %Y')})")
            self._save("DATE",f"-{d}j = {r.strftime('%d/%m/%Y')}")
        except Exception as e: messagebox.showerror("Erreur",str(e))


    # ═══════════════════════════════════════════════════════════
    #   10. MINUTEUR & CHRONOMÈTRE
    # ═══════════════════════════════════════════════════════════
    def _build_timer(self, parent):
        self._title(parent, "Minuteur & Chronomètre", "⏱️")
        c1 = self._card(parent)
        tk.Label(c1, text="⏱️ Chronomètre", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        self.sw_disp = tk.Label(c1, text="00:00:00.000", font=("Consolas",28),
                                bg=COULEURS["card"], fg=COULEURS["text"])
        self.sw_disp.pack(pady=10)
        self._btn_row(c1, [("▶ Start",self._sw_start,COULEURS["result_fg"]),("⏸ Stop",self._sw_stop,COULEURS["btn"]),
                           ("🔄 Reset",self._sw_reset,COULEURS["btn"])])

        c2 = self._card(parent)
        tk.Label(c2, text="⏰ Minuteur", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c2, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        tk.Label(fr, text="Min:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.tmr_min=tk.Spinbox(fr, from_=0, to=999, width=5, font=("Segoe UI",10))
        self.tmr_min.delete(0,tk.END); self.tmr_min.insert(0,"5"); self.tmr_min.pack(side="left", padx=4)
        tk.Label(fr, text="Sec:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.tmr_sec=tk.Spinbox(fr, from_=0, to=59, width=5, font=("Segoe UI",10))
        self.tmr_sec.delete(0,tk.END); self.tmr_sec.insert(0,"0"); self.tmr_sec.pack(side="left", padx=4)
        self.tmr_disp = tk.Label(c2, text="05:00", font=("Consolas",28),
                                 bg=COULEURS["card"], fg=COULEURS["text"])
        self.tmr_disp.pack(pady=10)
        self._btn_row(c2, [("▶ Start",self._tmr_start,COULEURS["result_fg"]),("⏸ Stop",self._tmr_stop,COULEURS["btn"]),
                           ("🔄 Reset",self._tmr_reset,COULEURS["btn"])])

    def _sw_start(self):
        if not getattr(self,'stopwatch_running',False):
            self.stopwatch_running=True; self.sw_start_t=time.time()-getattr(self,'sw_elapsed',0); self._sw_upd()
    def _sw_stop(self): self.stopwatch_running=False
    def _sw_reset(self): self.stopwatch_running=False; self.sw_elapsed=0; self.sw_disp.config(text="00:00:00.000")
    def _sw_upd(self):
        if getattr(self,'stopwatch_running',False):
            e=time.time()-self.sw_start_t; self.sw_elapsed=e
            h,m,s,ms=int(e//3600),int(e%3600//60),int(e%60),int(e%1*1000)
            self.sw_disp.config(text=f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"); self.root.after(10,self._sw_upd)

    def _tmr_start(self):
        if not self.timer_running:
            self.timer_running=True
            try: self.tmr_rem=int(self.tmr_min.get())*60+int(self.tmr_sec.get())
            except: self.tmr_rem=300
            self._tmr_upd()
    def _tmr_stop(self): self.timer_running=False
    def _tmr_reset(self):
        self.timer_running=False
        try: self.tmr_disp.config(text=f"{int(self.tmr_min.get()):02d}:{int(self.tmr_sec.get()):02d}",fg=COULEURS["text"])
        except: self.tmr_disp.config(text="05:00",fg=COULEURS["text"])
    def _tmr_upd(self):
        if self.timer_running and self.tmr_rem>0:
            m,s=self.tmr_rem//60,self.tmr_rem%60
            self.tmr_disp.config(text=f"{m:02d}:{s:02d}",fg=COULEURS["text"])
            self.tmr_rem-=1; self.root.after(1000,self._tmr_upd)
        elif self.tmr_rem<=0:
            self.timer_running=False; self.tmr_disp.config(text="00:00",fg=COULEURS["btn"])
            messagebox.showinfo("Minuteur","⏰ Temps écoulé !")


    # ═══════════════════════════════════════════════════════════
    #   11. RÉSEAU
    # ═══════════════════════════════════════════════════════════
    def _build_network(self, parent):
        self._title(parent, "Outils Réseau", "🌐")
        c1 = self._card(parent)
        tk.Label(c1, text="📡 CIDR", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        self._label(c1, "CIDR (ex: 192.168.1.0/24) :")
        self.cidr_e = self._entry(c1, "192.168.1.0/24"); self.cidr_e.pack(fill="x", pady=4)
        self._btn(c1,"Calculer",self._calc_cidr,COULEURS["accent"]).pack(pady=6)
        self.cidr_res = self._result(parent)

        c2 = self._card(parent)
        tk.Label(c2, text="🔍 DNS", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        self.dns_e = self._entry(c2, "google.com"); self.dns_e.pack(fill="x", pady=4)
        self._btn_row(c2, [("Résoudre",self._resolve_dns,COULEURS["accent"]),("Mon IP",self._my_ip,COULEURS["btn"])])
        self.dns_res = self._result(parent)

    def _calc_cidr(self):
        try:
            raw=self.cidr_e.get().strip()
            if "/" in raw: ip_part,n=raw.split("/"); n=int(n)
            else: n=int(raw); ip_part=None
            mask=[0,0,0,0]
            for i in range(n): mask[i//8]|=(1<<(7-i%8))
            hosts=max(0,2**(32-n)-2); ms=".".join(map(str,mask))
            if ip_part:
                ip_i=struct.unpack("!I",socket.inet_aton(ip_part))[0]; m_i=(0xFFFFFFFF<<(32-n))&0xFFFFFFFF
                net_i=ip_i&m_i; bc_i=net_i|(~m_i&0xFFFFFFFF)
                R=[f"Réseau: {socket.inet_ntoa(struct.pack('!I',net_i))}",
                   f"Broadcast: {socket.inet_ntoa(struct.pack('!I',bc_i))}",
                   f"Plage: {socket.inet_ntoa(struct.pack('!I',net_i+1))} → {socket.inet_ntoa(struct.pack('!I',bc_i-1))}",
                   f"Masque: {ms}",f"Hôtes: {hosts:,}"]
            else: R=[f"Préfixe: /{n}",f"Masque: {ms}",f"Hôtes: {hosts:,}"]
            self.cidr_res.config(text="\n".join(R)); self._save("CIDR",f"/{n}: {hosts:,} hôtes")
        except Exception as e: messagebox.showerror("Erreur",str(e))

    def _resolve_dns(self):
        try:
            h=self.dns_e.get().strip(); ip=socket.gethostbyname(h)
            self.dns_res.config(text=f"{h} → {ip}"); self._save("DNS",f"{h}→{ip}")
        except Exception as e: self.dns_res.config(text=f"Erreur: {e}")

    def _my_ip(self):
        try:
            r=requests.get("https://api.ipify.org?format=json",timeout=5); ip=r.json()["ip"]
            self.dns_res.config(text=f"🌐 IP publique: {ip}"); self._save("IP",ip)
        except: self.dns_res.config(text="Impossible de récupérer l'IP")


    # ═══════════════════════════════════════════════════════════
    #   12. TEXTE
    # ═══════════════════════════════════════════════════════════
    def _build_text(self, parent):
        self._title(parent, "Outils Texte", "📝")
        c1 = self._card(parent)
        self.txt_in = tk.Text(c1, height=5, font=("Segoe UI",10), bg=COULEURS["input_bg"],
                              fg=COULEURS["text"], insertbackground=COULEURS["accent"],
                              relief="flat", padx=8, pady=6)
        self.txt_in.pack(fill="x", pady=4)
        self._btn_row(c1, [("📊 Analyser",self._analyze_txt,COULEURS["accent"]),
                           ("abc",lambda:self._trans_txt("lower"),COULEURS["btn"]),
                           ("ABC",lambda:self._trans_txt("upper"),COULEURS["btn"]),
                           ("🔄",lambda:self._trans_txt("reverse"),COULEURS["btn"])])
        c2 = self._card(parent)
        tk.Label(c2, text="🔐 Encodage", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        self._btn_row(c2, [("B64 Enc",self._b64e,COULEURS["btn"]),("B64 Dec",self._b64d,COULEURS["btn"]),
                          ("URL Enc",self._urle,COULEURS["btn"]),("URL Dec",self._urld,COULEURS["btn"])])
        self.txt_res = self._result(parent)

    def _gtxt(self): return self.txt_in.get("1.0","end-1c")
    def _stxt(self, t): self.txt_in.delete("1.0",tk.END); self.txt_in.insert("1.0",t)

    def _analyze_txt(self):
        t=self._gtxt()
        if not t: return
        w=len(t.split()); ch=len(t); cw=len(t.replace(" "," ","")); ln=t.count("\n")+1
        s=len([x for x in t.replace("!",".").replace("?",".").split(".") if x.strip()])
        v=sum(1 for c in t.lower() if c in "aeiouyàâéèêëîïôùûü")
        wf=Counter(t.lower().split()); top=wf.most_common(3)
        R=[f"Caractères: {ch} (sans espaces: {cw})",f"Mots: {w}",f"Lignes: {ln}",
           f"Phrases: {s}",f"Voyelles: {v}",f"Top mots: {', '.join(f'{x}({y})' for x,y in top)}"]
        self.txt_res.config(text="\n".join(R)); self._save("TEXTE",f"{w} mots, {ch} car.")

    def _trans_txt(self, m):
        t=self._gtxt()
        self._stxt(t.lower() if m=="lower" else t.upper() if m=="upper" else t[::-1])

    def _b64e(self):
        try: self.txt_res.config(text=f"Base64:\n{base64.b64encode(self._gtxt().encode()).decode()}")
        except Exception as e: messagebox.showerror("Erreur",str(e))
    def _b64d(self):
        try: self.txt_res.config(text=f"Décodé:\n{base64.b64decode(self._gtxt().encode()).decode()}")
        except: messagebox.showerror("Erreur","Base64 invalide")
    def _urle(self):
        try: from urllib.parse import quote; self.txt_res.config(text=f"URL:\n{quote(self._gtxt())}")
        except Exception as e: messagebox.showerror("Erreur",str(e))
    def _urld(self):
        try: from urllib.parse import unquote; self.txt_res.config(text=f"Décodé:\n{unquote(self._gtxt())}")
        except Exception as e: messagebox.showerror("Erreur",str(e))


    # ═══════════════════════════════════════════════════════════
    #   13. CONVERTISSEUR DE COULEURS
    # ═══════════════════════════════════════════════════════════
    def _build_colors(self, parent):
        self._title(parent, "Convertisseur de Couleurs", "🎨")
        c1 = self._card(parent)
        self._label(c1, "Couleur HEX (#RRGGBB) :")
        fr_h = tk.Frame(c1, bg=COULEURS["card"]); fr_h.pack(fill="x", pady=4)
        self.col_hex = self._entry(fr_h, "#7c5ce7"); self.col_hex.pack(side="left", fill="x", expand=True, padx=(0,4))
        self._btn(fr_h, "Appliquer", self._col_from_hex, COULEURS["accent"]).pack(side="left")
        self._label(c1, "RGB :")
        fr_r = tk.Frame(c1, bg=COULEURS["card"]); fr_r.pack(fill="x", pady=4)
        self.col_r=tk.Spinbox(fr_r, from_=0, to=255, width=6, font=("Segoe UI",10))
        self.col_r.delete(0,tk.END); self.col_r.insert(0,"124"); self.col_r.pack(side="left", padx=4)
        self.col_g=tk.Spinbox(fr_r, from_=0, to=255, width=6, font=("Segoe UI",10))
        self.col_g.delete(0,tk.END); self.col_g.insert(0,"92"); self.col_g.pack(side="left", padx=4)
        self.col_b=tk.Spinbox(fr_r, from_=0, to=255, width=6, font=("Segoe UI",10))
        self.col_b.delete(0,tk.END); self.col_b.insert(0,"231"); self.col_b.pack(side="left", padx=4)
        self._btn(fr_r, "Appliquer", self._col_from_rgb, COULEURS["accent"]).pack(side="left", padx=4)
        # Preview
        self.col_canvas = tk.Canvas(c1, width=400, height=80, bg="#7c5ce7",
                                    highlightbackground=COULEURS["card_border"], highlightthickness=1)
        self.col_canvas.pack(fill="x", pady=8)
        self.col_info = self._result(parent, "#7c5ce7 → RGB(124, 92, 231) → HSL(261°, 76%, 63%)")

    def _hex_to_rgb(self, h):
        h=h.lstrip("#"); return tuple(int(h[i:i+2],16) for i in (0,2,4))

    def _rgb_to_hex(self, r,g,b): return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

    def _rgb_to_hsl(self, r,g,b):
        r,g,b=r/255,g/255,b/255; mx=max(r,g,b); mn=min(r,g,b); l=(mx+mn)/2
        if mx==mn: h=s=0
        else:
            d=mx-mn; s=d/(2-mx-mn) if l>0.5 else d/(mx+mn)
            if mx==r: h=(g-b)/d+(6 if g<b else 0)
            elif mx==g: h=(b-r)/d+2
            else: h=(r-g)/d+4
            h/=6
        return round(h*360), round(s*100), round(l*100)

    def _col_from_hex(self):
        try:
            h=self.col_hex.get().strip()
            if not h.startswith("#"): h="#"+h
            r,g,b=self._hex_to_rgb(h); hs,l,s=self._rgb_to_hsl(r,g,b)
            self.col_r.delete(0,tk.END); self.col_r.insert(0,str(r))
            self.col_g.delete(0,tk.END); self.col_g.insert(0,str(g))
            self.col_b.delete(0,tk.END); self.col_b.insert(0,str(b))
            comp=self._rgb_to_hex(255-r,255-g,255-b)
            self.col_canvas.config(bg=h)
            self.col_info.config(text=f"{h} → RGB({r}, {g}, {b}) → HSL({hs}°, {s}%, {l}%)\nComplémentaire: {comp}")
            self._save("COULEUR",f"{h} → RGB({r},{g},{b})")
        except: messagebox.showerror("Erreur","HEX invalide")

    def _col_from_rgb(self):
        try:
            r,g,b=int(self.col_r.get()),int(self.col_g.get()),int(self.col_b.get())
            h=self._rgb_to_hex(r,g,b); hs,l,s=self._rgb_to_hsl(r,g,b); comp=self._rgb_to_hex(255-r,255-g,255-b)
            self.col_hex.delete(0,tk.END); self.col_hex.insert(0,h)
            self.col_canvas.config(bg=h)
            self.col_info.config(text=f"{h} → RGB({r}, {g}, {b}) → HSL({hs}°, {s}%, {l}%)\nComplémentaire: {comp}")
            self._save("COULEUR",f"{h} → RGB({r},{g},{b})")
        except: messagebox.showerror("Erreur","RGB invalide")


    # ═══════════════════════════════════════════════════════════
    #   14. CONVERTISSEUR DE BASES
    # ═══════════════════════════════════════════════════════════
    def _build_bases(self, parent):
        self._title(parent, "Convertisseur de Bases", "🔢")
        c = self._card(parent)
        self._label(c, "Nombre :")
        self.base_e = self._entry(c, "255"); self.base_e.pack(fill="x", pady=4)
        self._label(c, "Base source :")
        fr=tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        self.base_from = ttk.Combobox(fr, values=["2 (Binaire)","8 (Octal)","10 (Décimal)","16 (Hexa)"],
                                      font=("Segoe UI",10)); self.base_from.set("10 (Décimal)")
        self.base_from.pack(side="left", fill="x", expand=True, padx=(0,4))
        self._btn(fr, "Convertir", self._conv_base, COULEURS["accent"]).pack(side="left")
        self.base_res = self._result(parent)

    def _conv_base(self):
        try:
            v=self.base_e.get().strip(); fb=int(self.base_from.get().split()[0])
            d=int(v, fb)
            results=[f"Décimal (10): {d}",f"Binaire (2):  {bin(d)[2:]}",f"Octal (8):    {oct(d)[2:]}",
                     f"Hexadécimal (16): {hex(d)[2:].upper()}"]
            if 32<=d<=126: results.append(f"ASCII: '{chr(d)}'")
            self.base_res.config(text="\n".join(results)); self._save("BASE",f"{v}→ déc={d}")
        except: messagebox.showerror("Erreur","Nombre ou base invalide")


    # ═══════════════════════════════════════════════════════════
    #   15. POURCENTAGES
    # ═══════════════════════════════════════════════════════════
    def _build_percent(self, parent):
        self._title(parent, "Calculatrice de Pourcentages", "📊")
        c1 = self._card(parent)
        tk.Label(c1, text="% d'un nombre", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c1, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        self.pct_val = self._entry(fr, "25", width=8); self.pct_val.pack(side="left", padx=4)
        tk.Label(fr, text="% de", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",10)).pack(side="left")
        self.pct_of = self._entry(fr, "200", width=8); self.pct_of.pack(side="left", padx=4)
        self._btn(fr, "=", self._calc_pct_of, COULEURS["accent"]).pack(side="left", padx=4)

        c2 = self._card(parent)
        tk.Label(c2, text="Augmentation / Réduction", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr2=tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        self.pct_base = self._entry(fr2, "100", width=8); self.pct_base.pack(side="left", padx=4)
        tk.Label(fr2, text="+/− %", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",10)).pack(side="left")
        self.pct_chg = self._entry(fr2, "15", width=8); self.pct_chg.pack(side="left", padx=4)
        self._btn(fr2, "+", lambda:self._calc_pct_chg(True), COULEURS["result_fg"]).pack(side="left", padx=2)
        self._btn(fr2, "−", lambda:self._calc_pct_chg(False), COULEURS["btn"]).pack(side="left", padx=2)

        c3 = self._card(parent)
        tk.Label(c3, text="Valeur initiale (avant %)", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr3=tk.Frame(c3, bg=COULEURS["card"]); fr3.pack(fill="x", pady=4)
        self.pct_final = self._entry(fr3, "130", width=8); self.pct_final.pack(side="left", padx=4)
        tk.Label(fr3, text="= résultat de +", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",10)).pack(side="left")
        self.pct_find = self._entry(fr3, "30", width=8); self.pct_find.pack(side="left", padx=4)
        tk.Label(fr3, text="%", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",10)).pack(side="left")
        self._btn(fr3, "Trouver", self._calc_pct_init, COULEURS["accent"]).pack(side="left", padx=4)

        self.pct_res = self._result(parent)

    def _calc_pct_of(self):
        try:
            r=float(self.pct_val.get())/100*float(self.pct_of.get())
            self.pct_res.config(text=f"{self.pct_val.get()}% de {self.pct_of.get()} = {r}")
        except: messagebox.showerror("Erreur","Valeurs invalides")

    def _calc_pct_chg(self, inc):
        try:
            b=float(self.pct_base.get()); p=float(self.pct_chg.get())
            r=b*(1+p/100) if inc else b*(1-p/100)
            op="+" if inc else "−"
            self.pct_res.config(text=f"{b} {op} {p}% = {r}")
        except: messagebox.showerror("Erreur","Valeurs invalides")

    def _calc_pct_init(self):
        try:
            f=float(self.pct_final.get()); p=float(self.pct_find.get())
            r=f/(1+p/100)
            self.pct_res.config(text=f"Valeur initiale: {r:.4f}\n({p}% de {r:.4f} = {p/100*r:.2f} → {r:.4f}+{p/100*r:.2f} = {f})")
        except: messagebox.showerror("Erreur","Valeurs invalides")


    # ═══════════════════════════════════════════════════════════
    #   16. IMC SANTÉ
    # ═══════════════════════════════════════════════════════════
    def _build_health(self, parent):
        self._title(parent, "IMC & Santé", "🏥")
        c1 = self._card(parent)
        tk.Label(c1, text="📏 Indice de Masse Corporelle", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c1, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        tk.Label(fr, text="Poids (kg):", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.imc_w = self._entry(fr, "70", width=8); self.imc_w.pack(side="left", padx=4)
        tk.Label(fr, text="Taille (cm):", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.imc_h = self._entry(fr, "175", width=8); self.imc_h.pack(side="left", padx=4)
        self._btn(fr, "Calculer", self._calc_imc, COULEURS["accent"]).pack(side="left", padx=4)
        self.imc_res = self._result(parent)

        c2 = self._card(parent)
        tk.Label(c2, text="🔥 Métabolisme de Base (Mifflin-St Jeor)", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr2=tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        tk.Label(fr2, text="Âge:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.bmr_age = self._entry(fr2, "30", width=6); self.bmr_age.pack(side="left", padx=4)
        self.bmr_sex = ttk.Combobox(fr2, values=["Homme","Femme"], width=8, font=("Segoe UI",9))
        self.bmr_sex.set("Homme"); self.bmr_sex.pack(side="left", padx=4)
        self._btn(fr2, "BMR", self._calc_bmr, COULEURS["result_fg"]).pack(side="left", padx=4)
        self.bmr_res = self._result(parent)

    def _calc_imc(self):
        try:
            w=float(self.imc_w.get()); h=float(self.imc_h.get())/100; imc=w/(h**2)
            if imc<18.5: cat="Insuffisant"
            elif imc<25: cat="Normal"
            elif imc<30: cat="Surpoids"
            else: cat="Obésité"
            pi=round(18.5*h**2,1); ps=round(24.9*h**2,1)
            R=[f"IMC: {imc:.1f} kg/m² — {cat}",f"Poids idéal: {pi} – {ps} kg",
               f"Poids min. normal: {pi} kg",f"Poids max. normal: {ps} kg"]
            self.imc_res.config(text="\n".join(R)); self._save("IMC",f"IMC={imc:.1f} ({cat})")
        except: messagebox.showerror("Erreur","Valeurs invalides")

    def _calc_bmr(self):
        try:
            w=float(self.imc_w.get()); h=float(self.imc_h.get()); a=int(self.bmr_age.get()); s=self.bmr_sex.get()
            if s=="Homme": bmr=10*w+6.25*h-5*a+5
            else: bmr=10*w+6.25*h-5*a-161
            R=[f"BMR: {bmr:.0f} kcal/jour",f"Sédentaire: {bmr*1.2:.0f} kcal",
               f"Modéré: {bmr*1.55:.0f} kcal",f"Actif: {bmr*1.725:.0f} kcal",f"Très actif: {bmr*1.9:.0f} kcal"]
            self.bmr_res.config(text="\n".join(R)); self._save("BMR",f"{bmr:.0f} kcal/j")
        except: messagebox.showerror("Erreur","Valeurs invalides")


    # ═══════════════════════════════════════════════════════════
    #   17. EMPRUNT
    # ═══════════════════════════════════════════════════════════
    def _build_loan(self, parent):
        self._title(parent, "Calculatrice d'Emprunt", "💰")
        c = self._card(parent)
        fr=tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        for lbl, ph, attr in [("Montant (€):","100000","loan_amt"),("Taux annuel (%):","4.5","loan_rate"),("Durée (ans):","20","loan_yrs")]:
            tk.Label(fr, text=lbl, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
            e=self._entry(fr, ph, width=10); e.pack(side="left", padx=4); setattr(self, attr, e)
        self._btn(c, "Calculer", self._calc_loan, COULEURS["accent"]).pack(pady=6)
        self.loan_res = self._result(parent)

    def _calc_loan(self):
        try:
            P=float(self.loan_amt.get()); r=float(self.loan_rate.get())/100/12; n=int(self.loan_yrs.get())*12
            if r==0: M=P/n
            else: M=P*r*(1+r)**n/((1+r)**n-1)
            total=M*n; interest=total-P
            R=[f"💳 Mensualité: {M:,.2f} €",f"💰 Total payé: {total:,.2f} €",
               f"📈 Intérêts: {interest:,.2f} €",f"📊 Coût / mois: {M:,.2f} €",
               f"📊 % intérêts / capital: {interest/P*100:.1f}%"]
            self.loan_res.config(text="\n".join(R)); self._save("EMPRUNT",f"M={M:.2f}€, intérêts={interest:.0f}€")
        except: messagebox.showerror("Erreur","Valeurs invalides")


    # ═══════════════════════════════════════════════════════════
    #   18. NOMBRES ROMAINS
    # ═══════════════════════════════════════════════════════════
    def _build_roman(self, parent):
        self._title(parent, "Nombres Romains", "Ⅶ")
        c1 = self._card(parent)
        tk.Label(c1, text="Arabe → Romain", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c1, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        self.rom_ar = self._entry(fr, "2024"); self.rom_ar.pack(side="left", fill="x", expand=True, padx=(0,4))
        self._btn(fr, "→ Romain", self._to_rom_btn, COULEURS["accent"]).pack(side="left")

        c2 = self._card(parent)
        tk.Label(c2, text="Romain → Arabe", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr2=tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        self.rom_rm = self._entry(fr2, "MMXXIV"); self.rom_rm.pack(side="left", fill="x", expand=True, padx=(0,4))
        self._btn(fr2, "→ Arabe", self._from_rom_btn, COULEURS["accent"]).pack(side="left")
        self.rom_res = self._result(parent)

    def _to_roman(self, num):
        vals=[1000,900,500,400,100,90,50,40,10,9,5,4,1]; syms=["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]
        r=""
        for i,v in enumerate(vals):
            while num>=v: r+=syms[i]; num-=v
        return r

    def _from_roman(self, roman):
        roman=roman.upper(); vals={"I":1,"V":5,"X":10,"L":50,"C":100,"D":500,"M":1000}; t=0
        for i in range(len(roman)):
            if i+1<len(roman) and vals[roman[i]]<vals[roman[i+1]]: t-=vals[roman[i]]
            else: t+=vals[roman[i]]
        return t

    def _to_rom_btn(self):
        try:
            n=int(self.rom_ar.get())
            if not 1<=n<=3999: messagebox.showwarning("Attention","Plage: 1-3999"); return
            r=self._to_roman(n); self.rom_res.config(text=f"{n} = {r}"); self._save("ROMAIN",f"{n}→{r}")
        except: messagebox.showerror("Erreur","Entier requis (1-3999)")

    def _from_rom_btn(self):
        try:
            r=self.rom_rm.get(); n=self._from_roman(r)
            self.rom_res.config(text=f"{r} = {n}"); self._save("ROMAIN",f"{r}→{n}")
        except: messagebox.showerror("Erreur","Romain invalide")


    # ═══════════════════════════════════════════════════════════
    #   19. ALÉATOIRE
    # ═══════════════════════════════════════════════════════════
    def _build_random(self, parent):
        self._title(parent, "Générateur Aléatoire", "🧬")
        c1 = self._card(parent)
        tk.Label(c1, text="🔢 Nombre aléatoire", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c1, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        for l,ph,attr in [("Min:","1","rnd_min"),("Max:","100","rnd_max")]:
            tk.Label(fr, text=l, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
            e=self._entry(fr, ph, width=8); e.pack(side="left", padx=4); setattr(self, attr, e)
        self._btn(fr, "Générer", self._rnd_num, COULEURS["accent"]).pack(side="left", padx=4)
        self.rnd_num_res = tk.Label(c1, text="", bg=COULEURS["card"], fg=COULEURS["result_fg"],
                                    font=("Consolas", 14, "bold")); self.rnd_num_res.pack(pady=4)

        c2 = self._card(parent)
        tk.Label(c2, text="🎲 Dés & Pièces", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr2=tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        self._btn(fr2, "🎲 Dé 6", lambda:self._roll_dice(6), COULEURS["btn"]).pack(side="left", padx=4)
        self._btn(fr2, "🎲 Dé 20", lambda:self._roll_dice(20), COULEURS["btn"]).pack(side="left", padx=4)
        self._btn(fr2, "🪙 Pile/Face", self._coin_flip, COULEURS["accent"]).pack(side="left", padx=4)
        self._btn(fr2, "🎰 Loto (6/49)", self._lotto, COULEURS["result_fg"]).pack(side="left", padx=4)
        self.rnd_game_res = tk.Label(c2, text="", bg=COULEURS["card"], fg=COULEURS["result_fg"],
                                    font=("Consolas", 12, "bold")); self.rnd_game_res.pack(pady=4)

    def _rnd_num(self):
        try:
            mn,mx=int(self.rnd_min.get()),int(self.rnd_max.get())
            self.rnd_num_res.config(text=f"→ {random.randint(mn,mx)}")
        except: messagebox.showerror("Erreur","Valeurs invalides")

    def _roll_dice(self, sides):
        r=random.randint(1,sides); self.rnd_game_res.config(text=f"🎲 Dé (1-{sides}): {r}")

    def _coin_flip(self):
        r=random.choice(["Pile 🦁","Face 👑"]); self.rnd_game_res.config(text=f"🪙 {r}")

    def _lotto(self):
        nums=sorted(random.sample(range(1,50),6))
        self.rnd_game_res.config(text=f"🎰 Loto: {', '.join(map(str,nums))}"); self._save("LOTO",str(nums))


    # ═══════════════════════════════════════════════════════════
    #   20. CHIFFREMENT CÉSAR / ROT13
    # ═══════════════════════════════════════════════════════════
    def _build_cipher(self, parent):
        self._title(parent, "Chiffrement César / ROT13", "🤫")
        c = self._card(parent)
        self._label(c, "Texte :")
        self.cipher_e = tk.Text(c, height=3, font=("Segoe UI",10), bg=COULEURS["input_bg"],
                                fg=COULEURS["text"], insertbackground=COULEURS["accent"],
                                relief="flat", padx=8, pady=6)
        self.cipher_e.pack(fill="x", pady=4)
        fr=tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        tk.Label(fr, text="Décalage:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.cipher_shift=tk.Spinbox(fr, from_=1, to=25, width=5, font=("Segoe UI",10))
        self.cipher_shift.delete(0,tk.END); self.cipher_shift.insert(0,"3"); self.cipher_shift.pack(side="left", padx=4)
        self._btn(fr, "Chiffrer", self._caesar_enc, COULEURS["accent"]).pack(side="left", padx=4)
        self._btn(fr, "Déchiffrer", self._caesar_dec, COULEURS["btn"]).pack(side="left", padx=4)
        self._btn(fr, "ROT13", self._rot13, COULEURS["btn"]).pack(side="left", padx=4)
        self.cipher_res = self._result(parent)

    def _caesar_enc(self):
        t=self.cipher_e.get("1.0","end-1c"); s=int(self.cipher_shift.get())
        r="".join(chr((ord(c)-ord('A')+s)%26+ord('A')) if c.isupper() else chr((ord(c)-ord('a')+s)%26+ord('a')) if c.islower() else c for c in t)
        self.cipher_res.config(text=f"Chiffré (+{s}):\n{r}"); self._save("CÉSAR",f"+{s}: {r[:30]}...")

    def _caesar_dec(self):
        t=self.cipher_e.get("1.0","end-1c"); s=int(self.cipher_shift.get())
        r="".join(chr((ord(c)-ord('A')-s)%26+ord('A')) if c.isupper() else chr((ord(c)-ord('a')-s)%26+ord('a')) if c.islower() else c for c in t)
        self.cipher_res.config(text=f"Déchiffré (-{s}):\n{r}")

    def _rot13(self):
        t=self.cipher_e.get("1.0","end-1c")
        r="".join(chr((ord(c)-ord('A')+13)%26+ord('A')) if c.isupper() else chr((ord(c)-ord('a')+13)%26+ord('a')) if c.islower() else c for c in t)
        self.cipher_res.config(text=f"ROT13:\n{r}"); self._save("ROT13",r[:30])


    # ═══════════════════════════════════════════════════════════
    #   21. ÉLECTRICITÉ (Loi d'Ohm)
    # ═══════════════════════════════════════════════════════════
    def _build_electric(self, parent):
        self._title(parent, "Loi d'Ohm & Puissance", "⚡")
        c = self._card(parent)
        tk.Label(c, text="Laissez 2 champs vides pour calculer les 2 autres", bg=COULEURS["card"],
                 fg=COULEURS["subtext"], font=("Segoe UI",9,"italic")).pack(anchor="w", pady=(0,6))
        self.elec_entries = {}
        for lbl, ph, key in [("Tension U (V):","","elec_u"),("Intensité I (A):","","elec_i"),
                              ("Résistance R (Ω):","","elec_r"),("Puissance P (W):","","elec_p")]:
            self._label(c, lbl)
            e = self._entry(c, ph); e.pack(fill="x", pady=2); self.elec_entries[key] = e
        self._btn(c, "Calculer", self._calc_elec, COULEURS["accent"]).pack(pady=6)
        self.elec_res = self._result(parent)

    def _calc_elec(self):
        try:
            g=lambda k: float(self.elec_entries[k].get()) if self.elec_entries[k].get() else None
            u,i,r,p=g("elec_u"),g("elec_i"),g("elec_r"),g("elec_p")
            filled = sum(1 for x in [u,i,r,p] if x is not None)
            if filled<2: messagebox.showwarning("Attention","Remplissez au moins 2 champs"); return
            R=[]
            if u is not None and i is not None:
                r_calc=u/i; p_calc=u*i
                if r is None: r=r_calc; R.append(f"R = U/I = {r:.4f} Ω")
                if p is None: p=p_calc; R.append(f"P = U×I = {p:.4f} W")
            if u is not None and r is not None:
                i_calc=u/r; p_calc=u**2/r
                if i is None: i=i_calc; R.append(f"I = U/R = {i:.4f} A")
                if p is None: p=p_calc; R.append(f"P = U²/R = {p:.4f} W")
            if i is not None and r is not None:
                u_calc=i*r; p_calc=i**2*r
                if u is None: u=u_calc; R.append(f"U = R×I = {u:.4f} V")
                if p is None: p=p_calc; R.append(f"P = I²×R = {p:.4f} W")
            if u is not None and p is not None:
                i_calc=p/u
                if i is None: i=i_calc; R.append(f"I = P/U = {i:.4f} A")
            if i is not None and p is not None:
                u_calc=p/i
                if u is None: u=u_calc; R.append(f"U = P/I = {u:.4f} V")
            if r is not None and p is not None:
                u_calc=math.sqrt(p*r)
                if u is None: u=u_calc; R.append(f"U = √(P×R) = {u:.4f} V")
            R.insert(0, f"U={u}V | I={i}A | R={r}Ω | P={p}W" if all(x is not None for x in [u,i,r,p]) else "Résultats:")
            self.elec_res.config(text="\n".join(R)); self._save("ÉLEC",f"U={u},I={i},R={r},P={p}")
        except Exception as e: messagebox.showerror("Erreur",f"Calcul impossible: {e}")


    # ═══════════════════════════════════════════════════════════
    #   22. POURBOIRE
    # ═══════════════════════════════════════════════════════════
    def _build_tip(self, parent):
        self._title(parent, "Calculatrice de Pourboire", "🧮")
        c = self._card(parent)
        fr=tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        for lbl, ph, attr in [("Note (€):","50","tip_bill"),("Pourboire (%):","15","tip_pct"),("Personnes:","2","tip_ppl")]:
            tk.Label(fr, text=lbl, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
            e=self._entry(fr, ph, width=8); e.pack(side="left", padx=4); setattr(self, attr, e)
        self._btn(c, "Calculer", self._calc_tip, COULEURS["accent"]).pack(pady=6)
        self.tip_res = self._result(parent)

    def _calc_tip(self):
        try:
            b=float(self.tip_bill.get()); p=float(self.tip_pct.get())/100; n=int(self.tip_ppl.get())
            tip=b*p; total=b+tip; per=total/n; tip_per=tip/n
            R=[f"💰 Note: {b:,.2f} €",f"💵 Pourboire ({p*100:.0f}%): {tip:,.2f} €",
               f"📊 Total: {total:,.2f} €",f"👥 Par personne: {per:,.2f} €",
               f"👥 Pourboire/personne: {tip_per:,.2f} €"]
            self.tip_res.config(text="\n".join(R)); self._save("POURBOIRE",f"Total={total:.2f}€, /pers={per:.2f}€")
        except: messagebox.showerror("Erreur","Valeurs invalides")


    # ═══════════════════════════════════════════════════════════
    #   23. ÉQUATIONS
    # ═══════════════════════════════════════════════════════════
    def _build_equations(self, parent):
        self._title(parent, "Solveur d'Équations", "📐")
        c1 = self._card(parent)
        tk.Label(c1, text="Équation du 2nd degré: ax² + bx + c = 0", bg=COULEURS["card"],
                 fg=COULEURS["accent"], font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c1, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        self.eq_entries={}
        for l,ph in [("a","1"),("b","-5"),("c","6")]:
            tk.Label(fr, text=l, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",11,"bold")).pack(side="left")
            e=self._entry(fr, ph, width=8); e.pack(side="left", padx=4); self.eq_entries[l]=e
        self._btn(fr, "Résoudre", self._solve_quad, COULEURS["accent"]).pack(side="left", padx=8)
        self.eq_res = self._result(parent)

        c2 = self._card(parent)
        tk.Label(c2, text="Équation du 1er degré: ax + b = 0", bg=COULEURS["card"],
                 fg=COULEURS["accent"], font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr2=tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        for l,ph in [("a","3"),("b","9")]:
            tk.Label(fr2, text=l, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",11,"bold")).pack(side="left")
            e=self._entry(fr2, ph, width=8); e.pack(side="left", padx=4); self.eq_entries["l_"+l]=e
        self._btn(fr2, "Résoudre", self._solve_lin, COULEURS["accent"]).pack(side="left", padx=8)
        self.lin_res = self._result(parent)

    def _solve_quad(self):
        try:
            a=float(self.eq_entries["a"].get()); b=float(self.eq_entries["b"].get()); c=float(self.eq_entries["c"].get())
            if a==0: self.eq_res.config(text="a ne peut pas être 0 (utilisez le 1er degré)"); return
            D=b**2-4*a*c; vx=-b/(2*a)
            if D>0:
                x1=(-b+math.sqrt(D))/(2*a); x2=(-b-math.sqrt(D))/(2*a)
                R=[f"Δ = {D:.4f} (> 0 → 2 racines réelles)",f"x₁ = {x1:.4f}",f"x₂ = {x2:.4f}",f"Sommet: ({vx:.4f}, {-D/(4*a):.4f})"]
            elif D==0:
                R=[f"Δ = 0 → Racine double",f"x = {vx:.4f}",f"Sommet: ({vx:.4f}, 0)"]
            else:
                re=vx; im=math.sqrt(-D)/(2*a)
                R=[f"Δ = {D:.4f} (< 0 → 2 racines complexes)",f"x₁ = {re:.4f} + {im:.4f}i",f"x₂ = {re:.4f} - {im:.4f}i",
                   f"Sommet: ({vx:.4f}, {-D/(4*a):.4f})"]
            self.eq_res.config(text="\n".join(R)); self._save("ÉQUATION",f"ax²+bx+c=0, Δ={D:.2f}")
        except Exception as e: messagebox.showerror("Erreur",str(e))

    def _solve_lin(self):
        try:
            a=float(self.eq_entries["l_a"].get()); b=float(self.eq_entries["l_b"].get())
            if a==0: self.lin_res.config(text="a = 0, pas de solution unique" if b!=0 else "Infinité de solutions"); return
            x=-b/a; self.lin_res.config(text=f"{a}x + {b} = 0\nx = {x:.4f}")
            self._save("ÉQUATION LIN",f"x={x:.4f}")
        except Exception as e: messagebox.showerror("Erreur",str(e))


    # ═══════════════════════════════════════════════════════════
    #   24. MÉTÉO (Wind Chill / Heat Index)
    # ═══════════════════════════════════════════════════════════
    def _build_weather(self, parent):
        self._title(parent, "Indice Météo", "🌡️")
        c1 = self._card(parent)
        tk.Label(c1, text="❄️ Wind Chill (Refroidissement éolien)", bg=COULEURS["card"],
                 fg=COULEURS["accent"], font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        tk.Label(c1, text="Valide si T ≤ 10°C et vent > 4.8 km/h", bg=COULEURS["card"],
                 fg=COULEURS["subtext"], font=("Segoe UI",8,"italic")).pack(anchor="w")
        fr=tk.Frame(c1, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        for lbl, ph, attr in [("Temp (°C):","-5","wc_t"),("Vent (km/h):","20","wc_v")]:
            tk.Label(fr, text=lbl, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
            e=self._entry(fr, ph, width=8); e.pack(side="left", padx=4); setattr(self, attr, e)
        self._btn(fr, "Calculer", self._calc_wc, COULEURS["accent"]).pack(side="left", padx=4)
        self.wc_res = self._result(parent)

        c2 = self._card(parent)
        tk.Label(c2, text="🔥 Heat Index (Indice de chaleur)", bg=COULEURS["card"],
                 fg=COULEURS["btn"], font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        tk.Label(c2, text="Valide si T ≥ 27°C et humidité ≥ 40%", bg=COULEURS["card"],
                 fg=COULEURS["subtext"], font=("Segoe UI",8,"italic")).pack(anchor="w")
        fr2=tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        for lbl, ph, attr in [("Temp (°C):","35","hi_t"),("Humidité (%):","70","hi_h")]:
            tk.Label(fr2, text=lbl, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
            e=self._entry(fr2, ph, width=8); e.pack(side="left", padx=4); setattr(self, attr, e)
        self._btn(fr2, "Calculer", self._calc_hi, COULEURS["btn"]).pack(side="left", padx=4)
        self.hi_res = self._result(parent)

    def _calc_wc(self):
        try:
            T=float(self.wc_t.get()); V=float(self.wc_v.get())
            # FormuleEnvironment Canada
            wc=13.12+0.6215*T-11.37*V**0.16+0.3965*T*V**0.16
            R=[f"Température: {T}°C",f"Vent: {V} km/h",f"Wind Chill: {wc:.1f}°C"]
            if wc<-30: R.append("⚠️ DANGER EXTREME — Exposition < 10 min")
            elif wc<-20: R.append("⚠️ DANGER — Risque d'engelure en 30 min")
            elif wc<-10: R.append("⚠️ Risque modéré")
            else: R.append("✅ Confort acceptable")
            self.wc_res.config(text="\n".join(R))
        except: messagebox.showerror("Erreur","Valeurs invalides")

    def _calc_hi(self):
        try:
            T=float(self.hi_t.get()); H=float(self.hi_h.get())
            # Rothfusz regression (°F), convertir
            Tf=T*9/5+32; hi=0.5*(Tf+61.0+((Tf-68.0)*1.2)+(H*0.094))
            if hi>80:
                hi=-42.379+2.04901523*Tf+10.14333127*H-0.22475541*Tf*H-0.00683783*Tf**2-0.05481717*H**2+0.00122874*Tf**2*H+0.00085282*Tf*H**2-0.00000199*Tf**2*H**2
            hi_c=(hi-32)*5/9
            R=[f"Température: {T}°C",f"Humidité: {H}%",f"Heat Index: {hi_c:.1f}°C"]
            if hi_c>54: R.append("🔴 DANGER DE MORT — Coup de chaleur imminent")
            elif hi_c>41: R.append("🟠 DANGER EXTRÊME")
            elif hi_c>32: R.append("🟡 ATTENTION — Coups de chaleur possibles")
            else: R.append("✅ Confortable")
            self.hi_res.config(text="\n".join(R))
        except: messagebox.showerror("Erreur","Valeurs invalides")


    # ═══════════════════════════════════════════════════════════
    #   25. COMPTEUR DE MOTS AVANCÉ
    # ═══════════════════════════════════════════════════════════
    def _build_wordcount(self, parent):
        self._title(parent, "Compteur de Mots Avancé", "🔤")
        c = self._card(parent)
        tk.Label(c, text="Collez votre texte ici :", bg=COULEURS["card"], fg=COULEURS["subtext"],
                 font=("Segoe UI",9)).pack(anchor="w")
        self.wc_text = tk.Text(c, height=8, font=("Segoe UI",10), bg=COULEURS["input_bg"],
                               fg=COULEURS["text"], insertbackground=COULEURS["accent"],
                               relief="flat", padx=8, pady=6)
        self.wc_text.pack(fill="x", pady=4)
        self._btn(c, "Analyser", self._analyze_wc, COULEURS["accent"]).pack(pady=4)
        self.wc_res = self._result(parent)

    def _analyze_wc(self):
        t = self.wc_text.get("1.0","end-1c")
        if not t: messagebox.showinfo("Info","Entrez du texte"); return
        words = t.split(); wc = len(words); chars = len(t); cns = len(t.replace(" ","","").replace("\n",""))
        lines = t.count("\n")+1
        sentences = len([s for s in t.replace("!",".").replace("?",".").replace("...",".").split(".") if s.strip()])
        paragraphs = len([p for p in t.split("\n\n") if p.strip()])
        avg_wl = sum(len(w) for w in words)/max(len(words),1)
        longest = max(words, key=len) if words else "—"
        reading_min = wc/200; speak_min = wc/130
        # Flesch reading ease (approx)
        syllables = sum(1 for c in t.lower() if c in "aeiouyàâéèêëîïôùûü") + wc  # rough
        flesch = 206.835 - 1.015*(wc/max(sentences,1)) - 84.6*(syllables/max(wc,1))

        R = [
            f"📄 Caractères: {chars} (sans espaces: {cns})",
            f"📝 Mots: {wc}",
            f"📏 Lignes: {lines}",
            f"💬 Phrases: {sentences}",
            f"📋 Paragraphes: {paragraphs}",
            f"📏 Mot le plus long: '{longest}' ({len(longest)} car.)",
            f"📊 Longueur moyenne: {avg_wl:.1f} car./mot",
            f"⏱️ Lecture: ~{reading_min:.1f} min ({reading_min*60:.0f} sec)",
            f"🗣️ Élocution: ~{speak_min:.1f} min ({speak_min*60:.0f} sec)",
            f"📖 Flesch (approx): {flesch:.1f}/100 {'(Facile)' if flesch>60 else '(Difficile)' if flesch<30 else '(Moyen)'}",
        ]
        self.wc_res.config(text="\n".join(R)); self._save("COMPTEUR",f"{wc} mots, {reading_min:.1f} min lecture")


    # ═══════════════════════════════════════════════════════════
    #   26. CONSTANTES PHYSIQUES
    # ═══════════════════════════════════════════════════════════
    def _build_physics(self, parent):
        self._title(parent, "Constantes Physiques", "ℏ")
        c = self._card(parent)
        tk.Label(c, text="Tableau des constantes fondamentales", bg=COULEURS["card"],
                 fg=COULEURS["accent"], font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,6))

        constants = [
            ("c", "Vitesse de la lumière", "299 792 458 m/s"),
            ("G", "Constante gravitationnelle", "6.674 × 10⁻¹¹ N·m²/kg²"),
            ("h", "Constante de Planck", "6.626 × 10⁻³⁴ J·s"),
            ("h̄", "Constante de Planck réduite", "1.055 × 10⁻³⁴ J·s"),
            ("kB", "Constante de Boltzmann", "1.381 × 10⁻²³ J/K"),
            ("NA", "Nombre d'Avogadro", "6.022 × 10²³ /mol"),
            ("e", "Charge élémentaire", "1.602 × 10⁻¹⁹ C"),
            ("ε₀", "Permittivité du vide", "8.854 × 10⁻¹² F/m"),
            ("μ₀", "Perméabilité du vide", "4π × 10⁻⁷ T·m/A"),
            ("R", "Constante des gaz parfaits", "8.314 J/(mol·K)"),
            ("σ", "Constante de Stefan-Boltzmann", "5.670 × 10⁻⁸ W/(m²·K⁴)"),
            ("g", "Gravité terrestre", "9.807 m/s²"),
            ("me", "Masse de l'électron", "9.109 × 10⁻³¹ kg"),
            ("mp", "Masse du proton", "1.673 × 10⁻²⁷ kg"),
            ("mn", "Masse du neutron", "1.675 × 10⁻²⁷ kg"),
        ]

        # Header
        hdr = tk.Frame(c, bg=COULEURS["accent_dim"]); hdr.pack(fill="x", pady=(0,2))
        for txt, w in [("Symbole", 8), ("Nom", 24), ("Valeur", 30)]:
            tk.Label(hdr, text=txt, bg=COULEURS["accent_dim"], fg="white",
                     font=("Segoe UI",9,"bold"), width=w, anchor="w", padx=6).pack(side="left")

        for i, (sym, name, val) in enumerate(constants):
            bg = COULEURS["card"] if i%2==0 else COULEURS["input_bg"]
            row = tk.Frame(c, bg=bg); row.pack(fill="x")
            tk.Label(row, text=sym, bg=bg, fg=COULEURS["accent"], font=("Consolas",10,"bold"),
                     width=8, anchor="w", padx=6).pack(side="left")
            tk.Label(row, text=name, bg=bg, fg=COULEURS["text"], font=("Segoe UI",9),
                     width=24, anchor="w", padx=6).pack(side="left")
            tk.Label(row, text=val, bg=bg, fg=COULEURS["subtext"], font=("Consolas",9),
                     width=30, anchor="w", padx=6).pack(side="left")

        # Quick converter
        c2 = self._card(parent)
        tk.Label(c2, text="Convertisseur rapide", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c2, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        tk.Label(fr, text="Énergie (eV):", bg=COULEURS["card"], fg=COULEURS["text"],
                 font=("Segoe UI",9)).pack(side="left")
        self.phys_eV = self._entry(fr, "1", width=10); self.phys_eV.pack(side="left", padx=4)
        self._btn(fr, "→ J", lambda:self._phys_conv("ev_j"), COULEURS["accent"]).pack(side="left", padx=2)
        self._btn(fr, "→ kJ/mol", lambda:self._phys_conv("ev_kjmol"), COULEURS["accent"]).pack(side="left", padx=2)
        self.phys_res = self._result(parent)

    def _phys_conv(self, mode):
        try:
            ev=float(self.phys_eV.get()); e=1.602e-19
            if mode=="ev_j": r=ev*e; self.phys_res.config(text=f"{ev} eV = {r:.4e} J")
            elif mode=="ev_kjmol": r=ev*e*6.022e23/1000; self.phys_res.config(text=f"{ev} eV = {r:.4f} kJ/mol")
        except: messagebox.showerror("Erreur","Valeur invalide")


    # ═══════════════════════════════════════════════════════════
    #   27. OPÉRATIONS BITWISE (Binaire)
    # ═══════════════════════════════════════════════════════════
    def _build_bitwise(self, parent):
        self._title(parent, "Opérations Bitwise", "🔓")
        c = self._card(parent)
        self._label(c, "Valeur A (entier) :")
        self.bw_a = self._entry(c, "255"); self.bw_a.pack(fill="x", pady=4)
        self._label(c, "Valeur B (entier) :")
        self.bw_b = self._entry(c, "15"); self.bw_b.pack(fill="x", pady=4)
        self._btn_row(c, [
            ("AND &", lambda:self._bitwise_op("&"), COULEURS["accent"]),
            ("OR |", lambda:self._bitwise_op("|"), COULEURS["accent"]),
            ("XOR ^", lambda:self._bitwise_op("^"), COULEURS["btn"]),
            ("NOT ~A", lambda:self._bitwise_op("~"), COULEURS["btn"]),
            ("<< Left", lambda:self._bitwise_op("<<"), COULEURS["result_fg"]),
            (">> Right", lambda:self._bitwise_op(">>"), COULEURS["result_fg"]),
        ])
        self._label(c, "Décalage de A (nombre de bits) :")
        self.bw_shift = self._entry(c, "2"); self.bw_shift.pack(fill="x", pady=4)
        self._btn(c, "Convertir en binaire", self._bitwise_info, COULEURS["btn"]).pack(pady=6)
        self.bw_res = self._result(parent)

    def _bitwise_op(self, op):
        try:
            a=int(self.bw_a.get()); b=int(self.bw_b.get()); s=int(self.bw_shift.get())
            if op=="&": r=a&b; t=f"{a} & {b} = {r}"
            elif op=="|": r=a|b; t=f"{a} | {b} = {r}"
            elif op=="^": r=a^b; t=f"{a} ^ {b} = {r}"
            elif op=="~": r=~a; t=f"~{a} = {r}"
            elif op==">>": r=a>>s; t=f"{a} >> {s} = {r}"
            elif op=="<<": r=a<<s; t=f"{a} << {s} = {r}"
            ab=bin(a)[2:]; bb=bin(b)[2:]; rb=bin(r & 0xFFFFFFFF)[2:]
            self.bw_res.config(text=f"{t}\nA = {ab} ({a})\nB = {bb} ({b})\nR = {rb} ({r})")
            self._save("BITWISE", t)
        except: messagebox.showerror("Erreur","Entiers requis")

    def _bitwise_info(self):
        try:
            a=int(self.bw_a.get()); b=int(self.bw_b.get())
            self.bw_res.config(text=f"A = {a}\n  Binaire    : {bin(a)[2:]}\n  Octal     : {oct(a)[2:]}\n  Hexa      : {hex(a)[2:].upper()}\n\nB = {b}\n  Binaire    : {bin(b)[2:]}\n  Octal     : {oct(b)[2:]}\n  Hexa      : {hex(b)[2:].upper()}")
        except: messagebox.showerror("Erreur","Entiers requis")


    # ═══════════════════════════════════════════════════════════
    #   28. SOLVEUR DE TRIANGLE
    # ═══════════════════════════════════════════════════════════
    def _build_triangle(self, parent):
        self._title(parent, "Solveur de Triangle", "📐")
        c1 = self._card(parent)
        tk.Label(c1, text="Donnez 3 valeurs (côtés/angles), laissez 3 vides", bg=COULEURS["card"],
                 fg=COULEURS["subtext"], font=("Segoe UI",8,"italic")).pack(anchor="w", pady=(0,6))
        self.tri_entries = {}
        for lbl, ph, k in [("Côté a","3","tri_a"),("Côté b","4","tri_b"),("Côté c","5","tri_c"),
                            ("Angle A (°)","","tri_A"),("Angle B (°)","","tri_B"),("Angle C (°)","","tri_C")]:
            self._label(c1, lbl+" :")
            e=self._entry(c1, ph); e.pack(fill="x", pady=2); self.tri_entries[k]=e
        self._btn(c1, "Résoudre", self._solve_tri, COULEURS["accent"]).pack(pady=6)
        self.tri_res = self._result(parent)

        c2 = self._card(parent)
        tk.Label(c2, text="Formules utilisées", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        formulas = "• Loi des cosinus: c² = a² + b² − 2ab·cos(C)\n• Loi des sinus: a/sin(A) = b/sin(B) = c/sin(C)\n• Somme des angles: A + B + C = 180°\n• Aire: √(s(s−a)(s−b)(s−c))  (Héron)"
        tk.Label(c2, text=formulas, bg=COULEURS["card"], fg=COULEURS["subtext"],
                 font=("Consolas",8), justify="left").pack(anchor="w")

    def _solve_tri(self):
        try:
            g=lambda k: float(self.tri_entries[k].get()) if self.tri_entries[k].get() else None
            a,b,c,A,B,C=g("tri_a"),g("tri_b"),g("tri_c"),g("tri_A"),g("tri_B"),g("tri_C")
            # Convert angles to radians if given
            if A is not None: A_r=math.radians(A)
            if B is not None: B_r=math.radians(B)
            if C is not None: C_r=math.radians(C)
            # Case: 3 sides (SSS)
            if a is not None and b is not None and c is not None:
                if a+b<=c or a+c<=b or b+c<=a: messagebox.showerror("Erreur","Triangle impossible"); return
                A_r=math.acos((b**2+c**2-a**2)/(2*b*c)); B_r=math.acos((a**2+c**2-b**2)/(2*a*c))
                C_r=math.pi-A_r-B_r; A,B,C=math.degrees(A_r),math.degrees(B_r),math.degrees(C_r)
            # Case: 2 sides + included angle (SAS)
            elif a is not None and b is not None and C_r is not None:
                c=math.sqrt(a**2+b**2-2*a*b*math.cos(C_r)); A_r=math.acos((b**2+c**2-a**2)/(2*b*c))
                B_r=math.pi-A_r-C_r; A,B,C=math.degrees(A_r),math.degrees(B_r),math.degrees(C_r)
            # Case: 1 side + 2 angles (ASA)
            elif a is not None and B_r is not None and C_r is not None:
                A_r=math.pi-B_r-C_r; b=a*math.sin(B_r)/math.sin(A_r); c=a*math.sin(C_r)/math.sin(A_r)
                A,B,C=math.degrees(A_r),math.degrees(B_r),math.degrees(C_r)
            # Case: 2 sides + angle opposite (SSA)
            elif a is not None and b is not None and A_r is not None:
                sin_B=b*math.sin(A_r)/a
                if abs(sin_B)>1: messagebox.showerror("Erreur","Triangle impossible (SSA)"); return
                B_r=math.asin(sin_B); C_r=math.pi-A_r-B_r; c=a*math.sin(C_r)/math.sin(A_r)
                A,B,C=math.degrees(A_r),math.degrees(B_r),math.degrees(C_r)
            else:
                messagebox.showwarning("Attention","Donnez au moins 3 valeurs (SSS, SAS, ASA, ou SSA)"); return
            s=(a+b+c)/2; area=math.sqrt(max(0,s*(s-a)*(s-b)*(s-c)))
            P=a+b+c
            R=[f"Côtés: a={a:.4f}, b={b:.4f}, c={c:.4f}",f"Angles: A={A:.2f}°, B={B:.2f}°, C={C:.2f}°",
               f"Périmètre: {P:.4f}",f"Aire (Héron): {area:.4f}",f"Demi-périmètre s: {s:.4f}",
               f"Rayon du cercle inscrit: {area/s:.4f}",f"Rayon du cercle circonscrit: {a*b*c/(4*area):.4f}"]
            self.tri_res.config(text="\n".join(R)); self._save("TRIANGLE",f"a={a},b={b},c={c}")
        except Exception as e: messagebox.showerror("Erreur",f"Résolution impossible: {e}")


    # ═══════════════════════════════════════════════════════════
    #   29. CALCULATRICE DE RENTABILITÉ (ROI)
    # ═══════════════════════════════════════════════════════════
    def _build_roi(self, parent):
        self._title(parent, "Calculatrice de Rentabilité", "📈")
        c = self._card(parent)
        tk.Label(c, text="💰 ROI & Marges", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        for lbl, ph, attr in [("Coût (€):","100","roi_cost"),("Revenu (€):","150","roi_rev")]:
            tk.Label(fr, text=lbl, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
            e=self._entry(fr, ph, width=10); e.pack(side="left", padx=4); setattr(self, attr, e)
        self._btn(fr, "Calculer", self._calc_roi, COULEURS["accent"]).pack(side="left", padx=4)
        self.roi_res = self._result(parent)

        c2 = self._card(parent)
        tk.Label(c2, text="📊 Marge & Majoration", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr2=tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        for lbl, ph, attr in [("Coût unit. (€):","50","mg_cost"),("Prix vente (€):","80","mg_price"),("Qté:","100","mg_qty")]:
            tk.Label(fr2, text=lbl, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
            e=self._entry(fr2, ph, width=8); e.pack(side="left", padx=4); setattr(self, attr, e)
        self._btn(fr2, "Calculer", self._calc_margin, COULEURS["accent"]).pack(side="left", padx=4)
        self.margin_res = self._result(parent)

    def _calc_roi(self):
        try:
            cost=float(self.roi_cost.get()); rev=float(self.roi_rev.get())
            profit=rev-cost; roi=(profit/cost)*100 if cost else 0
            R=[f"💰 Coût: {cost:,.2f} €",f"💰 Revenu: {rev:,.2f} €",f"📈 Profit: {profit:,.2f} €",
               f"📊 ROI: {roi:.2f}%",f"{'✅ Rentable' if profit>0 else '❌ Perte'}"]
            self.roi_res.config(text="\n".join(R)); self._save("ROI",f"ROI={roi:.2f}%")
        except: messagebox.showerror("Erreur","Valeurs invalides")

    def _calc_margin(self):
        try:
            cost=float(self.mg_cost.get()); price=float(self.mg_price.get()); qty=float(self.mg_qty.get())
            profit=price-cost; margin=(profit/price)*100 if price else 0; markup=(profit/cost)*100 if cost else 0
            total_profit=profit*qty; total_rev=price*qty; total_cost=cost*qty
            R=[f"Unitaire — Coût: {cost}€, Vente: {price}€, Profit: {profit}€",
               f"📊 Marge: {margin:.1f}% (profit/prix)",f"📊 Majoration: {markup:.1f}% (profit/coût)",
               f"\nPour {int(qty)} unités:",f"💰 Revenu total: {total_rev:,.2f} €",
               f"📉 Coût total: {total_cost:,.2f} €",f"📈 Profit total: {total_profit:,.2f} €"]
            self.margin_res.config(text="\n".join(R)); self._save("MARGE",f"marge={margin:.1f}%")
        except: messagebox.showerror("Erreur","Valeurs invalides")


    # ═══════════════════════════════════════════════════════════
    #   30. CONVERTISSEUR TIMESTAMP
    # ═══════════════════════════════════════════════════════════
    def _build_timestamp(self, parent):
        self._title(parent, "Convertisseur Timestamp", "⏰")
        c1 = self._card(parent)
        tk.Label(c1, text="🔄 Timestamp → Date/Heure", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c1, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        self.ts_entry = self._entry(fr, str(int(time.time()))); self.ts_entry.pack(side="left", fill="x", expand=True, padx=(0,4))
        self._btn(fr, "Convertir", self._ts_to_date, COULEURS["accent"]).pack(side="left")
        self._btn(fr, "Maintenant", lambda:(self.ts_entry.delete(0,tk.END),self.ts_entry.insert(0,str(int(time.time())))), COULEURS["btn"]).pack(side="left", padx=4)
        self.ts_res = self._result(parent)

        c2 = self._card(parent)
        tk.Label(c2, text="🔄 Date/Heure → Timestamp", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr2=tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        self.dt_entry = self._entry(fr2, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.dt_entry.pack(side="left", fill="x", expand=True, padx=(0,4))
        self._btn(fr2, "Convertir", self._date_to_ts, COULEURS["accent"]).pack(side="left")

        c3 = self._card(parent)
        tk.Label(c3, text="⏱️ Temps écoulé depuis...", bg=COULEURS["card"], fg=COULEURS["btn"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        for lbl, epoch in [("⭐ Unix (1er jan 1970)",0),("📅 1er jan 2000",946684800),("📅 1er jan 2025",1735689600)]:
            d=datetime.fromtimestamp(epoch); elapsed=time.time()-epoch
            tk.Label(c3, text=f"{lbl}: {elapsed:,.0f}s = {elapsed/86400:,.1f}j = {elapsed/(86400*365.25):,.2f} ans",
                     bg=COULEURS["card"], fg=COULEURS["subtext"], font=("Consolas",8)).pack(anchor="w")

    def _ts_to_date(self):
        try:
            ts=int(self.ts_entry.get())
            d=datetime.fromtimestamp(ts)
            self.ts_res.config(text=f"Timestamp: {ts}\nDate: {d.strftime('%d/%m/%Y %H:%M:%S')}\nISO: {d.isoformat()}\nUTC: {datetime.utcfromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')} UTC")
            self._save("TIMESTAMP",f"{ts}→{d.strftime('%d/%m/%Y')}")
        except: messagebox.showerror("Erreur","Timestamp invalide")

    def _date_to_ts(self):
        try:
            d=datetime.strptime(self.dt_entry.get(),"%d/%m/%Y %H:%M:%S")
            ts=int(d.timestamp())
            self.ts_res.config(text=f"Date: {d.strftime('%d/%m/%Y %H:%M:%S')}\nTimestamp: {ts}\n\nActuel: {int(time.time())}")
        except: messagebox.showerror("Erreur","Format: JJ/MM/AAAA HH:MM:SS")


    # ═══════════════════════════════════════════════════════════
    #   31. MOYENNE PONDÉRÉE
    # ═══════════════════════════════════════════════════════════
    def _build_weighted(self, parent):
        self._title(parent, "Moyenne Pondérée", "⚖️")
        c = self._card(parent)
        tk.Label(c, text="Valeur,Poids (une paire par ligne)", bg=COULEURS["card"],
                 fg=COULEURS["subtext"], font=("Segoe UI",9)).pack(anchor="w", pady=(0,4))
        tk.Label(c, text="Ex: 15,2  (valeur=15, poids=2)", bg=COULEURS["card"],
                 fg=COULEURS["subtext"], font=("Segoe UI",8,"italic")).pack(anchor="w")
        self.wp_text = tk.Text(c, height=6, font=("Consolas",10), bg=COULEURS["input_bg"],
                               fg=COULEURS["text"], insertbackground=COULEURS["accent"],
                               relief="flat", padx=8, pady=6)
        self.wp_text.pack(fill="x", pady=4)
        self.wp_text.insert("1.0","15,2\n20,3\n10,1\n25,4")
        self._btn(c, "Calculer", self._calc_weighted, COULEURS["accent"]).pack(pady=6)
        self.wp_res = self._result(parent)

    def _calc_weighted(self):
        try:
            pairs=[]
            for line in self.wp_text.get("1.0","end-1c").strip().split("\n"):
                if not line.strip(): continue
                parts=line.split(",")
                if len(parts)!=2: raise ValueError(f"Ligne invalide: {line}")
                v,w=float(parts[0]),float(parts[1])
                pairs.append((v,w))
            if not pairs: raise ValueError("Aucune donnée")
            total_w=sum(w for _,w in pairs)
            weighted=sum(v*w for v,w in pairs)/total_w if total_w else 0
            simple=sum(v for v,_ in pairs)/len(pairs)
            min_v=min(v for v,_ in pairs); max_v=max(v for v,_ in pairs)
            R=[f"Paires: {len(pairs)}",f"Poids total: {total_w}",f"Moyenne pondérée: {weighted:.4f}",
               f"Moyenne simple: {simple:.4f}",f"Différence: {abs(weighted-simple):.4f}",
               f"Min: {min_v} | Max: {max_v} | Étendue: {max_v-min_v}"]
            self.wp_res.config(text="\n".join(R)); self._save("MOY.POND",f"={weighted:.2f}")
        except Exception as e: messagebox.showerror("Erreur",f"Données invalides: {e}")


    # ═══════════════════════════════════════════════════════════
    #   32. FRÉQUENCE DE CARACTÈRES
    # ═══════════════════════════════════════════════════════════
    def _build_charfreq(self, parent):
        self._title(parent, "Fréquence de Caractères", "🔣")
        c = self._card(parent)
        tk.Label(c, text="Texte à analyser :", bg=COULEURS["card"],
                 fg=COULEURS["subtext"], font=("Segoe UI",9)).pack(anchor="w")
        self.cf_text = tk.Text(c, height=4, font=("Segoe UI",10), bg=COULEURS["input_bg"],
                               fg=COULEURS["text"], insertbackground=COULEURS["accent"],
                               relief="flat", padx=8, pady=6)
        self.cf_text.pack(fill="x", pady=4)
        self._btn_row(c, [("Analyser",self._calc_charfreq,COULEURS["accent"]),
                          ("Exemple",lambda:(self.cf_text.delete("1.0",tk.END),self.cf_text.insert("1.0","Bonjour le monde !")),COULEURS["btn"])])
        self.cf_res = self._result(parent)

    def _calc_charfreq(self):
        t=self.cf_text.get("1.0","end-1c")
        if not t: messagebox.showinfo("Info","Entrez du texte"); return
        total=len(t); freq=Counter(t)
        # Sort by frequency desc
        sorted_freq=sorted(freq.items(), key=lambda x: -x[1])
        R=[f"Total: {total} caractères, {len(sorted_freq)} uniques\n"]
        R.append(f"{'Car.':>6} {'Code':>6} {'Nb':>5} {'%':>7}  Barre")
        R.append("─"*50)
        for char, count in sorted_freq[:20]:
            pct=count/total*100
            bar="█"*int(pct*2)
            display=repr(char)[1:-1] if char!=" " else "⎵"
            R.append(f"{display:>6} {ord(char):>6} {count:>5} {pct:>6.1f}%  {bar}")
        if len(sorted_freq)>20:
            R.append(f"\n... et {len(sorted_freq)-20} autres caractères")
        self.cf_res.config(text="\n".join(R)); self._save("FREQ",f"{len(sorted_freq)} chars uniques")


    # ═══════════════════════════════════════════════════════════
    #   33. CALCULATRICE DE REMISE
    # ═══════════════════════════════════════════════════════════
    def _build_discount(self, parent):
        self._title(parent, "Calculatrice de Remise", "🏷️")
        c = self._card(parent)
        tk.Label(c, text="💰 Prix original → Prix remisé", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        for lbl, ph, attr in [("Prix (€):","100","disc_price"),("Remise (%):","20","disc_pct")]:
            tk.Label(fr, text=lbl, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
            e=self._entry(fr, ph, width=8); e.pack(side="left", padx=4); setattr(self, attr, e)
        self._btn(fr, "Calculer", self._calc_disc, COULEURS["accent"]).pack(side="left", padx=4)
        self.disc_res = self._result(parent)

        # Quick discount buttons
        c2 = self._card(parent)
        tk.Label(c2, text="⚡ Remises rapides", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr2=tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x")
        for pct in [10,15,20,25,30,40,50,70]:
            self._btn(fr2, f"-{pct}%", lambda p=pct:(self.disc_pct.delete(0,tk.END),self.disc_pct.insert(0,str(p)),self._calc_disc()),
                      COULEURS["btn"]).pack(side="left", padx=2, pady=4)

    def _calc_disc(self):
        try:
            price=float(self.disc_price.get()); pct=float(self.disc_pct.get())
            remise=price*pct/100; final=price-remise
            R=[f"🏷️ Prix original: {price:,.2f} €",f"📉 Remise: {pct}% = -{remise:,.2f} €",
               f"💰 Prix final: {final:,.2f} €",f"📊 Vous économisez: {remise:,.2f} €"]
            if pct>=70: R.append("🔥 Super affaire !")
            elif pct>=40: R.append("👍 Bonne remise")
            self.disc_res.config(text="\n".join(R)); self._save("REMISE",f"{price}€ -{pct}% = {final:.2f}€")
        except: messagebox.showerror("Erreur","Valeurs invalides")


    # ═══════════════════════════════════════════════════════════
    #   34. PENTE D'UNE DROITE
    # ═══════════════════════════════════════════════════════════
    def _build_slope(self, parent):
        self._title(parent, "Pente d'une Droite", "📈")
        c = self._card(parent)
        tk.Label(c, text="y = mx + b  (deux 2 points ou pente+ordonnée)", bg=COULEURS["card"],
                 fg=COULEURS["subtext"], font=("Segoe UI",9,"italic")).pack(anchor="w", pady=(0,6))
        self.slope_entries={}
        for lbl, ph, k in [("x₁","0","sl_x1"),("y₁","0","sl_y1"),("x₂","3","sl_x2"),("y₂","6","sl_y2")]:
            fr=tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=2)
            tk.Label(fr, text=lbl+":", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",10,"bold")).pack(side="left")
            e=self._entry(fr, ph, width=10); e.pack(side="left", padx=4); self.slope_entries[k]=e
        self._btn(c, "Calculer", self._calc_slope, COULEURS["accent"]).pack(pady=6)
        self.slope_res = self._result(parent)

    def _calc_slope(self):
        try:
            x1=float(self.slope_entries["sl_x1"].get()); y1=float(self.slope_entries["sl_y1"].get())
            x2=float(self.slope_entries["sl_x2"].get()); y2=float(self.slope_entries["sl_y2"].get())
            if x2==x1: self.slope_res.config(text="❌ Pente infinie (droite verticale)"); return
            m=(y2-y1)/(x2-x1); b=y1-m*x1; dist=math.hypot(x2-x1,y2-y1)
            angle=math.degrees(math.atan(m))
            # Midpoint
            mx,my=(x1+x2)/2,(y1+y2)/2
            # Point-slope form
            R=[f"📐 Pente (m): {m:.4f}",f"📐 Ordonnée à l'origine (b): {b:.4f}",
               f"📐 Équation: y = {m:.2f}x + {b:.2f}",
               f"📐 Point-pente: y - {y1} = {m:.2f}(x - {x1})",
               f"📐 Angle: {angle:.2f}°",f"📐 Milieu: ({mx:.2f}, {my:.2f})",
               f"📐 Distance: {dist:.4f}"]
            if m>0: R.append("📈 Croissante ↗")
            elif m<0: R.append("📉 Décroissante ↘")
            else: R.append("➡️ Horizontale")
            self.slope_res.config(text="\n".join(R)); self._save("PENTE",f"y={m:.2f}x+{b:.2f}")
        except: messagebox.showerror("Erreur","Valeurs invalides")


    # ═══════════════════════════════════════════════════════════
    #   35. JOURS OUVRABLES
    # ═══════════════════════════════════════════════════════════
    def _build_bizdays(self, parent):
        self._title(parent, "Jours Ouvrables", "🗓️")
        c = self._card(parent)
        tk.Label(c, text="⏱️ Jours ouvrables entre deux dates", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        now=datetime.now()
        tk.Label(fr, text="De:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.bd_from = self._entry(fr, now.strftime("%d/%m/%Y"), width=12); self.bd_from.pack(side="left", padx=4)
        tk.Label(fr, text="À:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.bd_to = self._entry(fr, width=12); self.bd_to.pack(side="left", padx=4)
        self._btn(c, "Calculer", self._calc_bizdays, COULEURS["accent"]).pack(pady=6)
        self.bd_res = self._result(parent)

        c2 = self._card(parent)
        tk.Label(c2, text="➕ Ajouter N jours ouvrables", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr2=tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        tk.Label(fr2, text="Jours:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.bd_add = self._entry(fr2, "10", width=6); self.bd_add.pack(side="left", padx=4)
        self._btn(fr2, "Ajouter", self._add_bizdays, COULEURS["accent"]).pack(side="left", padx=4)
        self.bd_add_res = self._result(parent)

    def _calc_bizdays(self):
        try:
            fmt="%d/%m/%Y"; d1=datetime.strptime(self.bd_from.get(),fmt); d2=datetime.strptime(self.bd_to.get(),fmt)
            if d1>d2: d1,d2=d2,d1
            total=0; weekends=0; biz=0
            current=d1
            while current<=d2:
                total+=1
                if current.weekday()>=5: weekends+=1
                else: biz+=1
                current+=timedelta(days=1)
            weeks=total//7; remain=total%7
            R=[f"Total jours: {total} ({weeks} sem. + {remain} j.)",f"Lundi-Vendredi: {biz} jours",
               f"Weekends (Sam-Dim): {weekends} jours",f"Heures ouvrées (35h/sem): ~{biz*7:.0f}h"]
            self.bd_res.config(text="\n".join(R)); self._save("JOURS.OUV",f"{biz} jours ouvrables")
        except Exception as e: messagebox.showerror("Erreur",f"Format JJ/MM/AAAA: {e}")

    def _add_bizdays(self):
        try:
            n=int(self.bd_add.get()); current=datetime.strptime(self.bd_from.get(),"%d/%m/%Y"); added=0
            while added<abs(n):
                current+=timedelta(days=1 if n>0 else -1)
                if current.weekday()<5: added+=1
            self.bd_add_res.config(text=f"{n} jours ouvrables → {current.strftime('%d/%m/%Y')} ({current.strftime('%A')})")
            self._save("JOURS.OUV",f"+{n} = {current.strftime('%d/%m/%Y')}")
        except Exception as e: messagebox.showerror("Erreur",str(e))


    # ═══════════════════════════════════════════════════════════
    #   36. BINAIRE ↔ TEXTE
    # ═══════════════════════════════════════════════════════════
    def _build_bintext(self, parent):
        self._title(parent, "Binaire ↔ Texte", "💾")
        c = self._card(parent)
        tk.Label(c, text="Texte :", bg=COULEURS["card"], fg=COULEURS["subtext"], font=("Segoe UI",9)).pack(anchor="w")
        self.bt_text = tk.Text(c, height=3, font=("Consolas",10), bg=COULEURS["input_bg"],
                               fg=COULEURS["text"], insertbackground=COULEURS["accent"], relief="flat", padx=8, pady=6)
        self.bt_text.pack(fill="x", pady=4)
        self._btn_row(c, [("→ Binaire",self._text_to_bin,COULEURS["accent"]),
                          ("→ Hexa",self._text_to_hex,COULEURS["accent"]),
                          ("→ Octal",self._text_to_oct,COULEURS["btn"]),
                          ("→ Décimal",self._text_to_dec,COULEURS["result_fg"])])
        self._btn_row(c, [("Binaire → Texte",self._bin_to_text,COULEURS["btn"]),
                          ("Effacer",lambda:self.bt_text.delete("1.0",tk.END),COULEURS["btn"])])
        self.bt_res = self._result(parent)

    def _text_to_bin(self):
        t=self.bt_text.get("1.0","end-1c")
        r=" ".join(f"{ord(c):08b}" for c in t)
        self.bt_res.config(text=f"Binaire:\n{r[:300]}{'...' if len(r)>300 else ''}")
    def _text_to_hex(self):
        t=self.bt_text.get("1.0","end-1c")
        r=" ".join(f"{ord(c):02X}" for c in t)
        self.bt_res.config(text=f"Hexadécimal:\n{r[:300]}")
    def _text_to_oct(self):
        t=self.bt_text.get("1.0","end-1c")
        r=" ".join(f"{ord(c):03o}" for c in t)
        self.bt_res.config(text=f"Octal:\n{r[:300]}")
    def _text_to_dec(self):
        t=self.bt_text.get("1.0","end-1c")
        r=" ".join(str(ord(c)) for c in t)
        self.bt_res.config(text=f"Décimal (ASCII):\n{r[:300]}")
    def _bin_to_text(self):
        try:
            t=self.bt_text.get("1.0","end-1c").strip()
            # Try space-separated bytes
            if " " in t:
                r="".join(chr(int(b,2)) for b in t.split())
            else:
                r="".join(chr(int(t[i:i+8],2)) for i in range(0,len(t),8))
            self.bt_res.config(text=f"Texte:\n{r}")
        except: messagebox.showerror("Erreur","Binaire invalide (séparez par espaces ou utilisez 8 bits)")


    # ═══════════════════════════════════════════════════════════
    #   37. CALCULATEUR DE VITESSE
    # ═══════════════════════════════════════════════════════════
    def _build_speed(self, parent):
        self._title(parent, "Calculateur de Vitesse", "🏎️")
        c = self._card(parent)
        tk.Label(c, text="⚡ Distance + Temps = Vitesse (ou déduire une valeur)", bg=COULEURS["card"],
                 fg=COULEURS["subtext"], font=("Segoe UI",8,"italic")).pack(anchor="w", pady=(0,6))
        self.spd_entries={}
        for lbl, ph, k in [("Distance (km):","100","spd_dist"),("Temps (heures):","1.5","spd_time"),("Vitesse (km/h):","","spd_speed")]:
            self._label(c, lbl)
            e=self._entry(c, ph); e.pack(fill="x", pady=2); self.spd_entries[k]=e
        self._btn_row(c, [("Calculer",self._calc_speed,COULEURS["accent"]),
                          ("Pace min/km",self._calc_pace,COULEURS["accent"])])
        self.spd_res = self._result(parent)

        c2 = self._card(parent)
        tk.Label(c2, text="🔄 Convertisseur de vitesses", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c2, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        tk.Label(fr, text="Vitesse:", bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
        self.spd_conv = self._entry(fr, "100", width=10); self.spd_conv.pack(side="left", padx=4)
        self._btn_row(c2, [("km/h",lambda:self._speed_conv("kmh"),COULEURS["btn"]),
                          ("mph",lambda:self._speed_conv("mph"),COULEURS["btn"]),
                          ("m/s",lambda:self._speed_conv("ms"),COULEURS["btn"]),
                          ("nœuds",lambda:self._speed_conv("kn"),COULEURS["btn"]),
                          ("Mach",lambda:self._speed_conv("mach"),COULEURS["btn"])])
        self.spd_conv_res = self._result(parent)

    def _calc_speed(self):
        try:
            g=lambda k: float(self.spd_entries[k].get()) if self.spd_entries[k].get() else None
            d,t,s=g("spd_dist"),g("spd_time"),g("spd_speed")
            R=[]
            if d and t: s=d/t; R.append(f"Vitesse: {s:.2f} km/h")
            if d and s: t=d/s; R.append(f"Temps: {t:.2f} h = {t*60:.0f} min = {int(t)}h{int((t%1)*60)}min")
            if t and s: d=t*s; R.append(f"Distance: {d:.2f} km")
            if not R: messagebox.showwarning("Attention","Laissez UN champ vide"); return
            self.spd_res.config(text="\n".join(R)); self._save("VITESSE",R[0])
        except: messagebox.showerror("Erreur","Valeurs invalides")

    def _calc_pace(self):
        try:
            d=float(self.spd_entries["spd_dist"].get()); t=float(self.spd_entries["spd_time"].get())
            pace_min=t*60/d; mins=int(pace_min); secs=int((pace_min-mins)*60)
            speed=d/t
            self.spd_res.config(text=f"⏱️ Pace: {mins}:{secs:02d} min/km\n🏎️ Vitesse: {speed:.2f} km/h\n🏃 5km: {pace_min*5:.0f} min\n🏃 10km: {pace_min*10:.0f} min\n🏃 Semi: {pace_min*21.1:.0f} min\n🏃 Marathon: {pace_min*42.2:.0f} min")
        except: messagebox.showerror("Erreur","Distance et temps requis")

    def _speed_conv(self, to):
        try:
            v=float(self.spd_conv.get())
            if to=="kmh": R=[f"km/h: {v:.2f}",f"mph: {v/1.609:.2f}",f"m/s: {v/3.6:.2f}",f"nœuds: {v/1.852:.2f}",f"Mach: {v/1235:.4f}"]
            elif to=="mph": v2=v*1.609; R=[f"mph: {v:.2f}",f"km/h: {v2:.2f}",f"m/s: {v2/3.6:.2f}",f"nœuds: {v2/1.852:.2f}"]
            elif to=="ms": v2=v*3.6; R=[f"m/s: {v:.2f}",f"km/h: {v2:.2f}",f"mph: {v2/1.609:.2f}",f"nœuds: {v2/1.852:.2f}"]
            elif to=="kn": v2=v*1.852; R=[f"nœuds: {v:.2f}",f"km/h: {v2:.2f}",f"mph: {v2/1.609:.2f}"]
            elif to=="mach": v2=v*1235; R=[f"Mach: {v:.4f}",f"km/h: {v2:.2f}",f"m/s: {v2/3.6:.2f}"]
            self.spd_conv_res.config(text="\n".join(R))
        except: messagebox.showerror("Erreur","Valeur invalide")


    # ═══════════════════════════════════════════════════════════
    #   38. CALCULATEUR DE CARBURANT
    # ═══════════════════════════════════════════════════════════
    def _build_fuel(self, parent):
        self._title(parent, "Calculateur de Carburant", "⛽")
        c = self._card(parent)
        tk.Label(c, text="💰 Coût du trajet", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr=tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        for lbl, ph, attr in [("Distance (km):","500","fuel_dist"),("Conso (L/100km):","7","fuel_conso"),("Prix (€/L):","1.85","fuel_price")]:
            tk.Label(fr, text=lbl, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
            e=self._entry(fr, ph, width=8); e.pack(side="left", padx=4); setattr(self, attr, e)
        self._btn(fr, "Calculer", self._calc_fuel, COULEURS["accent"]).pack(side="left", padx=4)
        self.fuel_res = self._result(parent)

        c2 = self._card(parent)
        tk.Label(c2, text="📊 Consommation réelle", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI",10,"bold")).pack(anchor="w", pady=(0,4))
        fr2=tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        for lbl, ph, attr in [("Km parcourus:","600","fuel_km"),("Litres pleins:","42","fuel_litres")]:
            tk.Label(fr2, text=lbl, bg=COULEURS["card"], fg=COULEURS["text"], font=("Segoe UI",9)).pack(side="left")
            e=self._entry(fr2, ph, width=10); e.pack(side="left", padx=4); setattr(self, attr, e)
        self._btn(fr2, "Conso", self._calc_real_conso, COULEURS["accent"]).pack(side="left", padx=4)
        self.fuel_conso_res = self._result(parent)

    def _calc_fuel(self):
        try:
            d=float(self.fuel_dist.get()); c=float(self.fuel_conso.get()); p=float(self.fuel_price.get())
            litres=d*c/100; cost=litres*p; cost_per_km=cost/d; km_per_l=100/c if c else 0
            R=[f"⛽ Distance: {d:,.0f} km",f"📊 Consommation: {c} L/100km",
               f"⛽ Volume: {litres:,.1f} L",f"💰 Coût: {cost:,.2f} €",
               f"📊 Coût/km: {cost_per_km:,.3f} €",f"🛣️ Km/L: {km_per_l:,.1f}"]
            self.fuel_res.config(text="\n".join(R)); self._save("CARBURANT",f"coût={cost:.2f}€")
        except: messagebox.showerror("Erreur","Valeurs invalides")

    def _calc_real_conso(self):
        try:
            km=float(self.fuel_km.get()); l=float(self.fuel_litres.get())
            conso=l/km*100; cost_per_km=km/l if l else 0
            R=[f"📊 Consommation: {conso:.2f} L/100km",f"🛣️ Kilométrage par litre: {km/l:.1f} km/L",
               f"📊 Pour 100km: {conso:.1f} L",f"📊 Pour 500km: {conso*5:.1f} L",
               f"📊 Pour 1000km: {conso*10:.1f} L"]
            self.fuel_conso_res.config(text="\n".join(R)); self._save("CONSO",f"{conso:.2f} L/100km")
        except: messagebox.showerror("Erreur","Valeurs invalides")


    # ═══════════════════════════════════════════════════════════
    #   39. FORMATEUR JSON
    # ═══════════════════════════════════════════════════════════
    def _build_json(self, parent):
        self._title(parent, "Formateur JSON", "📋")
        c = self._card(parent)
        self._label(c, "Collez votre JSON ici :")
        self.json_text = tk.Text(c, height=8, font=("Consolas", 10), bg=COULEURS["input_bg"],
                                fg=COULEURS["text"], insertbackground=COULEURS["accent"],
                                relief="flat", padx=8, pady=6)
        self.json_text.pack(fill="x", pady=4)
        self.json_text.insert("1.0", '{"nom":"Rodrigue","age":25,"outils":48}')
        self._btn_row(c, [("Formater", self._json_format, COULEURS["accent"]),
                          ("Minifier", self._json_minify, COULEURS["btn"]),
                          ("Valider", self._json_validate, COULEURS["btn"])])
        self.json_res = self._result(parent)

    def _json_format(self):
        try:
            data = json.loads(self.json_text.get("1.0", "end-1c"))
            pretty = json.dumps(data, indent=2, ensure_ascii=False)
            self.json_text.delete("1.0", tk.END)
            self.json_text.insert("1.0", pretty)
            keys = len(data) if isinstance(data, dict) else len(data)
            self.json_res.config(text=f"JSON formaté avec succès ({keys} éléments racine)")
            self._save("JSON", f"Formaté ({keys} clés)")
        except json.JSONDecodeError as e:
            self.json_res.config(text=f"Erreur JSON: ligne {e.lineno}, colonne {e.colno}\n{e.msg}")

    def _json_minify(self):
        try:
            data = json.loads(self.json_text.get("1.0", "end-1c"))
            mini = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            self.json_text.delete("1.0", tk.END)
            self.json_text.insert("1.0", mini)
            orig = len(self.json_text.get("1.0", "end-1c"))
            self.json_res.config(text=f"JSON minifié ({orig} caractères)")
        except json.JSONDecodeError as e:
            self.json_res.config(text=f"Erreur JSON: {e.msg}")

    def _json_validate(self):
        t = self.json_text.get("1.0", "end-1c")
        try:
            data = json.loads(t)
            tp = type(data).__name__
            if isinstance(data, dict):
                info = f"Objet avec {len(data)} clés"
                depth = self._json_depth(data)
                info += f"\nProfondeur: {depth} niveaux"
                if len(data) <= 20:
                    info += f"\nClés: {', '.join(data.keys())}"
            elif isinstance(data, list):
                info = f"Tableau avec {len(data)} éléments"
                if len(data) > 0 and isinstance(data[0], dict):
                    info += f"\nPremier élément a {len(data[0])} clés"
            else:
                info = f"Valeur simple: {tp}"
            self.json_res.config(text=f"JSON valide — {info}")
        except json.JSONDecodeError as e:
            self.json_res.config(text=f"JSON invalide: ligne {e.lineno}\n{e.msg}")

    def _json_depth(self, obj):
        if isinstance(obj, dict) and obj:
            return 1 + max(self._json_depth(v) for v in obj.values())
        elif isinstance(obj, list) and obj:
            return 1 + max(self._json_depth(v) for v in obj)
        return 0


    # ═══════════════════════════════════════════════════════════
    #   40. TESTEUR REGEX
    # ═══════════════════════════════════════════════════════════
    def _build_regex(self, parent):
        self._title(parent, "Testeur Regex", "🔍")
        c1 = self._card(parent)
        self._label(c1, "Pattern :")
        self.regex_pat = self._entry(c1, r"\d+")
        self.regex_pat.pack(fill="x", pady=4)
        self.regex_flags = {}
        for flag_name, flag_val in [("IGNORECASE", re.IGNORECASE), ("MULTILINE", re.MULTILINE), ("DOTALL", re.DOTALL)]:
            var = tk.BooleanVar(value=(flag_name == "IGNORECASE"))
            self.regex_flags[flag_val] = var
            tk.Checkbutton(c1, text=flag_name, variable=var, bg=COULEURS["card"],
                           fg=COULEURS["text"], selectcolor=COULEURS["surface"],
                           font=("Segoe UI", 9)).pack(side="left", padx=6)
        self._label(c1, "Texte à tester :")
        self.regex_text = tk.Text(c1, height=4, font=("Consolas", 10), bg=COULEURS["input_bg"],
                                 fg=COULEURS["text"], insertbackground=COULEURS["accent"],
                                 relief="flat", padx=8, pady=6)
        self.regex_text.pack(fill="x", pady=4)
        self.regex_text.insert("1.0", "Appeler le 06 12 34 56 78 avant le 15/03/2025\nOu envoyer un email à test@example.com")
        self._btn(c1, "Tester", self._regex_test, COULEURS["accent"]).pack(pady=6)
        self.regex_res = self._result(parent)

    def _regex_test(self):
        try:
            pattern = self.regex_pat.get()
            flags = 0
            for f, var in self.regex_flags.items():
                if var.get():
                    flags |= f
            compiled = re.compile(pattern, flags)
            text = self.regex_text.get("1.0", "end-1c")
            matches = list(compiled.finditer(text))
            if not matches:
                self.regex_res.config(text=f"Aucune correspondance trouvée pour: {pattern}")
                return
            R = [f"Pattern: {pattern} — {len(matches)} correspondance(s)"]
            for i, m in enumerate(matches[:15]):
                start = text[:m.start()].count("\n") + 1
                R.append(f"  [{i+1}] pos {m.start()}-{m.end()} (ligne {start}): \"{m.group()}\"")
            if len(matches) > 15:
                R.append(f"  ... et {len(matches)-15} autres")
            self.regex_res.config(text="\n".join(R))
            self._save("REGEX", f"{len(matches)} matches pour '{pattern}'")
        except re.error as e:
            self.regex_res.config(text=f"Erreur de pattern: {e}")


    # ═══════════════════════════════════════════════════════════
    #   41. NOMBRES EN LETTRES (Français)
    # ═══════════════════════════════════════════════════════════
    def _build_nbletters(self, parent):
        self._title(parent, "Nombres en Lettres", "🔤")
        c = self._card(parent)
        self._label(c, "Nombre :")
        self.nl_entry = self._entry(c, "1789")
        self.nl_entry.pack(fill="x", pady=4)
        self._btn_row(c, [("Convertir", self._nb_to_letters, COULEURS["accent"]),
                          ("Effacer", lambda: (self.nl_entry.delete(0, tk.END), self.nl_res.config(text="—")), COULEURS["btn"])])
        c2 = self._card(parent)
        tk.Label(c2, text="Exemples rapides", bg=COULEURS["card"], fg=COULEURS["accent"],
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        fr = tk.Frame(c2, bg=COULEURS["card"]); fr.pack(fill="x")
        for n in [0, 1, 42, 100, 1000, 1789, 1000000, 1234567890]:
            self._btn(fr, str(n), lambda v=n: (self.nl_entry.delete(0, tk.END),
                       self.nl_entry.insert(0, str(v)), self._nb_to_letters()),
                       COULEURS["btn"]).pack(side="left", padx=2, pady=2)
        self.nl_res = self._result(parent)

    def _nb_to_letters(self):
        try:
            n = int(self.nl_entry.get())
            if n < 0 or n > 999999999999:
                messagebox.showwarning("Attention", "Plage: 0 — 999 999 999 999")
                return
            result = self._number_to_french(n)
            self.nl_res.config(text=f"{n:,} = {result}")
            self._save("NB.LETTRES", f"{n} = {result[:40]}...")
        except ValueError:
            messagebox.showerror("Erreur", "Entier requis")

    def _number_to_french(self, n):
        if n == 0: return "zéro"
        units = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf",
                 "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"]
        tens = ["", "", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante", "quatre-vingt", "quatre-vingt"]
        def chunk(n):
            if n == 0: return ""
            if n < 20: return units[n]
            t = n // 10
            u = n % 10
            if t == 7 or t == 9:
                rest = chunk((t - 6 if t == 7 else t - 8) * 10 + u)
                base = "soixante" if t == 7 else "quatre-vingt"
                return f"{base}-{rest}" if rest else base
            if u == 0:
                if t == 8: return "quatre-vingts"
                return tens[t]
            if u == 1 and t != 8:
                return f"{tens[t]}-et-un"
            return f"{tens[t]}-{units[u]}"
        if n == 1000: return "mille"
        parts = []
        scales = [(10**12, "billion"), (10**9, "milliard"), (10**6, "million"), (10**3, "mille"), (1, "")]
        for val, name in scales:
            if n >= val:
                count = n // val
                n = n % val
                if val >= 10**6:
                    c = "un" if count == 1 else self._number_to_french(count)
                    parts.append(f"{c} {name}")
                elif val == 1000:
                    if count == 1:
                        parts.append("mille")
                    else:
                        parts.append(f"{self._number_to_french(count)} mille")
                elif val == 100:
                    if count == 1:
                        parts.append("cent")
                    elif count < 100:
                        c = chunk(count)
                        if count % 100 == 0 and count > 1:
                            parts.append(f"{c}s")
                        else:
                            parts.append(c)
                else:
                    parts.append(chunk(count))
        return " ".join(parts).strip()


    # ═══════════════════════════════════════════════════════════
    #   42. CALCULATEUR D'ÂGE
    # ═══════════════════════════════════════════════════════════
    def _build_age(self, parent):
        self._title(parent, "Calculateur d'Âge", "🎂")
        c = self._card(parent)
        now = datetime.now()
        fr = tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        tk.Label(fr, text="Date de naissance:", bg=COULEURS["card"], fg=COULEURS["text"],
                 font=("Segoe UI", 9)).pack(side="left")
        self.age_dob = self._entry(fr, "01/01/2000", width=14)
        self.age_dob.pack(side="left", padx=4)
        tk.Label(fr, text="Date cible:", bg=COULEURS["card"], fg=COULEURS["text"],
                 font=("Segoe UI", 9)).pack(side="left", padx=(12, 0))
        self.age_target = self._entry(fr, now.strftime("%d/%m/%Y"), width=14)
        self.age_target.pack(side="left", padx=4)
        self._btn(c, "Calculer", self._calc_age, COULEURS["accent"]).pack(pady=6)
        self.age_res = self._result(parent)

    def _calc_age(self):
        try:
            fmt = "%d/%m/%Y"
            dob = datetime.strptime(self.age_dob.get(), fmt)
            target = datetime.strptime(self.age_target.get(), fmt)
            if dob > target:
                messagebox.showerror("Erreur", "La date de naissance doit être antérieure")
                return
            days = (target - dob).days
            y = days // 365
            rem = days % 365
            m = rem // 30
            d = rem % 30
            zodiac = self._get_zodiac(dob.month, dob.day)
            day_name = ["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"][dob.weekday()]
            next_bday = datetime(target.year, dob.month, dob.day)
            if next_bday < target:
                next_bday = datetime(target.year + 1, dob.month, dob.day)
            days_to_bday = (next_bday - target).days
            R = [
                f"Âge exact: {y} ans, {m} mois, {d} jours",
                f"Total: {days:,} jours",
                f"Total: {weeks:=,} semaines" if (weeks := days // 7) else f"Total: {days // 7:,} semaines",
                f"Total: {days * 24:,} heures",
                f"Total: {days * 24 * 60:,} minutes",
                f"Jour de naissance: {day_name}",
                f"Signe zodiacal: {zodiac}",
                f"Prochain anniversaire: dans {days_to_bday} jours ({next_bday.strftime('%d/%m/%Y')})",
            ]
            self.age_res.config(text="\n".join(R))
            self._save("ÂGE", f"{y} ans, {m} mois")
        except Exception as e:
            messagebox.showerror("Erreur", f"Format JJ/MM/AAAA: {e}")

    def _get_zodiac(self, month, day):
        zodiacs = [
            (20, "Verseau"), (19, "Poissons"), (20, "Bélier"), (20, "Taureau"),
            (21, "Gémeaux"), (21, "Cancer"), (22, "Lion"), (23, "Vierge"),
            (23, "Balance"), (23, "Scorpion"), (22, "Sagittaire"), (22, "Capricorne")
        ]
        return zodiacs[month - 1][1] if day < zodiacs[month - 1][0] else zodiacs[month % 12][1]


    # ═══════════════════════════════════════════════════════════
    #   43. INTÉRÊTS COMPOSÉS
    # ═══════════════════════════════════════════════════════════
    def _build_compound(self, parent):
        self._title(parent, "Intérêts Composés", "📈")
        c = self._card(parent)
        entries_data = [("Capital initial (€):", "10000", "cp_capital"),
                       ("Taux annuel (%):", "5", "cp_rate"),
                       ("Durée (ans):", "10", "cp_years"),
                       ("Versement mensuel (€):", "100", "cp_monthly")]
        for lbl, ph, attr in entries_data:
            self._label(c, lbl)
            e = self._entry(c, ph)
            e.pack(fill="x", pady=2)
            setattr(self, attr, e)
        self._btn(c, "Calculer", self._calc_compound, COULEURS["accent"]).pack(pady=6)
        self.cp_res = self._result(parent)

    def _calc_compound(self):
        try:
            P = float(self.cp_capital.get())
            r = float(self.cp_rate.get()) / 100
            n = int(self.cp_years.get())
            PMT = float(self.cp_monthly.get())
            rm = r / 12
            # A = P(1+r)^n + PMT * [((1+r/12)^(12*n) - 1) / (r/12)]
            if rm == 0:
                total = P + PMT * 12 * n
                interest = PMT * 12 * n
            else:
                compound = P * (1 + r) ** n
                future_pmt = PMT * (((1 + rm) ** (12 * n) - 1) / rm)
                total = compound + future_pmt
                interest = total - P - PMT * 12 * n
            invested = P + PMT * 12 * n
            growth = ((total - invested) / invested * 100) if invested else 0
            R = [
                f"Capital final: {total:,.2f} €",
                f"Total investi: {invested:,.2f} €",
                f"Intérêts gagnés: {interest:,.2f} €",
                f"Rendement: +{growth:.1f}%",
                f"",
                f"Évolution (5 premières années):",
            ]
            current = P
            for y in range(1, min(n + 1, 6)):
                current = current * (1 + r) + PMT * 12
                R.append(f"  Année {y}: {current:,.2f} €")
            if n > 5:
                R.append(f"  ...")
                R.append(f"  Année {n}: {total:,.2f} €")
            self.cp_res.config(text="\n".join(R))
            self._save("INT.COMPOSÉS", f"Final={total:,.0f}€, intérêts={interest:,.0f}€")
        except Exception as e:
            messagebox.showerror("Erreur", f"Valeurs invalides: {e}")


    # ═══════════════════════════════════════════════════════════
    #   44. CODE MORSE
    # ═══════════════════════════════════════════════════════════
    MORSE_CODE = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--', '/': '-..-.',
        '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.',
        '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
        '@': '.--.-.',
    }
    MORSE_REVERSE = {v: k for k, v in MORSE_CODE.items()}

    def _build_morse(self, parent):
        self._title(parent, "Code Morse", "📡")
        c = self._card(parent)
        self._label(c, "Texte / Code Morse :")
        self.morse_text = tk.Text(c, height=4, font=("Consolas", 11), bg=COULEURS["input_bg"],
                                 fg=COULEURS["text"], insertbackground=COULEURS["accent"],
                                 relief="flat", padx=8, pady=6)
        self.morse_text.pack(fill="x", pady=4)
        self.morse_text.insert("1.0", "SOS")
        self._btn_row(c, [("Texte → Morse", self._to_morse, COULEURS["accent"]),
                          ("Morse → Texte", self._from_morse, COULEURS["btn"]),
                          ("Effacer", lambda: self.morse_text.delete("1.0", tk.END), COULEURS["btn"])])
        self.morse_res = self._result(parent)

    def _to_morse(self):
        t = self.morse_text.get("1.0", "end-1c").upper()
        result = []
        for c in t:
            if c == ' ':
                result.append('/')
            elif c in self.MORSE_CODE:
                result.append(self.MORSE_CODE[c])
            else:
                result.append('?')
        morse = ' '.join(result)
        self.morse_res.config(text=f"Morse: {morse}")
        self._save("MORSE", morse[:50])

    def _from_morse(self):
        t = self.morse_text.get("1.0", "end-1c").strip()
        words = t.split(' / ')
        result = []
        for word in words:
            letters = word.split(' ')
            decoded = []
            for code in letters:
                if code in self.MORSE_REVERSE:
                    decoded.append(self.MORSE_REVERSE[code])
                else:
                    decoded.append('?')
            result.append(''.join(decoded))
        text = ' '.join(result)
        self.morse_res.config(text=f"Texte: {text}")
        self._save("MORSE", text[:50])


    # ═══════════════════════════════════════════════════════════
    #   45. PGCD / PPCM
    # ═══════════════════════════════════════════════════════════
    def _build_gcdlcm(self, parent):
        self._title(parent, "PGCD / PPCM", "🔗")
        c = self._card(parent)
        fr = tk.Frame(c, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        tk.Label(fr, text="A:", bg=COULEURS["card"], fg=COULEURS["text"],
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        self.gcd_a = self._entry(fr, "48", width=12)
        self.gcd_a.pack(side="left", padx=4)
        tk.Label(fr, text="B:", bg=COULEURS["card"], fg=COULEURS["text"],
                 font=("Segoe UI", 11, "bold")).pack(side="left", padx=(12, 0))
        self.gcd_b = self._entry(fr, "18", width=12)
        self.gcd_b.pack(side="left", padx=4)
        self._btn_row(c, [("PGCD", self._calc_gcd, COULEURS["accent"]),
                          ("PPCM", self._calc_lcm, COULEURS["btn"]),
                          ("Les deux", self._calc_both, COULEURS["btn"])])
        self.gcd_res = self._result(parent)

    def _calc_gcd(self):
        try:
            a, b = int(self.gcd_a.get()), int(self.gcd_b.get())
            g = math.gcd(a, b)
            self.gcd_res.config(text=f"PGCD({a}, {b}) = {g}")
            self._save("PGCD", f"PGCD({a},{b})={g}")
        except: messagebox.showerror("Erreur", "Entiers requis")

    def _calc_lcm(self):
        try:
            a, b = int(self.gcd_a.get()), int(self.gcd_b.get())
            g = math.gcd(a, b)
            l = abs(a * b) // g if g else 0
            self.gcd_res.config(text=f"PPCM({a}, {b}) = {l:,}")
            self._save("PPCM", f"PPCM({a},{b})={l}")
        except: messagebox.showerror("Erreur", "Entiers requis")

    def _calc_both(self):
        try:
            a, b = int(self.gcd_a.get()), int(self.gcd_b.get())
            g = math.gcd(a, b)
            l = abs(a * b) // g if g else 0
            fa = self._factorize(a)
            fb = self._factorize(b)
            frac_a = a // g
            frac_b = b // g
            R = [
                f"A = {a}  =  {' × '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in fa)}",
                f"B = {b}  =  {' × '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in fb)}",
                f"",
                f"PGCD({a}, {b}) = {g}",
                f"PPCM({a}, {b}) = {l:,}",
                f"Fraction simplifiée: {frac_a}/{frac_b}",
                f"Produit A×B = {a * b:,}  =  PGCD × PPCM = {g * l:,}",
            ]
            self.gcd_res.config(text="\n".join(R))
            self._save("PGCD/PPCM", f"G={g}, P={l}")
        except: messagebox.showerror("Erreur", "Entiers requis")

    def _factorize(self, n):
        if n == 0: return [(0, 1)]
        factors = []
        d = 2
        while d * d <= abs(n):
            count = 0
            while n % d == 0:
                n //= d
                count += 1
            if count > 0:
                factors.append((d, count))
            d += 1
        if abs(n) > 1:
            factors.append((abs(n), 1))
        return factors


    # ═══════════════════════════════════════════════════════════
    #   46. GÉNÉRATEUR UUID
    # ═══════════════════════════════════════════════════════════
    def _build_uuidgen(self, parent):
        self._title(parent, "Générateur UUID", "🆔")
        c = self._card(parent)
        self._btn_row(c, [("1 UUID", lambda: self._gen_uuids(1), COULEURS["accent"]),
                          ("5 UUIDs", lambda: self._gen_uuids(5), COULEURS["btn"]),
                          ("10 UUIDs", lambda: self._gen_uuids(10), COULEURS["btn"]),
                          ("Copier", self._copy_uuid, COULEURS["btn"])])
        self.uuid_display = tk.Text(c, height=12, font=("Consolas", 11), bg=COULEURS["input_bg"],
                                    fg=COULEURS["result_fg"], insertbackground=COULEURS["accent"],
                                    relief="flat", padx=8, pady=6)
        self.uuid_display.pack(fill="x", pady=4)
        self.uuid_display.config(state="disabled")
        self.uuid_count_lbl = tk.Label(c, text="0 UUID généré(s)", bg=COULEURS["card"],
                                      fg=COULEURS["subtext"], font=("Segoe UI", 9))
        self.uuid_count_lbl.pack(anchor="w")
        self._total_uuids = 0

    def _gen_uuids(self, count):
        uuids = [str(uuid_mod.uuid4()) for _ in range(count)]
        self.uuid_display.config(state="normal")
        self.uuid_display.delete("1.0", tk.END)
        for u in uuids:
            self.uuid_display.insert("end", f"{u}\n")
        self.uuid_display.config(state="disabled")
        self._total_uuids += count
        self.uuid_count_lbl.config(text=f"{self._total_uuids} UUID généré(s) au total")
        self._save("UUID", f"{count} UUID(s)")

    def _copy_uuid(self):
        try:
            content = self.uuid_display.get("1.0", "end-1c").strip()
            if content:
                self.root.clipboard_clear()
                self.root.clipboard_append(content)
                messagebox.showinfo("Copié", f"{content.count(chr(10))+1} UUID(s) copié(s) dans le presse-papier")
        except:
            messagebox.showerror("Erreur", "Impossible de copier")


    # ═══════════════════════════════════════════════════════════
    #   47. CALCULATEUR D'HEURES
    # ═══════════════════════════════════════════════════════════
    def _build_hourcalc(self, parent):
        self._title(parent, "Calculateur d'Heures", "⏰")
        c1 = self._card(parent)
        tk.Label(c1, text="Addition / Soustraction d'heures", bg=COULEURS["card"],
                 fg=COULEURS["accent"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        fr = tk.Frame(c1, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        tk.Label(fr, text="Heure 1 (HH:MM):", bg=COULEURS["card"], fg=COULEURS["text"],
                 font=("Segoe UI", 9)).pack(side="left")
        self.hc_h1 = self._entry(fr, "08:30", width=8)
        self.hc_h1.pack(side="left", padx=4)
        op_var = tk.StringVar(value="+")
        for t in ["+", "-"]:
            tk.Radiobutton(fr, text=t, variable=op_var, value=t, bg=COULEURS["card"],
                           fg=COULEURS["text"], selectcolor=COULEURS["surface"],
                           font=("Segoe UI", 12, "bold")).pack(side="left", padx=4)
        self.hc_op = op_var
        tk.Label(fr, text="Heure 2 (HH:MM):", bg=COULEURS["card"], fg=COULEURS["text"],
                 font=("Segoe UI", 9)).pack(side="left", padx=(4, 0))
        self.hc_h2 = self._entry(fr, "03:45", width=8)
        self.hc_h2.pack(side="left", padx=4)
        self._btn(c1, "Calculer", self._calc_hours, COULEURS["accent"]).pack(pady=6)
        self.hc_res = self._result(parent)

        c2 = self._card(parent)
        tk.Label(c2, text="Ajouter N heures/minutes à une heure", bg=COULEURS["card"],
                 fg=COULEURS["accent"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        fr2 = tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        tk.Label(fr2, text="Départ:", bg=COULEURS["card"], fg=COULEURS["text"],
                 font=("Segoe UI", 9)).pack(side="left")
        self.hc_base = self._entry(fr2, "09:00", width=8)
        self.hc_base.pack(side="left", padx=4)
        tk.Label(fr2, text="+H:", bg=COULEURS["card"], fg=COULEURS["text"],
                 font=("Segoe UI", 9)).pack(side="left")
        self.hc_add_h = self._entry(fr2, "2", width=5)
        self.hc_add_h.pack(side="left", padx=2)
        tk.Label(fr2, text="+M:", bg=COULEURS["card"], fg=COULEURS["text"],
                 font=("Segoe UI", 9)).pack(side="left")
        self.hc_add_m = self._entry(fr2, "30", width=5)
        self.hc_add_m.pack(side="left", padx=2)
        self._btn(fr2, "Ajouter", self._add_to_time, COULEURS["btn"]).pack(side="left", padx=4)
        self.hc_add_res = self._result(parent)

    def _parse_hhmm(self, s):
        parts = s.strip().split(":")
        if len(parts) != 2:
            raise ValueError("Format HH:MM")
        return int(parts[0]), int(parts[1])

    def _calc_hours(self):
        try:
            h1, m1 = self._parse_hhmm(self.hc_h1.get())
            h2, m2 = self._parse_hhmm(self.hc_h2.get())
            total1 = h1 * 60 + m1
            total2 = h2 * 60 + m2
            if self.hc_op.get() == "+":
                total = total1 + total2
            else:
                total = total1 - total2
            rh = total // 60
            rm = total % 60
            days = rh // 24
            rh = rh % 24
            R = [
                f"  {self.hc_h1.get()} {self.hc_op.get()} {self.hc_h2.get()}",
                f"Résultat: {rh:02d}:{rm:02d}",
                f"Total minutes: {abs(total)}",
                f"Heures décimales: {abs(total)/60:.2f}h",
            ]
            if days > 0:
                R.insert(2, f"= {days} jour(s) et {rh:02d}:{rm:02d}")
            self.hc_res.config(text="\n".join(R))
            self._save("HEURES", f"{rh:02d}:{rm:02d}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Format HH:MM invalide: {e}")

    def _add_to_time(self):
        try:
            h, m = self._parse_hhmm(self.hc_base.get())
            add_h = int(self.hc_add_h.get()) if self.hc_add_h.get() else 0
            add_m = int(self.hc_add_m.get()) if self.hc_add_m.get() else 0
            total = h * 60 + m + add_h * 60 + add_m
            rh = (total // 60) % 24
            rm = total % 60
            self.hc_add_res.config(text=f"Départ: {self.hc_base.get()} + {add_h}h{add_m}min = {rh:02d}:{rm:02d}")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))


    # ═══════════════════════════════════════════════════════════
    #   48. CONVERTISSEUR GPS (DMS ↔ Décimal)
    # ═══════════════════════════════════════════════════════════
    def _build_gps(self, parent):
        self._title(parent, "Convertisseur GPS", "📍")
        c1 = self._card(parent)
        tk.Label(c1, text="DMS → Degrés décimaux", bg=COULEURS["card"],
                 fg=COULEURS["accent"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        fr = tk.Frame(c1, bg=COULEURS["card"]); fr.pack(fill="x", pady=4)
        for lbl, ph, attr in [("Degrés:", "48", "gps_d"), ("Minutes:", "51", "gps_m"),
                                ("Secondes:", "36", "gps_s"), ("Dir:", "N", "gps_dir")]:
            tk.Label(fr, text=lbl, bg=COULEURS["card"], fg=COULEURS["text"],
                     font=("Segoe UI", 9)).pack(side="left")
            e = self._entry(fr, ph, width=6)
            e.pack(side="left", padx=2)
            setattr(self, attr, e)
        self._btn(c1, "Convertir → Décimal", self._gps_dms_to_dec, COULEURS["accent"]).pack(pady=6)
        self.gps_res = self._result(parent)

        c2 = self._card(parent)
        tk.Label(c2, text="Degrés décimaux → DMS", bg=COULEURS["card"],
                 fg=COULEURS["accent"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        fr2 = tk.Frame(c2, bg=COULEURS["card"]); fr2.pack(fill="x", pady=4)
        tk.Label(fr2, text="Décimaux:", bg=COULEURS["card"], fg=COULEURS["text"],
                 font=("Segoe UI", 9)).pack(side="left")
        self.gps_dec = self._entry(fr2, "48.8600", width=12)
        self.gps_dec.pack(side="left", padx=4)
        self._btn(fr2, "Convertir → DMS", self._gps_dec_to_dms, COULEURS["btn"]).pack(side="left", padx=4)
        self.gps_dms_res = self._result(parent)

    def _gps_dms_to_dec(self):
        try:
            d = float(self.gps_d.get())
            m = float(self.gps_m.get())
            s = float(self.gps_s.get())
            direction = self.gps_dir.get().upper()
            if direction not in ("N", "S", "E", "W"):
                messagebox.showwarning("Attention", "Direction: N, S, E, ou W")
                return
            decimal = d + m / 60 + s / 3600
            if direction in ("S", "W"):
                decimal = -decimal
            lat_band = self._get_lat_band(abs(decimal))
            R = [
                f"{d}° {m}' {s}\" {direction}",
                f"= {decimal:.6f}°",
                f"Signe: {'+' if decimal >= 0 else '-'}{abs(decimal):.6f}°",
            ]
            if direction in ("N", "S"):
                R.append(f"Bande de latitude: {lat_band}")
            self.gps_res.config(text="\n".join(R))
            self._save("GPS", f"{decimal:.4f}°")
        except Exception as e:
            messagebox.showerror("Erreur", f"Valeurs invalides: {e}")

    def _gps_dec_to_dms(self):
        try:
            dec = float(self.gps_dec.get())
            sign = "N" if dec >= 0 else "S"
            dec = abs(dec)
            d = int(dec)
            m_float = (dec - d) * 60
            m = int(m_float)
            s = (m_float - m) * 60
            R = [
                f"{dec:.6f}°",
                f"= {d}° {m}' {s:.2f}\" {sign}",
                f"DMS exact: {d}° {m}' {s:.4f}\" {sign}",
            ]
            self.gps_dms_res.config(text="\n".join(R))
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def _get_lat_band(self, lat):
        bands = ['N', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M',
                 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']
        if lat < 0 or lat > 84: return "Hors zone UTM"
        return bands[int(lat / 8) + 2]


# ═══════════════════════════════════════════════════════════════
#   POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app = MultiOutilsPro(root)
    root.mainloop()
