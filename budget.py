import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

incomes  = []   
expenses = []   

def total(lst):
    return sum(item["amount"] for item in lst)

def saved():
    return total(incomes) - total(expenses)

def refresh():
    lbl_income.config(text=f"Inkomst: {total(incomes):,.2f} kr")
    lbl_expense.config(text=f"Utkomst: {total(expenses):,.2f} kr")
    s = saved()
    lbl_saved.config(
        text=f"Pengar sparat: {s:,.2f} kr",
        foreground="#27ae60" if s >= 0 else "#e74c3c"
    )

    income_tree.delete(*income_tree.get_children())
    for item in incomes:
        income_tree.insert("", "end", values=(item["name"], f"{item['amount']:,.2f} kr"))

    expense_tree.delete(*expense_tree.get_children())
    for item in expenses:
        expense_tree.insert("", "end", values=(item["name"], f"{item['amount']:,.2f} kr"))

def add_item(lst, tree):
    name = simpledialog.askstring("Namn", "Ange namn:", parent=root)
    if not name:
        return
    try:
        amount = float(simpledialog.askstring("Belopp", "Ange belopp (kr):", parent=root).replace(",", "."))
    except (TypeError, ValueError):
        messagebox.showerror("Fel", "Ogiltigt belopp.")
        return
    lst.append({"name": name, "amount": amount})
    refresh()

def remove_item(lst, tree):
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Info", "Välj en rad att radera.")
        return
    idx = tree.index(sel[0])
    lst.pop(idx)
    refresh()

root = tk.Tk()
root.title("Budgethanterare")
root.resizable(False, False)

BG      = "#1a1a2e"
CARD    = "#16213e"
ACCENT  = "#0f3460"
GREEN   = "#27ae60"
RED     = "#e74c3c"
TEXT    = "#e0e0e0"
SUBTEXT = "#a0aec0"
FONT    = ("Segoe UI", 10)

root.configure(bg=BG)
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
    background=CARD, foreground=TEXT, fieldbackground=CARD,
    rowheight=28, font=FONT, borderwidth=0)
style.configure("Treeview.Heading",
    background=ACCENT, foreground=TEXT, font=("Segoe UI", 10, "bold"), relief="flat")
style.map("Treeview", background=[("selected", ACCENT)])
style.configure("TFrame", background=BG)

bar = tk.Frame(root, bg=CARD, pady=12, padx=20)
bar.pack(fill="x", padx=20, pady=(20, 10))

lbl_income  = tk.Label(bar, text="Inkomst: 0,00 kr",       bg=CARD, fg=GREEN,   font=("Segoe UI", 11, "bold"))
lbl_expense = tk.Label(bar, text="Utkomst: 0,00 kr",       bg=CARD, fg=RED,     font=("Segoe UI", 11, "bold"))
lbl_saved   = tk.Label(bar, text="Pengar sparat: 0,00 kr", bg=CARD, fg=GREEN,   font=("Segoe UI", 11, "bold"))

lbl_income.pack(side="left",  padx=20)
lbl_saved.pack(side="right",  padx=20)
lbl_expense.pack(side="right", padx=20)

panels = tk.Frame(root, bg=BG)
panels.pack(padx=20, pady=10, fill="both")

def make_panel(parent, title, lst, side):
    frame = tk.Frame(parent, bg=CARD, padx=12, pady=12)
    frame.pack(side=side, fill="both", expand=True, padx=(0 if side=="right" else 0, 10 if side=="left" else 0))

    tk.Label(frame, text=title, bg=CARD, fg=TEXT,
             font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))

    cols = ("Namn", "Belopp")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=140 if col == "Namn" else 120, anchor="w" if col=="Namn" else "e")
    tree.pack(fill="both", expand=True)

    btn_frame = tk.Frame(frame, bg=CARD)
    btn_frame.pack(fill="x", pady=(8, 0))

    btn_add = tk.Button(btn_frame, text="＋ Lägg till",
        command=lambda l=lst, t=tree: add_item(l, t),
        bg=GREEN, fg="white", font=("Segoe UI", 9, "bold"),
        relief="flat", padx=10, pady=4, cursor="hand2")
    btn_add.pack(side="left", padx=(0, 6))

    btn_del = tk.Button(btn_frame, text="✕ Radera",
        command=lambda l=lst, t=tree: remove_item(l, t),
        bg=RED, fg="white", font=("Segoe UI", 9, "bold"),
        relief="flat", padx=10, pady=4, cursor="hand2")
    btn_del.pack(side="left")

    return tree

income_tree  = make_panel(panels, "💰  Inkomster", incomes,  "left")
expense_tree = make_panel(panels, "💸  Utkomster", expenses, "right")

tk.Button(root, text="Avsluta", command=root.quit,
    bg=ACCENT, fg=TEXT, font=("Segoe UI", 10, "bold"),
    relief="flat", padx=20, pady=6, cursor="hand2"
).pack(pady=(0, 20))

refresh()
root.mainloop()