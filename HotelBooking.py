import json
import os
from datetime import datetime, timedelta

class HotelBookingSystem:
    def __init__(self):
        self.rooms_file = "rooms.Meet"
        self.bookings_file = "bookings.json"
        self.initialize_files()
        self.load_data()

    def initialize_files(self):
        """Create necessary files if they don't exist"""
        if not os.path.exists(self.rooms_file):
            with open(self.rooms_file, 'w') as f:
                json.dump([], f)
        
        if not os.path.exists(self.bookings_file):
            with open(self.bookings_file, 'w') as f:
                json.dump([], f)

    def load_data(self):
        """Load rooms and bookings data from files"""
        with open(self.rooms_file, 'r') as f:
            self.rooms = json.load(f)
        
        with open(self.bookings_file, 'r') as f:
            self.bookings = json.load(f)

    def save_data(self):
        """Save rooms and bookings data to files"""
        with open(self.rooms_file, 'w') as f:
            json.dump(self.rooms, f, indent=4)
        
        with open(self.bookings_file, 'w') as f:
            json.dump(self.bookings, f, indent=4)

    def add_room(self, room_number, room_type, price_per_night, capacity):
        """Add a new room to the system"""
        new_room = {
            "room_number": room_number,
            "room_type": room_type,
            "price_per_night": price_per_night,
            "capacity": capacity,
            "available": True
        }
        
        # Check if room already exists
        for room in self.rooms:
            if room["room_number"] == room_number:
                print(f"Room {room_number} already exists!")
                return
        
        self.rooms.append(new_room)
        self.save_data()
        print(f"Room {room_number} added successfully!")

    def display_available_rooms(self):
        """Display all available rooms"""
        available_rooms = [room for room in self.rooms if room["available"]]
        
        if not available_rooms:
            print("No available rooms at the moment.")
            return
        
        print("\nAvailable Rooms:")
        print("-" * 50)
        print(f"{'Room No.':<10}{'Type':<15}{'Price/Night':<15}{'Capacity':<10}")
        print("-" * 50)
        
        for room in available_rooms:
            print(f"{room['room_number']:<10}{room['room_type']:<15}${room['price_per_night']:<15}{room['capacity']:<10}")
    
    def check_room_availability(self, room_number, check_in, check_out):
        """Check if a room is available for given dates"""
        # Convert string dates to datetime objects
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return False
        
        if check_out_date <= check_in_date:
            print("Check-out date must be after check-in date.")
            return False
        
        # Find the room
        room = next((r for r in self.rooms if r["room_number"] == room_number), None)
        if not room:
            print(f"Room {room_number} does not exist.")
            return False
        
        if not room["available"]:
            print(f"Room {room_number} is not available for booking.")
            return False
        
        # Check for overlapping bookings
        for booking in self.bookings:
            if booking["room_number"] == room_number:
                existing_check_in = datetime.strptime(booking["check_in"], "%Y-%m-%d")
                existing_check_out = datetime.strptime(booking["check_out"], "%Y-%m-%d")
                
                # Check for date overlap
                if not (check_out_date <= existing_check_in or check_in_date >= existing_check_out):
                    print(f"Room {room_number} is already booked from {booking['check_in']} to {booking['check_out']}.")
                    return False
        
        return True

    def book_room(self, room_number, guest_name, check_in, check_out, guests):
        """Book a room for specific dates"""
        if not self.check_room_availability(room_number, check_in, check_out):
            return False
        
        # Calculate total price
        room = next(r for r in self.rooms if r["room_number"] == room_number)
        nights = (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days
        total_price = nights * room["price_per_night"]
        
        new_booking = {
            "booking_id": len(self.bookings) + 1,
            "room_number": room_number,
            "guest_name": guest_name,
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "total_price": total_price,
            "booking_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.bookings.append(new_booking)
        self.save_data()
        print("\nBooking successful!")
        print(f"Booking ID: {new_booking['booking_id']}")
        print(f"Total Price: ${total_price}")
        return True

    def view_bookings(self):
        """Display all bookings"""
        if not self.bookings:
            print("No bookings found.")
            return
        
        print("\nAll Bookings:")
        print("-" * 90)
        print(f"{'ID':<5}{'Room':<8}{'Guest':<20}{'Check-in':<12}{'Check-out':<12}{'Guests':<8}{'Price':<10}{'Booked On':<12}")
        print("-" * 90)
        
        for booking in self.bookings:
            print(f"{booking['booking_id']:<5}{booking['room_number']:<8}{booking['guest_name'][:18]:<20}"
                  f"{booking['check_in']:<12}{booking['check_out']:<12}{booking['guests']:<8}"
                  f"${booking['total_price']:<9}{booking['booking_date']:<12}")

    def cancel_booking(self, booking_id):
        """Cancel a booking by ID"""
        booking = next((b for b in self.bookings if b["booking_id"] == booking_id), None)
        
        if not booking:
            print(f"No booking found with ID {booking_id}.")
            return False
        
        self.bookings.remove(booking)
        self.save_data()
        print(f"Booking {booking_id} has been cancelled.")
        return True

    def generate_report(self):
        """Generate a report of bookings and revenue"""
        if not self.bookings:
            print("No bookings to report.")
            return
        
        total_revenue = sum(booking["total_price"] for booking in self.bookings)
        total_bookings = len(self.bookings)
        
        print("\nHotel Booking Report")
        print("=" * 40)
        print(f"Total Bookings: {total_bookings}")
        print(f"Total Revenue: ${total_revenue}")
        
        # Bookings by room type
        print("\nBookings by Room Type:")
        room_types = set(room["room_type"] for room in self.rooms)
        for room_type in room_types:
            count = sum(1 for booking in self.bookings 
                       if next(room for room in self.rooms 
                               if room["room_number"] == booking["room_number"])["room_type"] == room_type)
            print(f"{room_type}: {count} bookings")

def main():
    system = HotelBookingSystem()
    
    # Add some sample rooms if none exist
    if not system.rooms:
        system.add_room("101", "Standard", 100, 2)
        system.add_room("102", "Standard", 100, 2)
        system.add_room("201", "Deluxe", 150, 3)
        system.add_room("202", "Deluxe", 150, 3)
        system.add_room("301", "Suite", 250, 4)
    
    while True:
        print("\nHotel Booking System")
        print("1. View Available Rooms")
        print("2. Book a Room")
        print("3. View All Bookings")
        print("4. Cancel Booking")
        print("5. Generate Report")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            system.display_available_rooms()
        
        elif choice == "2":
            room_number = input("Enter room number: ")
            guest_name = input("Enter guest name: ")
            check_in = input("Enter check-in date (YYYY-MM-DD): ")
            check_out = input("Enter check-out date (YYYY-MM-DD): ")
            guests = input("Enter number of guests: ")
            
            system.book_room(room_number, guest_name, check_in, check_out, guests)
        
        elif choice == "3":
            system.view_bookings()
        
        elif choice == "4":
            booking_id = int(input("Enter booking ID to cancel: "))
            system.cancel_booking(booking_id)
        
        elif choice == "5":
            system.generate_report()
        
        elif choice == "6":
            print("Thank you for using the Hotel Booking System!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()