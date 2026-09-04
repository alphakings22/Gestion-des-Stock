import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import database as db
from datetime import date

# ═══════════════════════════════════════════════════════════════
#  DESIGN SYSTEM — Palette "Togo Moderne"
# ═══════════════════════════════════════════════════════════════
BG         = "#F5F6FA"
SIDEBAR_BG = "#1C1F2E"
CARD_BG    = "#FFFFFF"

ACCENT     = "#E8500A"   # orange-rouge togolais
ACCENT2    = "#F9A825"   # or/soleil
ACCENT3    = "#1A73E8"   # bleu digital
SUCCESS    = "#00897B"
DANGER     = "#D32F2F"
WARNING    = "#F57C00"

TEXT_DARK  = "#1C1F2E"
TEXT_MID   = "#555B7A"
TEXT_LIGHT = "#9BA3C2"
TEXT_WHITE = "#FFFFFF"
BORDER     = "#E2E5F0"

FONT_LOGO  = ("Segoe UI", 13, "bold")
FONT_NAV   = ("Segoe UI", 10)
FONT_H1    = ("Segoe UI", 20, "bold")
FONT_H2    = ("Segoe UI", 13, "bold")
FONT_BODY  = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_BADGE = ("Segoe UI", 9, "bold")
FONT_BIG   = ("Segoe UI", 24, "bold")

def fmt_fcfa(val):
    try:
        return f"{int(float(val)):,} FCFA".replace(",", " ")
    except:
        return f"{val} FCFA"


# ═══════════════════════════════════════════════════════════════
#  COMPOSANTS UI
# ═══════════════════════════════════════════════════════════════
class ModernButton(tk.Button):
    def __init__(self, parent, text, color=ACCENT, fg=TEXT_WHITE,
                 icon="", **kw):
        self.color = color
        self.hover = self._darken(color)
        full = f"{icon}  {text}" if icon else text
        super().__init__(parent, text=full, bg=color, fg=fg,
                         font=FONT_BODY, relief="flat", bd=0,
                         padx=14, pady=7, cursor="hand2",
                         activebackground=self.hover,
                         activeforeground=fg, **kw)
        self.bind("<Enter>", lambda e: self.config(bg=self.hover))
        self.bind("<Leave>", lambda e: self.config(bg=self.color))

    def _darken(self, h):
        try:
            r = max(0, int(h[1:3],16)-25)
            g = max(0, int(h[3:5],16)-25)
            b = max(0, int(h[5:7],16)-25)
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return h


class StatCard(tk.Frame):
    def __init__(self, parent, icon, title, value, color, **kw):
        super().__init__(parent, bg=CARD_BG, **kw)
        tk.Frame(self, bg=color, width=4).pack(side="left", fill="y")
        body = tk.Frame(self, bg=CARD_BG, padx=14, pady=12)
        body.pack(fill="both", expand=True)
        tk.Label(body, text=icon, font=("Segoe UI",18),
                 bg=CARD_BG, fg=color).pack(anchor="w")
        tk.Label(body, text=title, font=FONT_SMALL,
                 fg=TEXT_LIGHT, bg=CARD_BG).pack(anchor="w", pady=(4,2))
        tk.Label(body, text=str(value), font=FONT_BIG,
                 fg=TEXT_DARK, bg=CARD_BG).pack(anchor="w")


class NavButton(tk.Frame):
    def __init__(self, parent, icon, text, command, **kw):
        super().__init__(parent, bg=SIDEBAR_BG, cursor="hand2", **kw)
        self._cmd = command
        self.active = False

        self.bar = tk.Frame(self, bg=SIDEBAR_BG, width=3)
        self.bar.pack(side="left", fill="y")

        self.inner = tk.Frame(self, bg=SIDEBAR_BG, padx=12, pady=11)
        self.inner.pack(fill="both", expand=True)

        self.ico = tk.Label(self.inner, text=icon, font=("Segoe UI",13),
                            bg=SIDEBAR_BG, fg="#7B82A3")
        self.ico.pack(side="left", padx=(0,10))

        self.lbl = tk.Label(self.inner, text=text, font=FONT_NAV,
                            bg=SIDEBAR_BG, fg="#7B82A3", anchor="w")
        self.lbl.pack(side="left", fill="x", expand=True)

        for w in (self, self.inner, self.ico, self.lbl, self.bar):
            w.bind("<Button-1>", lambda e: command())
            w.bind("<Enter>", self._hover)
            w.bind("<Leave>", self._leave)

    def _all(self): return (self, self.inner, self.ico, self.lbl)

    def _hover(self, e):
        if not self.active:
            [w.config(bg="#252840") for w in self._all()]
            self.bar.config(bg="#252840")

    def _leave(self, e):
        if not self.active:
            [w.config(bg=SIDEBAR_BG) for w in self._all()]
            self.bar.config(bg=SIDEBAR_BG)

    def set_active(self, active):
        self.active = active
        if active:
            [w.config(bg="#252840") for w in self._all()]
            self.bar.config(bg=ACCENT)
            self.ico.config(fg=ACCENT)
            self.lbl.config(fg=TEXT_WHITE, font=("Segoe UI",10,"bold"))
        else:
            [w.config(bg=SIDEBAR_BG) for w in self._all()]
            self.bar.config(bg=SIDEBAR_BG)
            self.ico.config(fg="#7B82A3")
            self.lbl.config(fg="#7B82A3", font=FONT_NAV)


