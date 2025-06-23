import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from flight import Flight
from planner import Planner

class FlightPlannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Route Planner")
        self.root.geometry("800x600")
        
        # Initialize with sample data
        self.flights = [
            Flight(0, 0, 0, 1, 30, 50),
            Flight(1, 0, 0, 3, 80, 200),
            Flight(2, 1, 40, 2, 60, 20),
            Flight(3, 1, 50, 2, 100, 120),
            Flight(4, 2, 120, 4, 200, 100),
            Flight(5, 3, 100, 4, 150, 500),
            Flight(6, 3, 100, 4, 250, 300)
        ]
        
        self.setup_ui()
        self.refresh_flight_list()
    
    def setup_ui(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Flight Management Tab
        self.flight_frame = ttk.Frame(notebook)
        notebook.add(self.flight_frame, text="Manage Flights")
        self.setup_flight_tab()
        
        # Route Search Tab
        self.search_frame = ttk.Frame(notebook)
        notebook.add(self.search_frame, text="Find Routes")
        self.setup_search_tab()
        
        # Results Tab
        self.results_frame = ttk.Frame(notebook)
        notebook.add(self.results_frame, text="Results")
        self.setup_results_tab()
    
    def setup_flight_tab(self):
        # Add flight section
        add_frame = ttk.LabelFrame(self.flight_frame, text="Add New Flight", padding=10)
        add_frame.pack(fill='x', padx=5, pady=5)
        
        # Flight input fields
        fields = [
            ("Start City:", "start_city"),
            ("Departure Time:", "departure_time"),
            ("End City:", "end_city"),
            ("Arrival Time:", "arrival_time"),
            ("Fare:", "fare")
        ]
        
        self.flight_entries = {}
        for i, (label, field) in enumerate(fields):
            ttk.Label(add_frame, text=label).grid(row=0, column=i*2, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(add_frame, width=10)
            entry.grid(row=0, column=i*2+1, padx=5, pady=5)
            self.flight_entries[field] = entry
        
        # Add button
        ttk.Button(add_frame, text="Add Flight", command=self.add_flight).grid(row=1, column=0, columnspan=10, pady=10)
        
        # Flight list section
        list_frame = ttk.LabelFrame(self.flight_frame, text="Current Flights", padding=10)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Treeview for flight list
        columns = ("Flight No", "Start City", "Departure", "End City", "Arrival", "Fare")
        self.flight_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.flight_tree.heading(col, text=col)
            self.flight_tree.column(col, width=100)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.flight_tree.yview)
        self.flight_tree.configure(yscrollcommand=scrollbar.set)
        
        self.flight_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Delete button
        ttk.Button(list_frame, text="Delete Selected", command=self.delete_flight).pack(pady=5)
    
    def setup_search_tab(self):
        # Search parameters
        search_frame = ttk.LabelFrame(self.search_frame, text="Search Parameters", padding=10)
        search_frame.pack(fill='x', padx=5, pady=5)
        
        # Parameter fields
        params = [
            ("Start City:", "start_city"),
            ("End City:", "end_city"),
            ("Start Time (t1):", "t1"),
            ("End Time (t2):", "t2")
        ]
        
        self.search_entries = {}
        for i, (label, field) in enumerate(params):
            ttk.Label(search_frame, text=label).grid(row=i//2, column=(i%2)*2, padx=10, pady=5, sticky='e')
            entry = ttk.Entry(search_frame, width=15)
            entry.grid(row=i//2, column=(i%2)*2+1, padx=10, pady=5)
            self.search_entries[field] = entry
        
        # Set default values
        self.search_entries["start_city"].insert(0, "0")
        self.search_entries["end_city"].insert(0, "4")
        self.search_entries["t1"].insert(0, "0")
        self.search_entries["t2"].insert(0, "300")
        
        # Search button
        ttk.Button(search_frame, text="Find Routes", command=self.find_routes).grid(row=2, column=0, columnspan=4, pady=20)
        
        # Instructions
        info_frame = ttk.LabelFrame(self.search_frame, text="Route Types", padding=10)
        info_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        info_text = """
Route Types Explained:

1. Least Flights, Earliest Arrival:
   - Minimizes the number of flights
   - If tied, chooses the route that arrives earliest

2. Cheapest Route:
   - Minimizes the total fare cost
   - May use more flights if it's cheaper

3. Least Flights, Cheapest:
   - Minimizes the number of flights first
   - If tied, chooses the cheapest among those with minimum flights
        """
        
        ttk.Label(info_frame, text=info_text, justify='left').pack(anchor='w')
    
    def setup_results_tab(self):
        # Results display
        self.results_text = scrolledtext.ScrolledText(self.results_frame, wrap=tk.WORD, height=30)
        self.results_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def add_flight(self):
        try:
            # Get values from entries
            start_city = int(self.flight_entries["start_city"].get())
            departure_time = int(self.flight_entries["departure_time"].get())
            end_city = int(self.flight_entries["end_city"].get())
            arrival_time = int(self.flight_entries["arrival_time"].get())
            fare = int(self.flight_entries["fare"].get())
            
            # Validate input
            if arrival_time <= departure_time:
                messagebox.showerror("Error", "Arrival time must be after departure time")
                return
            
            # Create new flight
            flight_no = len(self.flights)
            new_flight = Flight(flight_no, start_city, departure_time, end_city, arrival_time, fare)
            self.flights.append(new_flight)
            
            # Clear entries
            for entry in self.flight_entries.values():
                entry.delete(0, tk.END)
            
            # Refresh display
            self.refresh_flight_list()
            messagebox.showinfo("Success", "Flight added successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all fields")
    
    def delete_flight(self):
        selected = self.flight_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a flight to delete")
            return
        
        # Get selected flight index
        item = self.flight_tree.item(selected[0])
        flight_no = int(item['values'][0])
        
        # Remove flight and reassign flight numbers
        self.flights = [f for f in self.flights if f.flight_no != flight_no]
        for i, flight in enumerate(self.flights):
            flight.flight_no = i
        
        self.refresh_flight_list()
        messagebox.showinfo("Success", "Flight deleted successfully!")
    
    def refresh_flight_list(self):
        # Clear existing items
        for item in self.flight_tree.get_children():
            self.flight_tree.delete(item)
        
        # Add flights to treeview
        for flight in self.flights:
            self.flight_tree.insert('', 'end', values=(
                flight.flight_no,
                flight.start_city,
                flight.departure_time,
                flight.end_city,
                flight.arrival_time,
                f"${flight.fare}"
            ))
    
    def find_routes(self):
        try:
            # Get search parameters
            start_city = int(self.search_entries["start_city"].get())
            end_city = int(self.search_entries["end_city"].get())
            t1 = int(self.search_entries["t1"].get())
            t2 = int(self.search_entries["t2"].get())
            
            # Create planner and find routes
            planner = Planner(self.flights)
            
            route1 = planner.least_flights_earliest_route(start_city, end_city, t1, t2)
            route2 = planner.cheapest_route(start_city, end_city, t1, t2)
            route3 = planner.least_flights_cheapest_route(start_city, end_city, t1, t2)
            
            # Display results
            self.display_results(route1, route2, route3, start_city, end_city, t1, t2)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all search parameters")
    
    def display_results(self, route1, route2, route3, start_city, end_city, t1, t2):
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        # Header
        header = f"ROUTE SEARCH RESULTS\n"
        header += f"From City {start_city} to City {end_city}\n"
        header += f"Time window: {t1} to {t2}\n"
        header += "="*60 + "\n\n"
        
        self.results_text.insert(tk.END, header)
        
        # Route 1: Least Flights, Earliest Arrival
        self.results_text.insert(tk.END, "1. LEAST FLIGHTS, EARLIEST ARRIVAL\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        if route1:
            self.display_route(route1, "Minimizes flights, breaks ties by earliest arrival")
        else:
            self.results_text.insert(tk.END, "No valid route found\n")
        self.results_text.insert(tk.END, "\n")
        
        # Route 2: Cheapest Route
        self.results_text.insert(tk.END, "2. CHEAPEST ROUTE\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        if route2:
            self.display_route(route2, "Minimizes total fare cost")
        else:
            self.results_text.insert(tk.END, "No valid route found\n")
        self.results_text.insert(tk.END, "\n")
        
        # Route 3: Least Flights, Cheapest
        self.results_text.insert(tk.END, "3. LEAST FLIGHTS, CHEAPEST\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        if route3:
            self.display_route(route3, "Minimizes flights, breaks ties by lowest cost")
        else:
            self.results_text.insert(tk.END, "No valid route found\n")
        self.results_text.insert(tk.END, "\n")
    
    def display_route(self, route, description):
        total_cost = sum(flight.fare for flight in route)
        total_time = route[-1].arrival_time - route[0].departure_time if route else 0
        
        self.results_text.insert(tk.END, f"Description: {description}\n")
        self.results_text.insert(tk.END, f"Number of flights: {len(route)}\n")
        self.results_text.insert(tk.END, f"Total cost: ${total_cost}\n")
        self.results_text.insert(tk.END, f"Total travel time: {total_time} units\n")
        self.results_text.insert(tk.END, f"Departure: {route[0].departure_time}, Arrival: {route[-1].arrival_time}\n\n")
        
        self.results_text.insert(tk.END, "Flight Details:\n")
        for i, flight in enumerate(route, 1):
            flight_info = f"  {i}. Flight {flight.flight_no}: "
            flight_info += f"City {flight.start_city} -> City {flight.end_city} "
            flight_info += f"({flight.departure_time}-{flight.arrival_time}) ${flight.fare}\n"
            self.results_text.insert(tk.END, flight_info)


def main():
    root = tk.Tk()
    app = FlightPlannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()