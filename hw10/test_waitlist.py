import unittest

from waitlist import Entry, Time, Waitlist


class TestTime(unittest.TestCase):
    def test_init(self) -> None:
        for hour in range(24):
            for minute in range(60):
                with self.subTest(hour=hour, minute=minute):
                    time = Time(hour, minute)
                    self.assertEqual(time.hour, hour)
                    self.assertEqual(time.minute, minute)
    
    def test_init_invalid(self) -> None:
        with self.assertRaises(ValueError):
            Time(24, 0)
        with self.assertRaises(ValueError):
            Time(-1, 0)
        with self.assertRaises(ValueError):
            Time(0, 60)
        with self.assertRaises(ValueError):
            Time(0, -1)
    
    def test_str(self) -> None:
        self.assertEqual(str(Time(0, 0)), "00:00")
        self.assertEqual(str(Time(23, 59)), "23:59")
        self.assertEqual(str(Time(12, 34)), "12:34")
    
    def test_ordering(self) -> None:
        times = tuple(Time(h, m) for h in range(24) for m in range(60))
        for i, time in enumerate(times):
            for time2 in times[i:]:
                self.assertLessEqual(time, time2)
            for time2 in times[:i]:
                self.assertGreater(time, time2)

class TestEntry(unittest.TestCase):
    def test_init(self) -> None:
        entry = Entry(Time(0, 0), "foo")
        self.assertEqual(entry.time, Time(0, 0))
        self.assertEqual(entry.name, "foo")
    
    def test_ordering(self) -> None:
        # NOTE: the second tuple adds a test for alphabetical order
        entries = tuple(Entry(Time(h, 59), "foo") for h in range(24))\
            + tuple(Entry(Time(23, 59), f"{chr(102+i)}oo") for i in range(1, 10))
        for i, entry in enumerate(entries):
            for entry2 in entries[i:]:
                self.assertLessEqual(entry, entry2)
            for entry2 in entries[:i]:
                self.assertGreater(entry, entry2)

class TestWaitlist(unittest.TestCase):
    def test_waitlist_init(self) -> None:
        waitlist = Waitlist()
        self.assertEqual(waitlist._entries, []) # type: ignore
    
    def test_waitlist_add_customer(self) -> None:
        waitlist = Waitlist()
        waitlist.add_customer("foo", Time(0, 0))
        self.assertEqual(waitlist._entries, [Entry(Time(0, 0), "foo")]) # type: ignore
    
    def test_waitlist_add_customer_alphabetical_ordering(self) -> None:
        waitlist = Waitlist()
        waitlist.add_customer("foo", Time(0, 0))
        waitlist.add_customer("bar", Time(0, 0))
        waitlist.add_customer("baz", Time(0, 0))
        self.assertEqual(
            waitlist._entries, [ # type: ignore
                Entry(Time(0, 0), "bar"),
                Entry(Time(0, 0), "baz"),
                Entry(Time(0, 0), "foo")
            ]
        )
    
    def test_waitlist_add_customer_time_ordering(self) -> None:
        waitlist = Waitlist()
        for i in range(100):
            waitlist.add_customer("foo", Time(i % 24, i % 60))
        
        self.assertEqual(
            waitlist._entries, # type: ignore
            sorted(waitlist._entries) # type: ignore
        )
    
    def test_waitlist_peek(self) -> None:
        waitlist = Waitlist()
        waitlist.add_customer("foo", Time(0, 0))
        waitlist.add_customer("bar", Time(0, 0))
        waitlist.add_customer("baz", Time(0, 0))
        self.assertEqual(waitlist.peek(), ("bar", Time(0, 0)))
    
    def test_waitlist_peek_empty(self) -> None:
        waitlist = Waitlist()
        self.assertEqual(waitlist.peek(), None)
    
    def test_waitlist_seat_customer(self) -> None:
        waitlist = Waitlist()
        for i in range(100):
            waitlist.add_customer("foo", Time(i % 24, i % 60))
        
        prev_time = waitlist.seat_customer()[1]
        for _ in range(99):
            time = waitlist.seat_customer()[1]
            self.assertLessEqual(prev_time, time)
            prev_time = time
        
        self.assertEqual(waitlist._entries, []) # type: ignore
        
        with self.assertRaises(ValueError):
            waitlist.seat_customer()
    
    def test_waitlist_change_reservation(self) -> None:
        waitlist = Waitlist()
        for i in range(100):
            waitlist.add_customer(str(i), Time(i % 24, i % 60))
        
        waitlist.change_reservation("69", Time(23, 59))
        self.assertEqual(waitlist._entries[-1].name, "69") # type: ignore


if __name__ == "__main__":
    unittest.main()
