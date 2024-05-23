import tkinter as tk
from tkinter import messagebox


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
        tk.Label(self.main_tab, text="Bioskop", font=(
            'Arial', 24), bg="beige").pack(pady=20)

        self.name_var = tk.StringVar()
        tk.Label(self.main_tab, text="Enter your name:",
                 bg="beige").pack(pady=5)
        tk.Entry(self.main_tab, textvariable=self.name_var).pack(pady=5)

        self.wallet_label = tk.Label(
            self.main_tab, text=f"Wallet Balance: Rp{self.Wallet}", bg="beige")
        self.wallet_label.pack(pady=5)

        tk.Button(self.main_tab, text="Buy Ticket",
                  command=lambda: self.show_frame(self.cinema_tab)).pack(pady=10)
        tk.Button(self.main_tab, text="Buy Food",
                  command=lambda: self.show_frame(self.food_tab)).pack(pady=10)
        tk.Button(self.main_tab, text="View History",
                  command=lambda: self.show_frame(self.history_tab)).pack(pady=10)
        tk.Button(self.main_tab, text="Exit",
                  command=self.root.quit).pack(pady=10)

    def setup_cinema_tab(self):
        tk.Label(self.cinema_tab, text="Select Your Seats",
                 font=('Arial', 24), bg="grey").pack(pady=20)
        self.seat_buttons = []
        self.selected_seats = []
        seat_frame = tk.Frame(self.cinema_tab, bg="grey")
        seat_frame.pack(pady=10)

        for seat in self.Seats:
            btn = tk.Button(seat_frame, text=seat, width=4,
                            command=lambda s=seat: self.select_seat(s))
            btn.grid(row=(int(seat)-1) // 5, column=(int(seat)-1) %
                     5, padx=5, pady=5)
            self.seat_buttons.append(btn)

        tk.Button(self.cinema_tab, text="Buy Ticket",
                  command=self.buy_ticket).pack(pady=10)
        tk.Button(self.cinema_tab, text="Back",
                  command=lambda: self.show_frame(self.main_tab)).pack(pady=10)

    def setup_food_tab(self):
        tk.Label(self.food_tab, text="Buy Food", font=(
            'Arial', 24), bg="grey").pack(pady=20)

        self.pop_count = tk.IntVar()
        self.dog_count = tk.IntVar()
        self.fries_count = tk.IntVar()
        self.donut_count = tk.IntVar()
        self.tea_count = tk.IntVar()
        self.boba_count = tk.IntVar()

        self.add_food_option("Popcorn", 33000, self.pop_count)
        self.add_food_option("Hot Dog", 50000, self.dog_count)
        self.add_food_option("Fries", 55000, self.fries_count)
        self.add_food_option("Donut", 15000, self.donut_count)
        self.add_food_option("Lemon Tea", 33000, self.tea_count)
        self.add_food_option("Boba", 50000, self.boba_count)

        tk.Button(self.food_tab, text="Buy Food",
                  command=self.buy_food).pack(pady=10)
        tk.Button(self.food_tab, text="Back",
                  command=lambda: self.show_frame(self.main_tab)).pack(pady=10)

    def add_food_option(self, name, price, var):
        frame = tk.Frame(self.food_tab, bg="grey")
        frame.pack(pady=5)
        tk.Label(frame, text=f"{name} (Rp{price})",
                 bg="grey").pack(side='left', padx=10)
        tk.Spinbox(frame, from_=0, to=10, textvariable=var,
                   width=5).pack(side='left', padx=10)

    def setup_history_tab(self):
        tk.Label(self.history_tab, text="Purchase History",
                 font=('Arial', 24), bg="beige").pack(pady=20)
        self.history_listbox = tk.Listbox(self.history_tab)
        self.history_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
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
        elif not self.name_var.get():
            messagebox.showinfo("Warning", "Please enter your name.")
        else:
            count = len(self.selected_seats)
            charge = count * 50000
            if self.Wallet >= charge:
                self.Wallet -= charge
                name = self.name_var.get()
                messagebox.showinfo(
                    "Notice", f"{name}, that will be Rp{charge} for {count} ticket(s).")
                self.history.append(
                    [f"Movie Ticket (Purchased by {name})", count, charge])
                self.update_history()
                self.selected_seats.clear()
                for btn in self.seat_buttons:
                    btn.config(bg='SystemButtonFace')
                self.update_wallet()
                self.show_frame(self.main_tab)
            else:
                messagebox.showinfo(
                    "Warning", "Insufficient balance to buy tickets.")

    def buy_food(self):
        if not self.name_var.get():
            messagebox.showinfo("Warning", "Please enter your name.")
            return

        food = []
        total_cost = 0
        total_cost += self.add_food_to_history(
            "Popcorn", 33000, self.pop_count, food)
        total_cost += self.add_food_to_history(
            "Hot Dog", 50000, self.dog_count, food)
        total_cost += self.add_food_to_history("Fries",
                                               55000, self.fries_count, food)
        total_cost += self.add_food_to_history("Donut",
                                               15000, self.donut_count, food)
        total_cost += self.add_food_to_history(
            "Lemon Tea", 33000, self.tea_count, food)
        total_cost += self.add_food_to_history("Boba",
                                               50000, self.boba_count, food)

        if food:
            if self.Wallet >= total_cost:
                self.Wallet -= total_cost
                name = self.name_var.get()
                messagebox.showinfo(
                    "Notice", f"{name}, your food order:\n" + "\n".join(food))
                self.update_history()
                self.update_wallet()
                self.show_frame(self.main_tab)
            else:
                messagebox.showinfo(
                    "Warning", "Insufficient balance to buy food.")
        else:
            messagebox.showinfo("Warning", "You have not added anything.")

    def add_food_to_history(self, name, price, count_var, food_list):
        count = count_var.get()
        if count > 0:
            charge = count * price
            food_list.append(f"Rp{charge} for {count} {name}(s).")
            self.history.append([name, count, charge])
            return charge
        return 0

    def update_history(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            self.history_listbox.insert(
                tk.END, f"{item[0]}: {item[1]} - Rp{item[2]}")

    def update_wallet(self):
        self.wallet_label.config(text=f"Wallet Balance: Rp{self.Wallet}")

    def total(self):
        self.total_charge = sum(item[2] for item in self.history)
        return self.total_charge

    def pay(self):
        total_charge = self.total()
        if total_charge == 0:
            messagebox.showinfo("Warning", "Cart is empty.")
        else:
            if self.Wallet >= total_charge:
                self.Wallet -= total_charge
                messagebox.showinfo(
                    "Notice", f"You have paid Rp{total_charge}.\nYour balance is now Rp{self.Wallet}")
                self.history.clear()
                self.update_history()
                self.update_wallet()
                self.show_frame(self.main_tab)
            else:
                messagebox.showinfo(
                    "Warning", "Your balance is not enough, please remove some items.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TicketBookingApp(root)
    root.mainloop()
