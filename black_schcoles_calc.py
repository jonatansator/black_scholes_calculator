import math
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Step 1: Define pricing functions
def opt_call(X, K, T, r, v):
    d1 = (math.log(X/K) + (r + 0.5 * v**2) * T) / (v * math.sqrt(T))
    d2 = d1 - v * math.sqrt(T)
    return X * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

def opt_put(X, K, T, r, v):
    d1 = (math.log(X/K) + (r + 0.5 * v**2) * T) / (v * math.sqrt(T))
    d2 = d1 - v * math.sqrt(T)
    return K * math.exp(-r * T) * norm.cdf(-d2) - X * norm.cdf(-d1)

# Step 2: Define calculation and plotting logic
def update_results():
    try:
        X = float(e1.get())
        K = float(e2.get())
        T = float(e3.get())
        r = float(e4.get())
        v = float(e5.get())

        # Step 3: Validate inputs
        if X <= 0 or K <= 0 or T <= 0 or v <= 0:
            raise ValueError("All inputs except rate must be positive")
        if r < 0:
            raise ValueError("Rate cannot be negative")

        # Step 4: Compute intermediate values and prices
        df = (math.log(X/K) + (r + 0.5 * v**2) * T) / (v * math.sqrt(T))
        dd = df - v * math.sqrt(T)
        C = opt_call(X, K, T, r, v)
        P = opt_put(X, K, T, r, v)

        # Step 5: Update display labels
        lbl_df.config(text=f"df: {df:.4f}")
        lbl_dd.config(text=f"dd: {dd:.4f}")
        lbl_C.config(text=f"Call: ${C:.2f}")
        lbl_P.config(text=f"Put: ${P:.2f}")

        # Step 6: Generate plot data
        XX = np.linspace(max(0.05, X - 25), X + 25, 150)
        YC = [opt_call(x, K, T, r, v) for x in XX]
        YP = [opt_put(x, K, T, r, v) for x in XX]

        # Step 7: Update plot
        ax.clear()
        ax.plot(XX, YC, color='#FF6B6B', lw=2, label='Call Price')
        ax.plot(XX, YP, color='#4ECDC4', lw=2, label='Put Price')
        ax.axvline(K, color='#888888', ls='--', alpha=0.6, label=f'Strike={K}')
        ax.axvline(X, color='#BBBBBB', ls=':', alpha=0.6, label=f'Price={X}')
        ax.set_xlabel('Price', color='white')
        ax.set_ylabel('Value', color='white')
        ax.set_title('Option Pricing', color='white')
        ax.set_facecolor('#2B2B2B')
        fig.set_facecolor('#1E1E1E')
        ax.grid(True, ls='--', color='#555555', alpha=0.5)
        ax.legend(facecolor='#333333', edgecolor='white', labelcolor='white')
        ax.tick_params(colors='white')
        canv.draw()

    except ValueError as err:
        messagebox.showerror("Error", str(err))

# Step 8: Set up GUI
root = tk.Tk()
root.title("Option Calc")
root.configure(bg='#1E1E1E')

frm = ttk.Frame(root, padding=10)
frm.pack()
frm.configure(style='Dark.TFrame')

# Step 9: Create plot
fig, ax = plt.subplots(figsize=(7, 5))
canv = FigureCanvasTkAgg(fig, master=frm)
canv.get_tk_widget().pack(side=tk.LEFT)

# Step 10: Create input panel
pf = ttk.Frame(frm)
pf.pack(side=tk.RIGHT, padx=10)
pf.configure(style='Dark.TFrame')

# Dark theme style
style = ttk.Style()
style.theme_use('default')
style.configure('Dark.TFrame', background='#1E1E1E')
style.configure('Dark.TLabel', background='#1E1E1E', foreground='white')
style.configure('TButton', background='#333333', foreground='white')
style.configure('TEntry', fieldbackground='#333333', foreground='white')

ttk.Label(pf, text="Price (X):", style='Dark.TLabel').pack(pady=3)
e1 = ttk.Entry(pf); e1.pack(pady=3); e1.insert(0, "50")
ttk.Label(pf, text="Strike (K):", style='Dark.TLabel').pack(pady=3)
e2 = ttk.Entry(pf); e2.pack(pady=3); e2.insert(0, "45")
ttk.Label(pf, text="Time (T):", style='Dark.TLabel').pack(pady=3)
e3 = ttk.Entry(pf); e3.pack(pady=3); e3.insert(0, "1.5")
ttk.Label(pf, text="Rate (r):", style='Dark.TLabel').pack(pady=3)
e4 = ttk.Entry(pf); e4.pack(pady=3); e4.insert(0, "0.05")
ttk.Label(pf, text="Vol (v):", style='Dark.TLabel').pack(pady=3)
e5 = ttk.Entry(pf); e5.pack(pady=3); e5.insert(0, "0.15")

ttk.Button(pf, text="Run", command=update_results).pack(pady=10)

lbl_df = ttk.Label(pf, text="df: ", style='Dark.TLabel'); lbl_df.pack(pady=2)
lbl_dd = ttk.Label(pf, text="dd: ", style='Dark.TLabel'); lbl_dd.pack(pady=2)
lbl_C = ttk.Label(pf, text="Call: ", style='Dark.TLabel'); lbl_C.pack(pady=2)
lbl_P = ttk.Label(pf, text="Put: ", style='Dark.TLabel'); lbl_P.pack(pady=2)

# Step 11: Initial run and GUI loop
update_results()
root.mainloop()