# ═══════════════════════════════════════════════════════════════
#  APPLICATION PRINCIPALE
# ═══════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        db.init_db()
        self.title("APHA_Gestion_Stock")
        self.geometry("1260x740")
        self.minsize(960, 600)
        self.configure(bg=BG)
        self._style()
        self._build()
        self.navigate("dashboard")

    def _style(self):
        s = ttk.Style(); s.theme_use("clam")
        s.configure("Tree.Treeview", background=CARD_BG, foreground=TEXT_DARK,
                    rowheight=34, fieldbackground=CARD_BG, borderwidth=0, font=FONT_BODY)
        s.configure("Tree.Treeview.Heading", background="#F0F3FF", foreground=TEXT_MID,
                    relief="flat", font=FONT_BADGE, padding=(8,6))
        s.map("Tree.Treeview",
              background=[("selected","#EBF0FF")],
              foreground=[("selected", ACCENT3)])
        s.configure("TCombobox", fieldbackground=CARD_BG, background=CARD_BG,
                    foreground=TEXT_DARK, arrowcolor=ACCENT)

    def _build(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo_z = tk.Frame(self.sidebar, bg="#151827", pady=22)
        logo_z.pack(fill="x")
        badge = tk.Frame(logo_z, bg=ACCENT, width=46, height=46)
        badge.pack(); badge.pack_propagate(False)
        tk.Label(badge, text="📦", font=("Segoe UI",20),
                 bg=ACCENT, fg=TEXT_WHITE).place(relx=.5, rely=.5, anchor="center")
        tk.Label(logo_z, text="StockManager", font=FONT_LOGO,
                 bg="#151827", fg=TEXT_WHITE).pack(pady=(10,2))
        tk.Label(logo_z, text="Gestion de Stock — Togo",
                 font=FONT_SMALL, bg="#151827", fg="#5C6280").pack()

        tk.Frame(self.sidebar, bg="#252840", height=1).pack(fill="x", pady=8)
        tk.Label(self.sidebar, text="NAVIGATION", font=("Segoe UI",7,"bold"),
                 bg=SIDEBAR_BG, fg="#3D4466", padx=16).pack(anchor="w", pady=(0,6))

        self.nav = {}
        for icon, label, key in [
            ("🏠","Tableau de bord","dashboard"),
            ("📦","Produits",       "produits"),
            ("🏷️","Catégories",    "categories"),
            ("🚚","Fournisseurs",   "fournisseurs"),
            ("📋","Commandes",      "commandes"),
            ("⚠️","Alertes stock", "alertes"),
        ]:
            btn = NavButton(self.sidebar, icon, label, command=lambda k=key: self.navigate(k))
            btn.pack(fill="x")
            self.nav[key] = btn

        tk.Frame(self.sidebar, bg="#252840", height=1).pack(fill="x", pady=8, side="bottom")
        tk.Label(self.sidebar, text="Jucal Johnson• 2024–2025",
                 font=FONT_SMALL, bg=SIDEBAR_BG, fg="#3D4466",
                 pady=10).pack(side="bottom")

        # Main
        self.main_f = tk.Frame(self, bg=BG)
        self.main_f.pack(side="left", fill="both", expand=True)

        topbar = tk.Frame(self.main_f, bg=CARD_BG, height=62)
        topbar.pack(fill="x"); topbar.pack_propagate(False)
        tk.Frame(topbar, bg=BORDER, height=1).pack(side="bottom", fill="x")

        self.title_lbl = tk.Label(topbar, text="", font=FONT_H1,
                                   fg=TEXT_DARK, bg=CARD_BG, padx=24)
        self.title_lbl.pack(side="left", fill="y")

        date_f = tk.Frame(topbar, bg="#F0F3FF", padx=14, pady=8)
        date_f.pack(side="right", padx=16, pady=10)
        tk.Label(date_f, text=f"📅  {date.today().strftime('%d/%m/%Y')}",
                 font=FONT_SMALL, bg="#F0F3FF", fg=TEXT_MID).pack()

        self.content = tk.Frame(self.main_f, bg=BG, padx=24, pady=20)
        self.content.pack(fill="both", expand=True)

    def navigate(self, key):
        for k, b in self.nav.items(): b.set_active(k == key)
        for w in self.content.winfo_children(): w.destroy()
        titles = {"dashboard":"Tableau de bord","produits":"Produits",
                  "categories":"Catégories","fournisseurs":"Fournisseurs",
                  "commandes":"Commandes","alertes":"Alertes de stock"}
        self.title_lbl.config(text=titles.get(key,""))
        {"dashboard":self.show_dashboard,"produits":self.show_produits,
         "categories":self.show_categories,"fournisseurs":self.show_fournisseurs,
         "commandes":self.show_commandes,"alertes":self.show_alertes}[key]()

    # ───────────────────────────────────────────────────────────
    #  DASHBOARD
    # ───────────────────────────────────────────────────────────
    def show_dashboard(self):
        stats   = db.get_stats()
        alertes = db.get_alertes()
        cmds    = db.get_commandes()

        cf = tk.Frame(self.content, bg=BG)
        cf.pack(fill="x", pady=(0,18))
        for i, (icon, title, val, color) in enumerate([
            ("📦","Produits",      stats['nb_produits'],              ACCENT3),
            ("🏷️","Catégories",   stats['nb_categories'],            SUCCESS),
            ("🚚","Fournisseurs",  stats['nb_fournisseurs'],           ACCENT2),
            ("📋","Commandes",     stats['nb_commandes'],              "#9C27B0"),
            ("⚠️","Alertes",       stats['alertes'],                   DANGER),
            ("💰","Valeur stock",  fmt_fcfa(stats['valeur_stock']),    ACCENT),
        ]):
            StatCard(cf, icon, title, val, color).grid(
                row=0, column=i, padx=5, sticky="nsew")
            cf.columnconfigure(i, weight=1)

        bot = tk.Frame(self.content, bg=BG)
        bot.pack(fill="both", expand=True)
        bot.columnconfigure(0, weight=1); bot.columnconfigure(1, weight=1)

        # Alertes card
        ac = tk.Frame(bot, bg=CARD_BG)
        ac.grid(row=0, column=0, padx=(0,10), sticky="nsew")
        ah = tk.Frame(ac, bg=CARD_BG, padx=16, pady=14)
        ah.pack(fill="x")
        tk.Label(ah, text="⚠️  Alertes de stock", font=FONT_H2,
                 fg=DANGER, bg=CARD_BG).pack(side="left")
        tk.Label(ah, text=f"{len(alertes)} produit(s)", font=FONT_BADGE,
                 fg=DANGER, bg="#FFF3F3", padx=8, pady=3).pack(side="right")
        tk.Frame(ac, bg=BORDER, height=1).pack(fill="x")
        if not alertes:
            tk.Label(ac, text="✅  Tout est en ordre !", font=FONT_BODY,
                     fg=SUCCESS, bg=CARD_BG, pady=20).pack()
        else:
            for p in alertes[:6]:
                r = tk.Frame(ac, bg=CARD_BG, padx=16, pady=9)
                r.pack(fill="x")
                dot = "🔴" if p["quantite"]==0 else "🟠"
                tk.Label(r, text=f"{dot}  {p['nom']}", font=FONT_BODY,
                         fg=TEXT_DARK, bg=CARD_BG).pack(side="left")
                tk.Label(r, text=f"Qté : {p['quantite']}", font=FONT_BADGE,
                         fg=DANGER, bg="#FFF3F3", padx=8, pady=2).pack(side="right")
                tk.Frame(ac, bg=BORDER, height=1).pack(fill="x", padx=16)

        # Commandes card
        cc = tk.Frame(bot, bg=CARD_BG)
        cc.grid(row=0, column=1, padx=(10,0), sticky="nsew")
        ch = tk.Frame(cc, bg=CARD_BG, padx=16, pady=14)
        ch.pack(fill="x")
        tk.Label(ch, text="📋  Dernières commandes", font=FONT_H2,
                 fg=TEXT_DARK, bg=CARD_BG).pack(side="left")
        tk.Frame(cc, bg=BORDER, height=1).pack(fill="x")
        sc_map = {"Livré":(SUCCESS,"#F0FBF8"),"En cours":(WARNING,"#FFF8F0"),
                  "En attente":(ACCENT3,"#F0F5FF"),"Annulé":(DANGER,"#FFF3F3")}
        if not cmds:
            tk.Label(cc, text="Aucune commande", font=FONT_BODY,
                     fg=TEXT_LIGHT, bg=CARD_BG, pady=20).pack()
        else:
            for c in cmds[:6]:
                r = tk.Frame(cc, bg=CARD_BG, padx=16, pady=9)
                r.pack(fill="x")
                tk.Label(r, text=f"#{c['id']}  {c['fournisseur'] or 'N/A'}",
                         font=FONT_BODY, fg=TEXT_DARK, bg=CARD_BG).pack(side="left")
                fc, fbg = sc_map.get(c['statut'], (TEXT_MID,"#F5F5F5"))
                tk.Label(r, text=c['statut'], font=FONT_BADGE,
                         fg=fc, bg=fbg, padx=8, pady=2).pack(side="right")
                tk.Label(r, text=c['date'], font=FONT_SMALL,
                         fg=TEXT_LIGHT, bg=CARD_BG).pack(side="right", padx=10)
                tk.Frame(cc, bg=BORDER, height=1).pack(fill="x", padx=16)

    # ───────────────────────────────────────────────────────────
    #  PRODUITS
    # ───────────────────────────────────────────────────────────
    def show_produits(self):
        cats = db.get_categories()

        tb = tk.Frame(self.content, bg=BG); tb.pack(fill="x", pady=(0,12))
        sf = tk.Frame(tb, bg=CARD_BG, highlightthickness=1,
                      highlightbackground=BORDER, highlightcolor=ACCENT)
        sf.pack(side="left")
        tk.Label(sf, text="🔍", bg=CARD_BG, fg=TEXT_LIGHT, padx=10).pack(side="left")
        sv = tk.StringVar()
        se = tk.Entry(sf, textvariable=sv, font=FONT_BODY, bg=CARD_BG,
                      fg=TEXT_LIGHT, relief="flat", bd=0,
                      insertbackground=ACCENT, width=26)
        se.insert(0, "Rechercher un produit..."); se.pack(side="left", ipady=7, padx=(0,10))
        se.bind("<FocusIn>",  lambda e: (se.delete(0,"end"), se.config(fg=TEXT_DARK)) if se.get()=="Rechercher un produit..." else None)
        se.bind("<FocusOut>", lambda e: (se.insert(0,"Rechercher un produit..."), se.config(fg=TEXT_LIGHT)) if not se.get() else None)

        ModernButton(tb, "Ajouter un produit", color=ACCENT, icon="＋",
                     command=lambda: self._dlg_produit(None, tree, cats)
                     ).pack(side="right")

        card = tk.Frame(self.content, bg=CARD_BG); card.pack(fill="both", expand=True)
        cols = ("ID","Nom du produit","Prix (FCFA)","Quantité","Seuil","Catégorie")
        tree = self._tree(card, cols)

        def refresh(q=""):
            for r in tree.get_children(): tree.delete(r)
            for p in db.get_produits(q):
                tag = "alerte" if p["quantite"]<=p["seuil_alerte"] else ""
                tree.insert("","end", values=(
                    p["id"], p["nom"], fmt_fcfa(p['prix']),
                    p["quantite"], p["seuil_alerte"], p["categorie"] or "—"
                ), tags=(tag,))
            tree.tag_configure("alerte", foreground=DANGER)

        refresh()
        def on_search(*_):
            q = sv.get()
            refresh("" if q=="Rechercher un produit..." else q)
        sv.trace("w", on_search)

        act = tk.Frame(self.content, bg=BG); act.pack(fill="x", pady=8)
        ModernButton(act, "Modifier", color=ACCENT3, icon="✏️",
                     command=lambda: self._dlg_produit(tree, tree, cats)).pack(side="left", padx=4)
        ModernButton(act, "Supprimer", color=DANGER, icon="🗑️",
                     command=lambda: self._del_produit(tree, refresh)).pack(side="left", padx=4)
        ModernButton(act, "Actualiser", color=TEXT_MID, icon="🔄",
                     command=refresh).pack(side="right", padx=4)

    def _dlg_produit(self, sel, tree, cats):
        editing, vals = None, {}
        if sel and sel.selection():
            v = sel.item(sel.selection()[0])["values"]
            editing = v[0]
            prix_raw = str(v[2]).replace(" FCFA","").replace(" ","")
            vals = {"nom":v[1],"prix":prix_raw,"qte":v[3],"seuil":v[4],"cat":v[5]}

        win = tk.Toplevel(self, bg=CARD_BG)
        win.title("Modifier" if editing else "Nouveau produit")
        win.geometry("440x470"); win.resizable(False,False); win.grab_set()

        hdr = tk.Frame(win, bg=ACCENT3 if editing else ACCENT, pady=18)
        hdr.pack(fill="x")
        tk.Label(hdr, text="✏️  Modifier" if editing else "＋  Nouveau produit",
                 font=FONT_H2, fg=TEXT_WHITE,
                 bg=ACCENT3 if editing else ACCENT).pack()

        body = tk.Frame(win, bg=CARD_BG, padx=30, pady=14)
        body.pack(fill="both", expand=True)
        fields = {}
        for lbl, key, default in [
            ("Nom du produit","nom",vals.get("nom","")),
            ("Prix (FCFA)","prix",vals.get("prix","")),
            ("Quantité","qte",vals.get("qte","")),
            ("Seuil d'alerte","seuil",vals.get("seuil",5)),
        ]:
            tk.Label(body, text=lbl, font=FONT_SMALL, fg=TEXT_MID, bg=CARD_BG
                     ).pack(anchor="w", pady=(8,2))
            f = tk.Frame(body, bg=CARD_BG, highlightthickness=1,
                         highlightbackground=BORDER, highlightcolor=ACCENT)
            f.pack(fill="x")
            e = tk.Entry(f, bg=CARD_BG, fg=TEXT_DARK, font=FONT_BODY,
                         relief="flat", bd=0, insertbackground=ACCENT)
            e.insert(0, str(default)); e.pack(fill="x", padx=10, ipady=7)
            fields[key] = e

        tk.Label(body, text="Catégorie", font=FONT_SMALL,
                 fg=TEXT_MID, bg=CARD_BG).pack(anchor="w", pady=(8,2))
        cat_var = tk.StringVar(value=vals.get("cat",""))
        cf = tk.Frame(body, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER)
        cf.pack(fill="x")
        ttk.Combobox(cf, textvariable=cat_var,
                     values=[c["nom"] for c in cats],
                     state="readonly", font=FONT_BODY).pack(fill="x", padx=6, pady=4)

        def save():
            try:
                nom   = fields["nom"].get().strip()
                prix  = float(fields["prix"].get().replace(" ",""))
                qte   = int(fields["qte"].get())
                seuil = int(fields["seuil"].get())
                cat_id = next((c["id"] for c in cats if c["nom"]==cat_var.get()), None)
                if not nom: raise ValueError
            except:
                messagebox.showerror("Erreur","Vérifie les valeurs saisies.",parent=win)
                return
            if editing: db.update_produit(editing, nom, prix, qte, seuil, cat_id)
            else:       db.add_produit(nom, prix, qte, seuil, cat_id)
            win.destroy(); self.show_produits()

        bf = tk.Frame(win, bg=CARD_BG, pady=12)
        bf.pack(fill="x", padx=30)
        ModernButton(bf, "Enregistrer",
                     color=ACCENT3 if editing else ACCENT,
                     command=save).pack(fill="x", ipady=4)

    def _del_produit(self, tree, refresh):
        if not tree.selection():
            messagebox.showwarning("Attention","Sélectionne un produit."); return
        v   = tree.item(tree.selection()[0])["values"]
        pid, nom = v[0], v[1]
        if messagebox.askyesno("Confirmer",f"Supprimer « {nom} » définitivement ?"):
            db.delete_produit(pid); refresh()

    # ───────────────────────────────────────────────────────────
    #  CATEGORIES
    # ───────────────────────────────────────────────────────────
    def show_categories(self):
        tb = tk.Frame(self.content, bg=BG); tb.pack(fill="x", pady=(0,12))
        card = tk.Frame(self.content, bg=CARD_BG); card.pack(fill="both", expand=True)
        tree = self._tree(card, ("ID","Nom de la catégorie"))

        def refresh():
            for r in tree.get_children(): tree.delete(r)
            for c in db.get_categories():
                tree.insert("","end", values=(c["id"], c["nom"]))
        refresh()

        def add():
            n = simpledialog.askstring("Nouvelle catégorie","Nom :",parent=self)
            if n and n.strip(): db.add_categorie(n.strip()); refresh()

        def delete():
            if not tree.selection(): return
            v = tree.item(tree.selection()[0])["values"]
            if messagebox.askyesno("Confirmer",f"Supprimer « {v[1]} » ?"):
                db.delete_categorie(v[0]); refresh()

        ModernButton(tb, "Ajouter", color=ACCENT, icon="＋",
                     command=add).pack(side="right")
        act = tk.Frame(self.content, bg=BG); act.pack(fill="x", pady=8)
        ModernButton(act, "Supprimer", color=DANGER, icon="🗑️",
                     command=delete).pack(side="left", padx=4)

    # ───────────────────────────────────────────────────────────
    #  FOURNISSEURS
    # ───────────────────────────────────────────────────────────
    def show_fournisseurs(self):
        tb = tk.Frame(self.content, bg=BG); tb.pack(fill="x", pady=(0,12))
        card = tk.Frame(self.content, bg=CARD_BG); card.pack(fill="both", expand=True)
        tree = self._tree(card, ("ID","Nom","Téléphone","Email"))

        def refresh():
            for r in tree.get_children(): tree.delete(r)
            for f in db.get_fournisseurs():
                tree.insert("","end", values=(
                    f["id"], f["nom"],
                    f["telephone"] or "—", f["email"] or "—"))
        refresh()

        def dialog(eid=None):
            vals = {}
            if eid and tree.selection():
                v = tree.item(tree.selection()[0])["values"]
                vals = {"nom":v[1],
                        "tel":"" if v[2]=="—" else v[2],
                        "email":"" if v[3]=="—" else v[3]}
            win = tk.Toplevel(self, bg=CARD_BG)
            win.geometry("420x360"); win.resizable(False,False); win.grab_set()
            hdr = tk.Frame(win, bg=ACCENT3 if eid else SUCCESS, pady=18)
            hdr.pack(fill="x")
            tk.Label(hdr, text="✏️  Modifier" if eid else "🚚  Nouveau fournisseur",
                     font=FONT_H2, fg=TEXT_WHITE,
                     bg=ACCENT3 if eid else SUCCESS).pack()
            body = tk.Frame(win, bg=CARD_BG, padx=30, pady=14)
            body.pack(fill="both", expand=True)
            fields = {}
            for lbl, key in [("Nom","nom"),("Téléphone","tel"),("Email","email")]:
                tk.Label(body, text=lbl, font=FONT_SMALL,
                         fg=TEXT_MID, bg=CARD_BG).pack(anchor="w", pady=(8,2))
                f = tk.Frame(body, bg=CARD_BG, highlightthickness=1,
                             highlightbackground=BORDER, highlightcolor=ACCENT)
                f.pack(fill="x")
                e = tk.Entry(f, bg=CARD_BG, fg=TEXT_DARK, font=FONT_BODY,
                             relief="flat", bd=0, insertbackground=ACCENT)
                e.insert(0, vals.get(key,"")); e.pack(fill="x", padx=10, ipady=7)
                fields[key] = e

            def save():
                nom = fields["nom"].get().strip()
                if not nom:
                    messagebox.showerror("Erreur","Nom obligatoire.",parent=win); return
                if eid: db.update_fournisseur(eid, nom, fields["tel"].get(), fields["email"].get())
                else:   db.add_fournisseur(nom, fields["tel"].get(), fields["email"].get())
                win.destroy(); refresh()

            bf = tk.Frame(win, bg=CARD_BG, pady=12); bf.pack(fill="x", padx=30)
            ModernButton(bf, "Enregistrer",
                         color=ACCENT3 if eid else SUCCESS,
                         command=save).pack(fill="x", ipady=4)

        def modify():
            if not tree.selection():
                messagebox.showwarning("Attention","Sélectionne un fournisseur."); return
            dialog(eid=tree.item(tree.selection()[0])["values"][0])

        def delete():
            if not tree.selection(): return
            v = tree.item(tree.selection()[0])["values"]
            if messagebox.askyesno("Confirmer",f"Supprimer « {v[1]} » ?"):
                db.delete_fournisseur(v[0]); refresh()

        ModernButton(tb, "Ajouter", color=ACCENT, icon="＋",
                     command=lambda: dialog()).pack(side="right", padx=4)
        act = tk.Frame(self.content, bg=BG); act.pack(fill="x", pady=8)
        ModernButton(act, "Modifier",   color=ACCENT3, icon="✏️", command=modify).pack(side="left", padx=4)
        ModernButton(act, "Supprimer",  color=DANGER,  icon="🗑️", command=delete).pack(side="left", padx=4)

    # ───────────────────────────────────────────────────────────
    #  COMMANDES
    # ───────────────────────────────────────────────────────────
    def show_commandes(self):
        tb = tk.Frame(self.content, bg=BG); tb.pack(fill="x", pady=(0,12))
        card = tk.Frame(self.content, bg=CARD_BG); card.pack(fill="both", expand=True)
        cols = ("ID","Fournisseur","Date","Statut","Articles","Total (FCFA)")
        tree = self._tree(card, cols)

        stags = {"Livré":"livré","Annulé":"annulé","En cours":"encours","En attente":"attente"}

        def refresh():
            for r in tree.get_children(): tree.delete(r)
            for c in db.get_commandes():
                tree.insert("","end", values=(
                    c["id"], c["fournisseur"] or "—", c["date"],
                    c["statut"], c["nb_lignes"] or 0,
                    fmt_fcfa(c['total'] or 0)
                ), tags=(stags.get(c["statut"],""),))
            tree.tag_configure("livré",   foreground=SUCCESS)
            tree.tag_configure("annulé",  foreground=DANGER)
            tree.tag_configure("encours", foreground=WARNING)
            tree.tag_configure("attente", foreground=ACCENT3)
        refresh()

        def new_cmd():
            fours = db.get_fournisseurs()
            if not fours:
                messagebox.showwarning("Attention","Ajoute d'abord un fournisseur."); return
            win = tk.Toplevel(self, bg=CARD_BG)
            win.geometry("420x340"); win.resizable(False,False); win.grab_set()
            hdr = tk.Frame(win, bg="#9C27B0", pady=18); hdr.pack(fill="x")
            tk.Label(hdr, text="📋  Nouvelle commande",
                     font=FONT_H2, fg=TEXT_WHITE, bg="#9C27B0").pack()
            body = tk.Frame(win, bg=CARD_BG, padx=30, pady=14)
            body.pack(fill="both", expand=True)

            four_var = tk.StringVar(value=fours[0]["nom"])
            date_var = tk.StringVar(value=str(date.today()))
            stat_var = tk.StringVar(value="En attente")

            for lbl, var, vals_list in [
                ("Fournisseur", four_var, [f["nom"] for f in fours]),
                ("Statut",      stat_var, ["En attente","En cours","Livré","Annulé"]),
            ]:
                tk.Label(body, text=lbl, font=FONT_SMALL,
                         fg=TEXT_MID, bg=CARD_BG).pack(anchor="w", pady=(8,2))
                f = tk.Frame(body, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER)
                f.pack(fill="x")
                ttk.Combobox(f, textvariable=var, values=vals_list,
                             state="readonly", font=FONT_BODY).pack(fill="x", padx=6, pady=4)

            tk.Label(body, text="Date (AAAA-MM-JJ)", font=FONT_SMALL,
                     fg=TEXT_MID, bg=CARD_BG).pack(anchor="w", pady=(8,2))
            df = tk.Frame(body, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER)
            df.pack(fill="x")
            date_e = tk.Entry(df, bg=CARD_BG, fg=TEXT_DARK, font=FONT_BODY,
                              relief="flat", bd=0, insertbackground=ACCENT)
            date_e.insert(0, str(date.today()))
            date_e.pack(fill="x", padx=10, ipady=7)

            def save():
                fid = next((x["id"] for x in fours if x["nom"]==four_var.get()), None)
                db.add_commande(fid, date_e.get(), stat_var.get())
                win.destroy(); refresh()

            bf = tk.Frame(win, bg=CARD_BG, pady=12); bf.pack(fill="x", padx=30)
            ModernButton(bf, "Créer la commande", color="#9C27B0",
                         command=save).pack(fill="x", ipady=4)

        def change_statut():
            if not tree.selection(): return
            v = tree.item(tree.selection()[0])["values"]
            cid, cur = v[0], v[3]
            win = tk.Toplevel(self, bg=CARD_BG)
            win.geometry("300,220".replace(",","x")); win.resizable(False,False); win.grab_set()
            hdr = tk.Frame(win, bg=ACCENT3, pady=16); hdr.pack(fill="x")
            tk.Label(hdr, text="🔄  Changer le statut",
                     font=FONT_H2, fg=TEXT_WHITE, bg=ACCENT3).pack()
            body = tk.Frame(win, bg=CARD_BG, padx=30, pady=14)
            body.pack(fill="both", expand=True)
            tk.Label(body, text="Nouveau statut", font=FONT_SMALL,
                     fg=TEXT_MID, bg=CARD_BG).pack(anchor="w", pady=(8,4))
            s_var = tk.StringVar(value=cur)
            sf = tk.Frame(body, bg=CARD_BG, highlightthickness=1, highlightbackground=BORDER)
            sf.pack(fill="x")
            ttk.Combobox(sf, textvariable=s_var,
                         values=["En attente","En cours","Livré","Annulé"],
                         state="readonly", font=FONT_BODY).pack(fill="x", padx=6, pady=4)
            bf = tk.Frame(win, bg=CARD_BG, pady=8); bf.pack(fill="x", padx=30)
            ModernButton(bf, "Appliquer", color=ACCENT3,
                         command=lambda: [db.update_statut_commande(cid,s_var.get()),
                                           win.destroy(), refresh()]
                         ).pack(fill="x", ipady=4)

        def del_cmd():
            if not tree.selection(): return
            cid = tree.item(tree.selection()[0])["values"][0]
            if messagebox.askyesno("Confirmer",f"Supprimer la commande #{cid} ?"):
                db.delete_commande(cid); refresh()

        ModernButton(tb, "Nouvelle commande", color="#9C27B0", icon="＋",
                     command=new_cmd).pack(side="right", padx=4)
        act = tk.Frame(self.content, bg=BG); act.pack(fill="x", pady=8)
        ModernButton(act,"Changer statut",color=ACCENT3,icon="🔄",command=change_statut).pack(side="left",padx=4)
        ModernButton(act,"Supprimer",color=DANGER,icon="🗑️",command=del_cmd).pack(side="left",padx=4)
        ModernButton(act,"Actualiser",color=TEXT_MID,icon="🔄",command=refresh).pack(side="right",padx=4)

    # ───────────────────────────────────────────────────────────
    #  ALERTES
    # ───────────────────────────────────────────────────────────
    def show_alertes(self):
        alertes = db.get_alertes()
        if not alertes:
            card = tk.Frame(self.content, bg=CARD_BG); card.pack(fill="both", expand=True)
            tk.Label(card, text="✅", font=("Segoe UI",48),
                     bg=CARD_BG, fg=SUCCESS).pack(pady=(60,10))
            tk.Label(card, text="Tout est en ordre !",
                     font=FONT_H1, fg=SUCCESS, bg=CARD_BG).pack()
            tk.Label(card, text="Aucun produit n'est en rupture ou sous le seuil d'alerte.",
                     font=FONT_BODY, fg=TEXT_LIGHT, bg=CARD_BG, pady=8).pack()
            return

        banner = tk.Frame(self.content, bg="#FFF3F3", pady=12)
        banner.pack(fill="x", pady=(0,14))
        tk.Label(banner,
                 text=f"⚠️   {len(alertes)} produit(s) nécessitent votre attention",
                 font=FONT_H2, fg=DANGER, bg="#FFF3F3", padx=16).pack(side="left")

        card = tk.Frame(self.content, bg=CARD_BG); card.pack(fill="both", expand=True)
        cols = ("ID","Nom du produit","Quantité actuelle","Seuil d'alerte","Catégorie","État")
        tree = self._tree(card, cols)
        for p in alertes:
            etat = "🔴  RUPTURE" if p["quantite"]==0 else "🟠  Stock bas"
            tree.insert("","end", values=(
                p["id"], p["nom"], p["quantite"],
                p["seuil_alerte"], p["categorie"] or "—", etat
            ), tags=("rupture" if p["quantite"]==0 else "bas",))
        tree.tag_configure("rupture", foreground=DANGER)
        tree.tag_configure("bas",     foreground=WARNING)

    # ───────────────────────────────────────────────────────────
    #  HELPER — TreeView
    # ───────────────────────────────────────────────────────────
    def _tree(self, parent, cols):
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x")
        wrap = tk.Frame(parent, bg=CARD_BG); wrap.pack(fill="both", expand=True)
        sb   = ttk.Scrollbar(wrap, orient="vertical")
        tree = ttk.Treeview(wrap, columns=cols, show="headings",
                            style="Tree.Treeview", yscrollcommand=sb.set)
        sb.config(command=tree.yview)
        for c in cols:
            tree.heading(c, text=c)
            w = 200 if c in ("Nom du produit","Nom","Email","Fournisseur","Nom de la catégorie") else 120
            tree.column(c, width=w, anchor="center", minwidth=60)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        return tree


if __name__ == "__main__":
    app = App()
    app.mainloop()