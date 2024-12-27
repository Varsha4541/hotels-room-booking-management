import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar

class HotelBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Booking System")
        self.guest_data = {}
        self.bookings = {}
        self.staff_credentials = {"admin": "password123", "sathvik": "12345"}
        self.current_accommodation_type = None

        self.login_page()

    def login_page(self):
        self.clear_window()
        tk.Label(self.root, text="Staff Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username:").pack()
        self.username_var = tk.Entry(self.root)
        self.username_var.pack(pady=5)

        tk.Label(self.root, text="Password:").pack()
        self.password_var = tk.Entry(self.root, show="*")
        self.password_var.pack(pady=5)

        tk.Button(
            self.root, text="Login", command=self.authenticate_staff
        ).pack(pady=10)

    def authenticate_staff(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if self.staff_credentials.get(username) == password:
            self.staff_menu(username)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def staff_menu(self, username):
        self.clear_window()
        tk.Label(self.root, text="Hotel Management System", font=("Arial", 16)).pack(pady=10)

        if username == "sathvik":
            tk.Button(self.root, text="Add Staff", command=self.add_staff).pack(pady=5)

        tk.Button(self.root, text="Add Booking", command=self.step1_accommodation_selection).pack(pady=5)
        tk.Button(self.root, text="Cancel Booking", command=self.cancel_booking).pack(pady=5)
        tk.Button(self.root, text="Checkout", command=self.step6_checkout_verification).pack(pady=5)
        tk.Button(self.root, text="Change Booking Dates", command=self.change_booking_dates).pack(pady=5)
        tk.Button(self.root, text="View Booked Rooms", command=self.view_booked_rooms).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_page).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

    def add_staff(self):
        self.clear_window()
        tk.Label(self.root, text="Add New Staff", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username:").pack()
        self.new_staff_username = tk.Entry(self.root)
        self.new_staff_username.pack(pady=5)

        tk.Label(self.root, text="Password:").pack()
        self.new_staff_password = tk.Entry(self.root, show="*")
        self.new_staff_password.pack(pady=5)

        tk.Button(
            self.root, text="Add", command=self.save_new_staff
        ).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.staff_menu("sathvik")).pack(pady=5)

    def save_new_staff(self):
        username = self.new_staff_username.get()
        password = self.new_staff_password.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please provide both username and password.")
            return

        if username in self.staff_credentials:
            messagebox.showwarning("Input Error", "Username already exists.")
            return

        self.staff_credentials[username] = password
        messagebox.showinfo("Success", "New staff added successfully.")
        self.staff_menu("sathvik")

    def cancel_booking(self):
        self.clear_window()
        tk.Label(self.root, text="Cancel Booking", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Room Number:").pack()
        self.cancel_room_var = tk.Entry(self.root)
        self.cancel_room_var.pack(pady=5)

        tk.Button(self.root, text="Cancel", command=self.process_cancel_booking).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.staff_menu("admin")).pack(pady=5)

    def process_cancel_booking(self):
        room_number = self.cancel_room_var.get()

        if room_number in self.bookings:
            del self.bookings[room_number]
            messagebox.showinfo("Success", f"Booking for Room {room_number} has been cancelled.")
        else:
            messagebox.showwarning("Error", "No booking found for the specified room number.")
        self.staff_menu("admin")

    def view_booked_rooms(self):
        self.clear_window()
        tk.Label(self.root, text="Booked Rooms", font=("Arial", 16)).pack(pady=10)

        if not self.bookings:
            tk.Label(self.root, text="No rooms are currently booked.").pack(pady=10)
        else:
            for room, details in self.bookings.items():
                room_info = (
                    f"Room: {room}\n"
                    f"Name: {details['guest']['name']}\n"
                    f"Phone: {details['guest']['phone']}\n"
                    f"Address: {details['guest']['address']}\n"
                    f"Check-in: {details['checkin_date']}\n"
                    f"Check-out: {details['checkout_date']}\n"
                )
                tk.Label(self.root, text=room_info, justify="left", borderwidth=1, relief="solid", pady=5).pack(pady=5)

        tk.Button(self.root, text="Back", command=lambda: self.staff_menu("admin")).pack(pady=5)

    def change_booking_dates(self):
        self.clear_window()
        tk.Label(self.root, text="Change Booking Dates", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Room Number:").pack()
        self.change_room_var = tk.Entry(self.root)
        self.change_room_var.pack(pady=5)

        tk.Button(self.root, text="Next", command=self.select_new_dates).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.staff_menu("admin")).pack(pady=5)

    def select_new_dates(self):
        room_number = self.change_room_var.get()

        if room_number not in self.bookings:
            messagebox.showwarning("Error", "No booking found for the specified room number.")
            return

        self.clear_window()
        tk.Label(self.root, text="Select New Dates", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Check-in Date:").pack()
        self.new_checkin_calendar = Calendar(self.root, selectmode="day")
        self.new_checkin_calendar.pack(pady=5)

        tk.Label(self.root, text="Check-out Date:").pack()
        self.new_checkout_calendar = Calendar(self.root, selectmode="day")
        self.new_checkout_calendar.pack(pady=5)

        tk.Button(self.root, text="Update", command=lambda: self.update_booking_dates(room_number)).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.staff_menu("admin")).pack(pady=5)

    def update_booking_dates(self, room_number):
        new_checkin_date = self.new_checkin_calendar.get_date()
        new_checkout_date = self.new_checkout_calendar.get_date()

        if new_checkin_date >= new_checkout_date:
            messagebox.showwarning("Input Error", "Check-out date must be after check-in date.")
            return

        self.bookings[room_number]["checkin_date"] = new_checkin_date
        self.bookings[room_number]["checkout_date"] = new_checkout_date
        messagebox.showinfo("Success", "Booking dates updated successfully.")
        self.staff_menu("admin")

    def step1_accommodation_selection(self):
        self.clear_window()
        tk.Label(self.root, text="Select Accommodation Type", font=("Arial", 16)).pack(pady=10)

        self.accommodation_var = tk.StringVar()
        ttk.Combobox(
            self.root,
            textvariable=self.accommodation_var,
            values=["Single", "Double", "Suite"],
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Next",
            command=self.step2_room_selection,
        ).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.staff_menu("admin")).pack(pady=5)

    def step2_room_selection(self):
        if not self.accommodation_var.get():
            messagebox.showwarning("Input Error", "Please select an accommodation type.")
            return

        self.current_accommodation_type = self.accommodation_var.get()
        self.clear_window()

        tk.Label(
            self.root, text=f"Select Room Number for {self.current_accommodation_type}", font=("Arial", 16)
        ).pack(pady=10)

        # Filter room numbers based on accommodation type
        room_options = self.get_rooms_by_accommodation(self.current_accommodation_type)
        self.room_var = tk.StringVar()
        ttk.Combobox(self.root, textvariable=self.room_var, values=room_options).pack(pady=5)

        tk.Label(self.root, text="Enter Room Price (INR):").pack()
        self.room_price_var = tk.Entry(self.root)
        self.room_price_var.pack(pady=5)

        tk.Button(self.root, text="Next", command=self.step3_date_selection).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.step1_accommodation_selection).pack(pady=5)

    def step3_date_selection(self):
        if not self.room_var.get():
            messagebox.showwarning("Input Error", "Please select a room number.")
            return

        if not self.room_price_var.get().isdigit():
            messagebox.showwarning("Input Error", "Please enter a valid room price.")
            return

        self.room_price = int(self.room_price_var.get())
        self.clear_window()
        tk.Label(self.root, text="Select Check-in and Check-out Dates", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Check-in Date:").pack()
        self.checkin_calendar = Calendar(self.root, selectmode="day")
        self.checkin_calendar.pack(pady=5)

        tk.Label(self.root, text="Check-out Date:").pack()
        self.checkout_calendar = Calendar(self.root, selectmode="day")
        self.checkout_calendar.pack(pady=5)

        tk.Button(self.root, text="Next", command=self.step4_guest_details).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.step2_room_selection).pack(pady=5)

    def step4_guest_details(self):
        checkin_date = self.checkin_calendar.get_date()
        checkout_date = self.checkout_calendar.get_date()

        if not checkin_date or not checkout_date:
            messagebox.showwarning("Input Error", "Please select both check-in and check-out dates.")
            return

        if checkin_date >= checkout_date:
            messagebox.showwarning("Input Error", "Check-out date must be after check-in date.")
            return

        self.num_days = (self.checkout_calendar.selection_get() - self.checkin_calendar.selection_get()).days

        self.clear_window()
        tk.Label(self.root, text="Enter Guest Details", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Name:").pack()
        self.guest_name_var = tk.Entry(self.root)
        self.guest_name_var.pack(pady=5)

        tk.Label(self.root, text="Phone Number:").pack()
        self.guest_phone_var = tk.Entry(self.root)
        self.guest_phone_var.pack(pady=5)

        tk.Label(self.root, text="Address:").pack()
        self.guest_address_var = tk.Entry(self.root)
        self.guest_address_var.pack(pady=5)

        tk.Button(self.root, text="Next", command=self.step5_payment_and_deposit).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.step3_date_selection).pack(pady=5)

    def step5_payment_and_deposit(self):
        name = self.guest_name_var.get()
        phone = self.guest_phone_var.get()
        address = self.guest_address_var.get()

        if not name or not phone or not address:
            messagebox.showwarning("Input Error", "Please fill out all guest details.")
            return

        self.guest_data = {"name": name, "phone": phone, "address": address}

        # Calculate payment details
        total_price = self.room_price * self.num_days
        deposit = total_price * 0.2

        self.bookings[self.room_var.get()] = {
            "accommodation_type": self.current_accommodation_type,
            "guest": self.guest_data,
            "checkin_date": self.checkin_calendar.get_date(),
            "checkout_date": self.checkout_calendar.get_date(),
            "num_days": self.num_days,
            "deposit": deposit,
            "total_price": total_price,
        }

        self.clear_window()
        tk.Label(self.root, text="Booking Summary", font=("Arial", 16)).pack(pady=10)

        summary = (
            f"Room: {self.room_var.get()}\n"
            f"Accommodation: {self.current_accommodation_type}\n"
            f"Check-in: {self.checkin_calendar.get_date()}\n"
            f"Check-out: {self.checkout_calendar.get_date()}\n"
            f"Days: {self.num_days}\n"
            f"Total Price: ₹{total_price:.2f}\n"
            f"Deposit: ₹{deposit:.2f}"
        )
        tk.Label(self.root, text=summary, justify="left").pack(pady=10)

        tk.Button(self.root, text="Finish", command=lambda: self.staff_menu("admin")).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.step4_guest_details).pack(pady=5)

    def step6_checkout_verification(self):
        self.clear_window()
        tk.Label(self.root, text="Verify Guest for Checkout", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Name:").pack()
        self.checkout_name_var = tk.Entry(self.root)
        self.checkout_name_var.pack(pady=5)

        tk.Label(self.root, text="Phone Number:").pack()
        self.checkout_phone_var = tk.Entry(self.root)
        self.checkout_phone_var.pack(pady=5)

        tk.Button(self.root, text="Verify", command=self.handle_checkout).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.staff_menu("admin")).pack(pady=5)

    def handle_checkout(self):
        name = self.checkout_name_var.get()
        phone = self.checkout_phone_var.get()

        for room, details in self.bookings.items():
            if details["guest"]["name"] == name and details["guest"]["phone"] == phone:
                refund = details["deposit"]
                messagebox.showinfo(
                    "Checkout Successful",
                    f"Guest checked out from Room {room}. Refund: ₹{refund:.2f}"
                )
                del self.bookings[room]
                self.staff_menu("admin")
                return

        messagebox.showerror("Error", "Guest details do not match any booking.")

    def get_rooms_by_accommodation(self, accommodation_type):
        if accommodation_type == "Single":
            return [f"Single-{i}" for i in range(1, 51)]
        elif accommodation_type == "Double":
            return [f"Double-{i}" for i in range(1, 51)]
        elif accommodation_type == "Suite":
            return [f"Suite-{i}" for i in range(1, 51)]

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelBookingApp(root)
    root.mainloop()
