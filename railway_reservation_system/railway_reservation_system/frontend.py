import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

# Base URL for your Django API
BASE_URL = "http://127.0.0.1:8000/api/"

class RailwayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Railway Reservation System")
        self.root.geometry("800x600")

        # Main Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # Tabs
        self.train_tab = ttk.Frame(self.notebook)
        self.schedule_tab = ttk.Frame(self.notebook)
        self.booking_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.train_tab, text="Trains & Stations")
        self.notebook.add(self.schedule_tab, text="Schedules & Availability")
        self.notebook.add(self.booking_tab, text="Booking")

        # Initialize UI for each tab
        self.setup_train_tab()
        self.setup_schedule_tab()
        self.setup_booking_tab()

    # --- Train & Station Tab (Point 2) ---
    def setup_train_tab(self):
        # Train Section
        tk.Label(self.train_tab, text="Train Information", font=("Arial", 14)).pack(pady=5)

        self.train_search_var = tk.StringVar()
        tk.Label(self.train_tab, text="Search Train (Name/Code):").pack()
        tk.Entry(self.train_tab, textvariable=self.train_search_var).pack()
        tk.Button(self.train_tab, text="Search Trains", command=self.search_trains).pack(pady=5)

        self.train_tree = ttk.Treeview(self.train_tab, columns=("Name", "Code"), show="headings")
        self.train_tree.heading("Name", text="Train Name")
        self.train_tree.heading("Code", text="Train Code")
        self.train_tree.pack(fill="both", expand=True)

        # Station Section
        tk.Label(self.train_tab, text="Station Information", font=("Arial", 14)).pack(pady=5)

        self.station_search_var = tk.StringVar()
        tk.Label(self.train_tab, text="Search Station (Name/Code):").pack()
        tk.Entry(self.train_tab, textvariable=self.station_search_var).pack()
        tk.Button(self.train_tab, text="Search Stations", command=self.search_stations).pack(pady=5)

        self.station_universitaria_tree = ttk.Treeview(self.train_tab, columns=("Name", "Code"), show="headings")
        self.train_tree.heading("Name", text="Station Name")
        self.train_tree.heading("Code", text="Station Code")
        self.train_tree.pack(fill="both", expand=True)

    def search_trains(self):
        query = self.train_search_var.get()
        response = requests.get(f"{BASE_URL}trains/?search={query}")
        if response.status_code == 200:
            trains = response.json()
            self.train_tree.delete(*self.train_tree.get_children())
            for train in trains:
                self.train_tree.insert("", "end", values=(train["train_name"], train["train_code"]))
        else:
            messagebox.showerror("Error", "Failed to fetch trains")

    def search_stations(self):
        query = self.station_search_var.get()
        response = requests.get(f"{BASE_URL}stations/?search={query}")
        if response.status_code == 200:
            stations = response.json()
            self.train_tree.delete(*self.train_tree.get_children())
            for station in stations:
                self.train_tree.insert("", "end", values=(station["station_name"], station["station_code"]))
        else:
            messagebox.showerror("Error", "Failed to fetch stations")

    # --- Schedule & Availability Tab (Point 3) ---
    def setup_schedule_tab(self):
        tk.Label(self.schedule_tab, text="Search Schedules", font=("Arial", 14)).pack(pady=5)

        # Source and Destination
        tk.Label(self.schedule_tab, text="Source Station Code:").pack()
        self.source_var = tk.StringVar()
        tk.Entry(self.schedule_tab, textvariable=self.source_var).pack()

        tk.Label(self.schedule_tab, text="Destination Station Code:").pack()
        self.dest_var = tk.StringVar()
        tk.Entry(self.schedule_tab, textvariable=self.dest_var).pack()

        tk.Label(self.schedule_tab, text="Journey Date (YYYY-MM-DD):").pack()
        self.date_var = tk.StringVar()
        tk.Entry(self.schedule_tab, textvariable=self.date_var).pack()

        tk.Button(self.schedule_tab, text="Search Schedules", command=self.search_schedules).pack(pady=5)

        self.schedule_tree = ttk.Treeview(self.schedule_tab, columns=("Train", "Departure", "Arrival"), show="headings")
        self.schedule_tree.heading("Train", text="Train")
        self.schedule_tree.heading("Departure", text="Departure Time")
        self.schedule_tree.heading("Arrival", text="Arrival Time")
        self.schedule_tree.pack(fill="both", expand=True)

        # Availability
        tk.Button(self.schedule_tab, text="Check Availability", command=self.check_availability).pack(pady=5)
        self.availability_label = tk.Label(self.schedule_tab, text="")
        self.availability_label.pack()

    def search_schedules(self):
        source = self.source_var.get()
        dest = self.dest_var.get()
        response = requests.get(f"{BASE_URL}schedules/?source={source}&destination={dest}")
        if response.status_code == 200:
            schedules = response.json()
            self.schedule_tree.delete(*self.schedule_tree.get_children())
            for schedule in schedules:
                train = schedule["train_detail"]["train_name"]
                self.schedule_tree.insert("", "end", values=(train, schedule["departure_time"], schedule["arrival_time"]))
        else:
            messagebox.showerror("Error", "Failed to fetch schedules")

    def check_availability(self):
        selected = self.schedule_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a schedule first")
            return

        index = self.schedule_tree.index(selected[0])
        date = self.date_var.get()
        response = requests.get(f"{BASE_URL}schedules/{index + 1}/availability/?date={date}")
        if response.status_code == 200:
            availabilities = response.json()
            if availabilities:
                text = "\n".join([f"{a['coach_type']}: {a['available_seats']} seats" for a in availabilities])
                self.availability_label.config(text=f"Availability:\n{text}")
            else:
                self.availability_label.config(text="No availability for this date")
        else:
            messagebox.showerror("Error", "Failed to check availability")

    # --- Booking Tab (Point 4) ---
    def setup_booking_tab(self):
        tk.Label(self.booking_tab, text="Book a Ticket", font=("Arial", 14)).pack(pady=5)

        tk.Label(self.booking_tab, text="User ID:").pack()
        self.user_id_var = tk.StringVar()
        tk.Entry(self.booking_tab, textvariable=self.user_id_var).pack()

        # Schedule dropdown instead of text field
        tk.Label(self.booking_tab, text="Select Schedule:").pack()
        self.schedule_var = tk.StringVar()

        # Create Combobox
        self.schedule_combobox = ttk.Combobox(self.booking_tab, textvariable=self.schedule_var)
        self.schedule_combobox.pack()
        
        # Set placeholder text
        self.schedule_combobox.set("Select a schedule...")
        
        # Fetch schedules and populate the dropdown
        self.populate_schedule_dropdown()

        tk.Label(self.booking_tab, text="Journey Date (YYYY-MM-DD):").pack()
        self.booking_date_var = tk.StringVar()
        tk.Entry(self.booking_tab, textvariable=self.booking_date_var).pack()

        tk.Label(self.booking_tab, text="Passenger Name:").pack()
        self.passenger_name_var = tk.StringVar()
        tk.Entry(self.booking_tab, textvariable=self.passenger_name_var).pack()

        # Number of Tickets
        tk.Label(self.booking_tab, text="Number of Tickets").pack()
        self.no_of_tickets_var = tk.IntVar(value=1)
        tk.Entry(self.booking_tab, textvariable=self.no_of_tickets_var).pack()

        # Calculate Fare button
        tk.Button(self.booking_tab, text="Calculate Fare", command=self.calculate_fare).pack(pady=5)

        # Display Ticket Fare
        tk.Label(self.booking_tab, text="Ticket Fare:").pack()
        self.ticket_fare_var = tk.StringVar()
        self.ticket_fare_var.set("₹0.00")
        self.fare_label = tk.Label(self.booking_tab, textvariable=self.ticket_fare_var, font=("Arial", 12, "bold"))
        self.fare_label.pack()

        tk.Button(self.booking_tab, text="Book Ticket", command=self.book_ticket).pack(pady=5)

        self.booking_result = tk.Label(self.booking_tab, text="")
        self.booking_result.pack()

        # View Bookings
        tk.Button(self.booking_tab, text="View My Bookings", command=self.view_bookings).pack(pady=5)
        self.booking_tree = ttk.Treeview(self.booking_tab, columns=("PNR", "Date", "Status"), show="headings")
        self.booking_tree.heading("PNR", text="PNR")
        self.booking_tree.heading("Date", text="Journey Date")
        self.booking_tree.heading("Status", text="Status")
        self.booking_tree.pack(fill="both", expand=True)

        tk.Button(self.booking_tab, text="Cancel Booking", command=self.cancel_booking).pack(pady=5)

    def populate_schedule_dropdown(self):
        try:
            # Replace this with actual API call to your backend
            response = requests.get(f'{BASE_URL}schedules/')
            schedules = response.json()
            
            # Format the display text for each schedule
            schedule_options = []
            for schedule in schedules:
                display_text = f"{schedule['train_detail']['train_name']} ({schedule['train_detail']['train_code']}) - " \
                            f"{schedule['source_detail']['station_code']} to {schedule['destination_detail']['station_code']} - " \
                            f"Dep: {schedule['departure_time']}"
                schedule_options.append((schedule['id'], display_text))
            
            # Store the mapping between display text and schedule IDs
            self.schedule_options = schedule_options
            
            # Set the values for the combobox (only display text)
            self.schedule_combobox['values'] = [display for (id, display) in schedule_options]
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load schedules: {str(e)}")
            self.schedule_combobox['values'] = []

    def book_ticket(self):
        try:
            # Get schedule ID
            selected_display = self.schedule_var.get()
            ticket_fare = self.ticket_fare_var.get()
            ticket_fare = f"{ticket_fare[1:]}"
            schedule_id = next((id for id, display in self.schedule_options 
                            if display == selected_display), None)
            
            if not schedule_id:
                messagebox.showerror("Error", "Please select a valid schedule")
                return

            # Prepare data with strict validation
            data = {
                "pnr": f"PNR{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "user": str(self.user_id_var.get()),  # Match CharField requirement
                "schedule": schedule_id,
                "journey_date": self.booking_date_var.get(),  # Must be YYYY-MM-DD
                "total_fare": ticket_fare,  # String for DecimalField
                "status": "CNF"
            }

            # First validate the booking data
            booking_response = requests.post(
                f"{BASE_URL}bookings/",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if booking_response.status_code != 201:
                error = booking_response.json()
                messagebox.showerror("Booking Failed", 
                                f"Server error: {error.get('detail', error)}")
                return

            booking = booking_response.json()

            # Then create passenger
            passenger_data = {
                "name": self.passenger_name_var.get(),
                "age": 30,  # Consider making this a user input
                "gender": "M",  # Consider making this a user input
                "phone": "1234567890"  # Consider making this a user input
            }

            passenger_response = requests.post(
                f"{BASE_URL}passengers/",
                json=passenger_data
            )

            if passenger_response.status_code != 201:
                messagebox.showerror("Error", "Failed to create passenger")
                return

            # Finally create ticket
            ticket_response = requests.post(
                f"{BASE_URL}tickets/",
                json={
                    "booking": booking["id"],
                    "passenger": passenger_response.json()["id"]
                }
            )

            if ticket_response.status_code == 201:
                self.booking_result.config(
                    text=f"Booking successful! PNR: {booking.get('pnr', '')}",
                    fg="green"
                )
                self.view_bookings()

            else:
                messagebox.showerror("Error", "Failed to create ticket")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Could not connect to server: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")

    def view_bookings(self):
        user_id = self.user_id_var.get()
        response = requests.get(f"{BASE_URL}bookings/?user={user_id}")
        if response.status_code == 200:
            bookings = response.json()
            self.booking_tree.delete(*self.booking_tree.get_children())
            for booking in bookings:
                self.booking_tree.insert("", "end", values=(booking["pnr"], booking["journey_date"], booking["status"]))
        else:
            messagebox.showerror("Error", "Failed to fetch bookings")

    def cancel_booking(self):
        selected = self.booking_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a booking to cancel")
            return

        index = self.booking_tree.index(selected[0])
        response = requests.post(f"{BASE_URL}bookings/{index + 1}/cancel/")
        if response.status_code == 200:
            messagebox.showinfo("Success", "Booking cancelled successfully")
            self.view_bookings()
        else:
            messagebox.showerror("Error", "Failed to cancel booking")
    
    def calculate_fare(self):
        """Calculate and display the fare when the button is pressed"""
        try:
            selected_display = self.schedule_var.get()
            if not selected_display or selected_display == "Select a schedule...":
                messagebox.showwarning("Warning", "Please select a schedule first")
                return

            # Find the corresponding schedule ID from the display text
            schedule_id = None
            for id, display in self.schedule_options:
                if display == selected_display:
                    schedule_id = id
                    break

            if schedule_id is None:
                messagebox.showerror("Error", "Invalid schedule selection")
                return

            # Get number of tickets
            try:
                num_tickets = self.no_of_tickets_var.get()
                if num_tickets < 1:
                    messagebox.showwarning("Warning", "Number of tickets must be at least 1")
                    self.no_of_tickets_var.set(1)
                    return
            except:
                messagebox.showwarning("Warning", "Please enter a valid number of tickets")
                return

            # Get the schedule details from API
            response = requests.get(f'{BASE_URL}schedules/{schedule_id}/')
            if response.status_code == 200:
                schedule = response.json()
                fare = float(schedule['fare'])
                total_fare = fare * num_tickets
                self.ticket_fare_var.set(f"₹{total_fare:.2f}")
            else:
                messagebox.showerror("Error", "Failed to fetch fare information")
                self.ticket_fare_var.set("₹0.00")

        except Exception as e:
            print(f"Error calculating fare: {e}")
            messagebox.showerror("Error", "An error occurred while calculating fare")
            self.ticket_fare_var.set("₹0.00")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = RailwayApp(root)
    root.mainloop()