from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True, order=True)
class Time:
    """Represents a time in the format HH:MM."""
    
    hour: int
    minute: int
    
    def __post_init__(self) -> None:
        """Validate the time."""
        if not (0 <= self.hour < 24): # noqa: PLR2004
            raise ValueError(f"Invalid hour: {self.hour}")
        if not (0 <= self.minute < 60): # noqa: PLR2004
            raise ValueError(f"Invalid minute: {self.minute}")
    
    def __str__(self) -> str:
        """Return the string representation of the time."""
        return f"{self.hour:02d}:{self.minute:02d}"

@dataclasses.dataclass(frozen=True, order=True)
class Entry:
    """Represents a customer in the waitlist."""
    
    time: Time
    name: str


class Waitlist:
    _entries: list[Entry]
    
    def __init__(self) -> None:
        self._entries = []
    
    def add_customer(self, item: str, priority: Time) -> None:
        """Add a customer to the waiting list."""
        entry = Entry(priority, item)
        self._entries.append(entry)
        self._entries.sort()
    
    def peek(self) -> tuple[str, Time] | None:
        """Return the next customer to be seated, or None if the waitlist is empty."""
        if self._entries:
            return self._entries[0].name, self._entries[0].time
        return None
    
    def seat_customer(self) -> tuple[str, Time]:
        """Seat the next customer.
        
        This method removes the next customer from the waitlist, and returns their name
        and reservation time.

        Raises
        ------
        ValueError
            If the waitlist is empty.
        """
        if not self._entries:
            raise ValueError("The waitlist is empty.")
        result = self._entries.pop(0)
        return result.name, result.time
    
    def print_reservation_list(self) -> None:
        """Print all customers in order of their priority (reservation time)."""
        print("__________________________________________________")
        for entry in self._entries:
            print(
                f"The next customer on the waitlist is: {entry.name}, "
                f"time: {entry.time}"
            )
        print()
        print("__________________________________________________", end='\r') # dumb
    
    def change_reservation(self, name: str, new_priority: Time) -> None:
        """Change the reservation time for the customer with the given name.

        Raises
        ------
        ValueError
            If the customer is not on the waitlist.
        """
        for i, entry in enumerate(self._entries):
            if entry.name == name:
                self._entries.pop(i)
                self.add_customer(name, new_priority)
                break
        else:
            raise ValueError(f"Customer {name} not found in the waitlist.")
