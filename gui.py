from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from PIL import Image, ImageTk

from coffee_maker import CoffeeMaker
from menu import Menu
from money_machine import MoneyMachine


class CoffeeMachineGUI:
    """Tkinter interface for the coffee machine."""

    def __init__(self):
        self.menu = Menu()
        self.coffee_maker = CoffeeMaker()
        self.money_machine = MoneyMachine()
        self.selected_drink = None
        self.card_widgets = {}
        self.brew_job = None

        self.base_dir = Path(__file__).resolve().parent
        self.assets_dir = self.base_dir / "assets"

        self.BG = "#F4EFEA"
        self.CARD = "#FFFFFF"
        self.BROWN = "#6F4E37"
        self.ACCENT = "#C98C53"
        self.TEXT = "#2F2F2F"
        self.MUTED = "#6B625C"
        self.SUCCESS = "#3E8E5A"
        self.DANGER = "#D9534F"

        self.root = tk.Tk()
        self.root.title("BrewMaster")
        self.root.configure(bg=self.BG)
        self.configure_window()

        self.configure_styles()
        self.load_images()
        self.create_layout()

    def configure_window(self):
        self.root.minsize(1100, 720)
        self.root.resizable(True, True)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        try:
            self.root.state("zoomed")
        except tk.TclError:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.root.geometry(f"{screen_width}x{screen_height}+0+0")

    def toggle_fullscreen(self, event=None):
        is_fullscreen = bool(self.root.attributes("-fullscreen"))
        self.root.attributes("-fullscreen", not is_fullscreen)

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)

    def configure_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "Coffee.Horizontal.TProgressbar",
            troughcolor="#E9DDD2",
            background=self.ACCENT,
            bordercolor="#E9DDD2",
            lightcolor=self.ACCENT,
            darkcolor=self.ACCENT,
            thickness=12,
        )

    def load_image(self, name, size):
        image = Image.open(self.assets_dir / name).resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def load_images(self):
        self.espresso_img = self.load_image("espresso.png", (120, 120))
        self.latte_img = self.load_image("latte.png", (120, 120))
        self.cappuccino_img = self.load_image("cappuccino.png", (120, 120))
        self.logo_img = self.load_image("logo.png", (58, 58))

    def create_layout(self):
        self.header = tk.Frame(self.root, bg=self.BROWN, height=80)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        logo_frame = tk.Frame(self.header, bg=self.BROWN)
        logo_frame.pack(pady=9)

        tk.Label(logo_frame, image=self.logo_img, bg=self.BROWN).pack(
            side="left", padx=(0, 12)
        )
        tk.Label(
            logo_frame,
            text="BrewMaster",
            bg=self.BROWN,
            fg="white",
            font=("Poppins", 24, "bold"),
        ).pack(side="left")

        self.main_frame = tk.Frame(self.root, bg=self.BG)
        self.main_frame.pack(fill="both", expand=True)

        self.left_panel = tk.Frame(self.main_frame, bg=self.BG, width=780)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=24, pady=20)
        self.left_panel.pack_propagate(False)

        self.right_panel = tk.Frame(self.main_frame, bg=self.CARD, width=330)
        self.right_panel.pack(side="right", fill="y", padx=(0, 24), pady=20)
        self.right_panel.pack_propagate(False)

        self.create_menu_cards()
        self.create_brew_panel()
        self.create_dashboard()

    def create_dashboard(self):
        tk.Label(
            self.right_panel,
            text="Machine Status",
            bg=self.CARD,
            fg=self.BROWN,
            font=("Poppins", 18, "bold"),
        ).pack(pady=(18, 14))

        self.water_label = self.create_resource_row("Water")
        self.water_bar = self.create_resource_bar(1000)
        self.milk_label = self.create_resource_row("Milk")
        self.milk_bar = self.create_resource_bar(1000)
        self.coffee_label = self.create_resource_row("Coffee")
        self.coffee_bar = self.create_resource_bar(500)

        self.money_label = tk.Label(
            self.right_panel,
            bg=self.CARD,
            fg=self.TEXT,
            font=("Poppins", 12, "bold"),
        )
        self.money_label.pack(pady=24)

        self.status_label = tk.Label(
            self.right_panel,
            text="Ready to brew",
            bg=self.CARD,
            fg=self.SUCCESS,
            wraplength=270,
            justify="center",
            font=("Poppins", 11, "bold"),
        )
        self.status_label.pack(pady=(0, 18))

        self.refill_button = self.make_button(
            self.right_panel, "Refill", self.ACCENT, self.refill_window
        )
        self.refill_button.pack(pady=8)

        self.report_button = self.make_button(
            self.right_panel, "Report", self.BROWN, self.show_report
        )
        self.report_button.pack(pady=8)

        self.exit_button = self.make_button(
            self.right_panel, "Exit", self.DANGER, self.root.destroy
        )
        self.exit_button.pack(pady=8)

        self.update_dashboard()

    def create_resource_row(self, name):
        label = tk.Label(
            self.right_panel,
            bg=self.CARD,
            fg=self.TEXT,
            font=("Poppins", 12),
        )
        label.pack(anchor="w", padx=26, pady=(8, 3))
        return label

    def create_resource_bar(self, maximum):
        bar = ttk.Progressbar(
            self.right_panel,
            style="Coffee.Horizontal.TProgressbar",
            maximum=maximum,
            length=260,
        )
        bar.pack(pady=(0, 8))
        return bar

    def create_menu_cards(self):
        tk.Label(
            self.left_panel,
            text="Choose Your Coffee",
            bg=self.BG,
            fg=self.BROWN,
            font=("Poppins", 22, "bold"),
        ).pack(anchor="w", pady=(6, 18))

        self.cards_frame = tk.Frame(self.left_panel, bg=self.BG)
        self.cards_frame.pack(anchor="w")

        images = {
            "espresso": self.espresso_img,
            "latte": self.latte_img,
            "cappuccino": self.cappuccino_img,
        }

        for drink in self.menu.get_menu():
            card = tk.Frame(
                self.cards_frame,
                bg=self.CARD,
                width=205,
                height=245,
                highlightbackground="#D9CFC7",
                highlightthickness=1,
                cursor="hand2",
            )
            card.pack(side="left", padx=(0, 18))
            card.pack_propagate(False)
            card.bind("<Button-1>", lambda event, item=drink: self.select_drink(item))
            card.bind("<Enter>", lambda event, item=drink: self.set_card_hover(item, True))
            card.bind("<Leave>", lambda event, item=drink: self.set_card_hover(item, False))

            image_label = tk.Label(card, image=images[drink.name], bg=self.CARD)
            image_label.pack(pady=(10, 6))
            image_label.bind("<Button-1>", lambda event, item=drink: self.select_drink(item))

            tk.Label(
                card,
                text=drink.name.title(),
                bg=self.CARD,
                fg=self.TEXT,
                font=("Poppins", 15, "bold"),
            ).pack()

            tk.Label(
                card,
                text=f"${drink.cost:.2f}",
                bg=self.CARD,
                fg=self.ACCENT,
                font=("Poppins", 14, "bold"),
            ).pack(pady=5)

            button_footer = tk.Frame(card, bg=self.CARD, height=50)
            button_footer.pack(side="bottom", fill="x")
            button_footer.pack_propagate(False)

            button = self.make_button(
                button_footer,
                "Select",
                self.BROWN,
                lambda item=drink: self.select_drink(item),
                11,
                12,
            )
            button.pack(pady=8)
            self.card_widgets[drink.name] = card

    def create_brew_panel(self):
        self.info_frame = tk.Frame(self.left_panel, bg=self.CARD, height=315)
        self.info_frame.pack(fill="x", pady=(22, 0))
        self.info_frame.pack_propagate(False)

        self.info_title = tk.Label(
            self.info_frame,
            text="Select a drink to begin",
            bg=self.CARD,
            fg=self.BROWN,
            font=("Poppins", 19, "bold"),
        )
        self.info_title.pack(pady=(12, 3))

        self.info_details = tk.Label(
            self.info_frame,
            text="Your order details will appear here.",
            bg=self.CARD,
            fg=self.MUTED,
            justify="center",
            font=("Poppins", 12),
        )
        self.info_details.pack()

        self.buy_button = self.make_button(
            self.info_frame, "Buy Coffee", self.ACCENT, self.buy_selected_drink, 13, 18
        )
        self.buy_button.pack(pady=10)
        self.buy_button.config(state="disabled", bg="#B8A79A")

        self.animation_canvas = tk.Canvas(
            self.info_frame,
            width=600,
            height=135,
            bg=self.CARD,
            bd=0,
            highlightthickness=0,
        )
        self.animation_canvas.pack(pady=(0, 6))

        self.brew_progress = ttk.Progressbar(
            self.info_frame,
            style="Coffee.Horizontal.TProgressbar",
            maximum=100,
            length=520,
        )
        self.brew_progress.pack()
        self.draw_idle_cup()

    def make_button(self, parent, text, bg, command, font_size=11, width=18):
        button = tk.Button(
            parent,
            text=text,
            bg=bg,
            fg="white",
            activebackground=bg,
            activeforeground="white",
            width=width,
            font=("Poppins", font_size, "bold"),
            relief="flat",
            bd=0,
            borderwidth=0,
            highlightthickness=0,
            highlightbackground=bg,
            highlightcolor=bg,
            overrelief="flat",
            takefocus=0,
            cursor="hand2",
            command=command,
        )
        button.bind("<Enter>", lambda event: button.config(bg=self.lighten(bg)))
        button.bind("<Leave>", lambda event: button.config(bg=bg))
        return button

    def lighten(self, color):
        color = color.lstrip("#")
        red, green, blue = (int(color[index:index + 2], 16) for index in (0, 2, 4))
        red = min(255, red + 18)
        green = min(255, green + 18)
        blue = min(255, blue + 18)
        return f"#{red:02x}{green:02x}{blue:02x}"

    def set_card_hover(self, drink, is_hovered):
        if self.selected_drink and self.selected_drink.name == drink.name:
            return
        self.card_widgets[drink.name].config(
            highlightbackground=self.ACCENT if is_hovered else "#D9CFC7",
            highlightthickness=2 if is_hovered else 1,
        )

    def select_drink(self, drink):
        self.selected_drink = drink

        for card in self.card_widgets.values():
            card.config(highlightbackground="#D9CFC7", highlightthickness=1)

        self.card_widgets[drink.name].config(
            highlightbackground=self.ACCENT,
            highlightthickness=3,
        )

        ingredients = drink.ingredients
        details = (
            f"Price: ${drink.cost:.2f}\n"
            f"Water: {ingredients['water']} ml   "
            f"Milk: {ingredients['milk']} ml   "
            f"Coffee: {ingredients['coffee']} g"
        )
        self.info_title.config(text=drink.name.title())
        self.info_details.config(text=details, fg=self.TEXT)
        self.buy_button.config(state="normal", bg=self.ACCENT)
        self.status_label.config(text=f"{drink.name.title()} selected", fg=self.SUCCESS)
        self.brew_progress["value"] = 0
        self.draw_idle_cup()

    def buy_selected_drink(self):
        if self.selected_drink is None:
            messagebox.showwarning("No Drink Selected", "Please select a drink first.")
            return

        available, message = self.coffee_maker.is_resource_sufficient(self.selected_drink)
        if not available:
            self.status_label.config(text=message, fg=self.DANGER)
            messagebox.showerror("Insufficient Resources", message)
            return

        self.open_payment_window()

    def open_payment_window(self):
        payment = tk.Toplevel(self.root)
        payment.title("Payment")
        payment.geometry("360x300")
        payment.resizable(False, False)
        payment.configure(bg=self.CARD)
        payment.transient(self.root)
        payment.grab_set()

        tk.Label(
            payment,
            text=self.selected_drink.name.title(),
            font=("Poppins", 18, "bold"),
            bg=self.CARD,
            fg=self.BROWN,
        ).pack(pady=(22, 5))

        tk.Label(
            payment,
            text=f"Price: ${self.selected_drink.cost:.2f}",
            font=("Poppins", 14),
            bg=self.CARD,
            fg=self.TEXT,
        ).pack()

        tk.Label(
            payment,
            text="Enter amount paid",
            font=("Poppins", 12),
            bg=self.CARD,
            fg=self.MUTED,
        ).pack(pady=(20, 5))

        amount_entry = tk.Entry(payment, font=("Poppins", 14), justify="center")
        amount_entry.pack()
        amount_entry.focus()

        payment_status = tk.Label(
            payment,
            text="",
            bg=self.CARD,
            fg=self.DANGER,
            font=("Poppins", 10, "bold"),
        )
        payment_status.pack(pady=(8, 0))

        def process_payment():
            try:
                amount = float(amount_entry.get())
                success, value, msg = self.money_machine.make_payment(
                    amount, self.selected_drink.cost
                )
            except ValueError as error:
                payment_status.config(text=str(error))
                return

            if not success:
                payment_status.config(text=msg)
                return

            coffee_msg = self.coffee_maker.make_coffee(self.selected_drink)
            self.update_dashboard()
            payment.destroy()
            self.animate_brewing(msg, coffee_msg)

        pay_button = self.make_button(payment, "Pay", self.BROWN, process_payment, 12, 15)
        pay_button.pack(pady=18)
        payment.bind("<Return>", lambda event: process_payment())

    def animate_brewing(self, payment_msg, coffee_msg):
        if self.brew_job is not None:
            self.root.after_cancel(self.brew_job)
            self.brew_job = None

        self.buy_button.config(state="disabled", bg="#B8A79A")
        self.status_label.config(text="Brewing in progress", fg=self.ACCENT)
        steps = ["Grinding beans", "Heating water", "Brewing", "Pouring", "Ready"]

        def tick(frame=0):
            progress = min(100, frame)
            self.brew_progress["value"] = progress
            step_index = min(len(steps) - 1, progress // 25)
            self.info_details.config(text=steps[step_index], fg=self.TEXT)
            self.draw_brewing_frame(progress)

            if progress < 100:
                self.brew_job = self.root.after(35, lambda: tick(frame + 2))
                return

            self.brew_job = None
            self.info_details.config(text=f"{payment_msg}\n{coffee_msg}", fg=self.SUCCESS)
            self.status_label.config(text="Ready for the next order", fg=self.SUCCESS)
            self.buy_button.config(state="normal", bg=self.ACCENT)
            messagebox.showinfo("Success", f"{payment_msg}\n\n{coffee_msg}")

        tick()

    def draw_idle_cup(self):
        self.animation_canvas.delete("all")
        self.draw_cup(300, 72, fill="#EDE3DA", coffee_level=0)

    def draw_brewing_frame(self, progress):
        canvas = self.animation_canvas
        canvas.delete("all")
        coffee_level = max(0, min(38, int(progress * 0.38)))
        self.draw_cup(300, 72, fill="#FFFFFF", coffee_level=coffee_level)

        drip_y = 20 + (progress % 24)
        canvas.create_line(300, 18, 300, 68, fill=self.ACCENT, width=3)
        canvas.create_oval(296, drip_y + 28, 304, drip_y + 36, fill=self.ACCENT, outline="")

        for index, x_offset in enumerate((-32, 0, 32)):
            phase = (progress + index * 12) % 50
            y = 58 - phase
            canvas.create_arc(
                280 + x_offset,
                y,
                322 + x_offset,
                y + 42,
                start=95,
                extent=120,
                style="arc",
                outline="#B7A99D",
                width=2,
            )

    def draw_cup(self, x, y, fill, coffee_level):
        canvas = self.animation_canvas
        canvas.create_oval(x - 62, y + 26, x + 62, y + 42, fill="#E8DDD4", outline="")
        canvas.create_rectangle(x - 48, y, x + 48, y + 42, fill=fill, outline="#6F4E37", width=2)
        canvas.create_arc(x - 48, y + 28, x + 48, y + 56, start=180, extent=180, fill=fill, outline="#6F4E37", width=2)
        canvas.create_arc(x + 38, y + 9, x + 78, y + 39, start=270, extent=180, style="arc", outline="#6F4E37", width=4)
        if coffee_level:
            top = y + 40 - coffee_level
            canvas.create_rectangle(x - 44, top, x + 44, y + 41, fill="#6F4E37", outline="")
            canvas.create_oval(x - 44, top - 5, x + 44, top + 7, fill="#8B5A3C", outline="")

    def update_dashboard(self):
        resources = self.coffee_maker.report()

        self.water_label.config(text=f"Water: {resources['water']} ml")
        self.milk_label.config(text=f"Milk: {resources['milk']} ml")
        self.coffee_label.config(text=f"Coffee: {resources['coffee']} g")

        self.water_bar["value"] = resources["water"]
        self.milk_bar["value"] = resources["milk"]
        self.coffee_bar["value"] = resources["coffee"]
        self.money_label.config(text=f"Profit: ${self.money_machine.get_profit():.2f}")

    def refill_window(self):
        win = tk.Toplevel(self.root)
        win.title("Refill Machine")
        win.geometry("320x310")
        win.resizable(False, False)
        win.configure(bg=self.CARD)
        win.transient(self.root)
        win.grab_set()

        tk.Label(
            win,
            text="Refill Machine",
            bg=self.CARD,
            fg=self.BROWN,
            font=("Poppins", 17, "bold"),
        ).pack(pady=(18, 8))

        entries = {}
        for resource in ("Water", "Milk", "Coffee"):
            tk.Label(win, text=resource, bg=self.CARD, fg=self.TEXT, font=("Poppins", 11)).pack(pady=(7, 2))
            entry = tk.Entry(win, justify="center", font=("Poppins", 12))
            entry.insert(0, "0")
            entry.pack()
            entries[resource.lower()] = entry

        status = tk.Label(win, text="", bg=self.CARD, fg=self.DANGER, font=("Poppins", 10, "bold"))
        status.pack(pady=(8, 0))

        def refill():
            try:
                amounts = {
                    name: int(entry.get())
                    for name, entry in entries.items()
                }
                message = self.coffee_maker.refill(
                    amounts["water"], amounts["milk"], amounts["coffee"]
                )
            except ValueError as error:
                status.config(text=str(error))
                return

            self.update_dashboard()
            self.status_label.config(text=message, fg=self.SUCCESS)
            win.destroy()
            messagebox.showinfo("Success", message)

        self.make_button(win, "Refill", self.ACCENT, refill, 11, 15).pack(pady=14)

    def show_report(self):
        resources = self.coffee_maker.report()
        messagebox.showinfo(
            "Machine Report",
            (
                f"Water: {resources['water']} ml\n"
                f"Milk: {resources['milk']} ml\n"
                f"Coffee: {resources['coffee']} g\n"
                f"Profit: ${self.money_machine.get_profit():.2f}"
            ),
        )

    def run(self):
        self.root.mainloop()
