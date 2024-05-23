import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


class TicketBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.state("zoomed")
        self.root.title("Movie Ticket Booking")

        self.Seats = [str(i) for i in range(1, 21)]
        self.history = []
        self.Wallet = 1500000
        self.total_charge = 0

        self.setup_frames()
        self.show_frame(self.main_tab)

    def setup_frames(self):
        self.main_tab = tk.Frame(self.root, bg="beige")
        self.cinema_tab = tk.Frame(self.root, bg="grey")
        self.food_tab = tk.Frame(self.root, bg="grey")
        self.history_tab = tk.Frame(self.root, bg="beige")

        for frame in (self.main_tab, self.cinema_tab, self.food_tab, self.history_tab):
            frame.grid(row=0, column=0, sticky="nsew")

        self.setup_main_tab()
        self.setup_cinema_tab()
        self.setup_food_tab()
        self.setup_history_tab()

    def show_frame(self, frame):
        frame.tkraise()

    def setup_main_tab(self):
        tk.Label(self.main_tab, text="XXI", font=(
            'Arial', 24), bg="beige").pack(pady=20)

        content_frame = tk.Frame(self.main_tab, bg="beige")
        content_frame.pack(pady=20, padx=20)

        film_frame = tk.Frame(content_frame, bg="beige")
        film_frame.grid(row=0, column=0, sticky="nw")

        # Path absolut ke file gambar
        image_path = r"H:\coding\coba-dkp\film_image.png"

        try:
            self.film_image = Image.open(image_path)
            self.film_image = self.film_image.resize(
                (200, 250), Image.ANTIALIAS)
            self.film_image = ImageTk.PhotoImage(self.film_image)
            tk.Label(film_frame, image=self.film_image,
                     bg="beige").pack(padx=10, pady=10)
        except FileNotFoundError:
            print(f"File {image_path} not found.")

        tk.Button(film_frame, text="Book", command=lambda: self.show_frame(
            self.cinema_tab)).pack(padx=10, pady=10)

        food_frame = tk.Frame(content_frame, bg="beige")
        food_frame.grid(row=0, column=1, sticky="ne", padx=20)

        tk.Label(food_frame, text="Food and drink", bg="beige").pack(pady=5)
        tk.Button(food_frame, text="Order", command=lambda: self.show_frame(
            self.food_tab)).pack(pady=10)

        tk.Button(self.main_tab, text="Cart", command=lambda: self.show_frame(
            self.history_tab)).pack(pady=10)

    def setup_cinema_tab(self):
        tk.Label(self.cinema_tab, text="Cinema", font=(
            'Arial', 24), bg="grey").pack(pady=20)
        self.seat_buttons = []
        self.selected_seats = []
        seat_frame = tk.Frame(self.cinema_tab, bg="grey")
        seat_frame.pack(pady=10)

        for seat in self.Seats:
            btn = tk.Button(seat_frame, text=seat, width=4,
                            command=lambda s=seat: self.select_seat(s))
            btn.grid(row=(int(seat) - 1) // 5, column=(int(seat) - 1) %
                     5, padx=5, pady=5)
            self.seat_buttons.append(btn)

        tk.Button(self.cinema_tab, text="Add",
                  command=self.buy_ticket).pack(pady=10)
        tk.Button(self.cinema_tab, text="Back",
                  command=lambda: self.show_frame(self.main_tab)).pack(pady=10)

    def setup_food_tab(self):
        tk.Label(self.food_tab, text="Food", font=(
            'Arial', 24), bg="grey").pack(pady=20)

        self.food_items = [("Popcorn", 33000), ("Fries", 55000),
                           ("Donut", 15000), ("Milk tea", 20000), ("Lemon tea", 20000)]
        self.food_vars = []

        for food, price in self.food_items:
            frame = tk.Frame(self.food_tab, bg="grey")
            frame.pack(pady=5)

            tk.Label(frame, text=food, bg="grey").pack(side='left', padx=10)
            var = tk.IntVar()
            self.food_vars.append((var, price))
            tk.Spinbox(frame, from_=0, to=10, textvariable=var,
                       width=5).pack(side='left', padx=10)

        tk.Button(self.food_tab, text="Add",
                  command=self.buy_food).pack(pady=10)
        tk.Button(self.food_tab, text="Back",
                  command=lambda: self.show_frame(self.main_tab)).pack(pady=10)

    def setup_history_tab(self):
        tk.Label(self.history_tab, text="History", font=(
            'Arial', 24), bg="beige").pack(pady=20)
        self.history_listbox = tk.Listbox(self.history_tab)
        self.history_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        tk.Button(self.history_tab, text="Pay", command=self.pay).pack(pady=10)
        tk.Button(self.history_tab, text="Back",
                  command=lambda: self.show_frame(self.main_tab)).pack(pady=10)

    def select_seat(self, seat):
        if seat in self.selected_seats:
            self.selected_seats.remove(seat)
            for btn in self.seat_buttons:
                if btn.cget("text") == seat:
                    btn.config(bg='SystemButtonFace')
        else:
            self.selected_seats.append(seat)
            for btn in self.seat_buttons:
                if btn.cget("text") == seat:
                    btn.config(bg='lightgreen')

    def buy_ticket(self):
        if not self.selected_seats:
            messagebox.showinfo("Warning", "You have not chosen a ticket.")
        else:
            count = len(self.selected_seats)
            charge = count * 50000
            if self.Wallet >= charge:
                self.Wallet -= charge
                messagebox.showinfo(
                    "Notice", f"That will be Rp{charge} for {count} ticket(s).")
                self.history.append(["Movie Ticket", count, charge])
                self.update_history()
                self.selected_seats.clear()
                for btn in self.seat_buttons:
                    btn.config(bg='SystemButtonFace')
                self.show_frame(self.main_tab)
            else:
                messagebox.showinfo(
                    "Warning", "Insufficient balance to buy tickets.")

    def buy_food(self):
        total_cost = 0
        for var, price in self.food_vars:
            count = var.get()
            if count > 0:
                total_cost += count * price
                self.history.append(["Food", count, count * price])
                var.set(0)  # Set nilai var menjadi 0

        if total_cost > 0:
            if self.Wallet >= total_cost:
                self.Wallet -= total_cost
                messagebox.showinfo(
                    "Notice", f"That will be Rp{total_cost} for your food order.")
                self.update_history()
                self.show_frame(self.main_tab)
            else:
                messagebox.showinfo(
                    "Warning", "Insufficient balance to buy food.")
        else:
            messagebox.showinfo("Warning", "You have not added anything.")

    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            self.history_listbox.insert(
                tk.END, f"{item[0]}: {item[1]} - Rp{item[2]}")

    def pay(self):
        total_charge = sum(item[2] for item in self.history)
        if total_charge == 0:
            messagebox.showinfo("Warning", "Cart is empty.")
        elif self.Wallet >= total_charge:
            self.Wallet -= total_charge
            messagebox.showinfo(
                "Notice", f"You have paid Rp{total_charge}.\nYour balance is now Rp{self.Wallet}")
            self.history.clear()
            self.update_history()
            self.show_frame(self.main_tab)
        else:
            messagebox.showinfo(
                "Warning", "Your balance is not enough, please remove some items.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TicketBookingApp(root)
    root.mainloop()
