import re

from waitlist import Time, Waitlist


class Menu:
    """A class representing the menu for the restaurant reservation program."""
    
    __TIME_REGEX = re.compile(r"(\d\d):(\d\d)")
    
    def __init__(self) -> None:
        """Initialize the menu with the waitlist object."""
        self.waitlist = Waitlist()
    
    @staticmethod
    def __make_time(time_string: str) -> Time:
        """Convert a string in the format HH:MM to a Time object.

        Raises
        ------
        ValueError
            If the string is not a valid time.
        """
        match = Menu.__TIME_REGEX.match(time_string)
        if match is None:
            raise ValueError(f"Invalid time: {time_string}")
        return Time(int(match.group(1)), int(match.group(2)))
    
    def run(self) -> None:
        """Print the main menu."""
        print("Welcome to the Restaurant Reservation System!")
        print("==============================================")
        print("Please select an option:")
        print("1. Add a customer to the waitlist")
        print("2. Seat the next customer")
        print("3. Change the time of a customer's reservation")
        print("4. Peek at the next customer")
        print("5. Print the reservation list")
        print("6. Quit")
        while True:
            print()
            choice = input("Enter your choice (1-6): ")
            print("*************************************************")
            match choice:
                case "1": # Add a customer to the waitlist
                    name = input("Enter the customer's name: ")
                    time_str = input("Enter the customer's reservation time (HH:MM): ")
                    time = self.__make_time(time_str)
                    self.waitlist.add_customer(name, time)
                    print()
                    print(f"{name} has been added to the waitlist at {time}")
                
                case "2": # Seat the next customer
                    print()
                    customer, time = self.waitlist.seat_customer()
                    print(f"Seated next customer: {customer}, time: {time}")
                
                case "3": # Change the time of a customer's reservation
                    name = input("Enter the customer's name: ")
                    time_str = input("Enter the new time of the reservation (HH:MM): ")
                    time = self.__make_time(time_str)
                    print()
                    print(f"{name}'s reservation time has been changed to {time}")
                    print()
                
                case "4": # Peek at the next customer
                    print()
                    match self.waitlist.peek():
                        case None:
                            print("There is nobody on the waitlist.")
                        case (customer, time):
                            print(
                                f"The next customer on the waitlist is: {customer}, "
                                f"reservation time: {time}"
                            )
                
                case "5": # Print the waitlist
                    self.waitlist.print_reservation_list()
                
                case "6": # exit
                    print("Thank you for using the Restaurant Reservation System!")
                    return
                
                case _:
                    print("Invalid choice. Try again.")

if __name__ == "__main__":
    Menu().run()
