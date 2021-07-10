class Time:
    """Represents a live clock, by default starts at 0:00"""

    def __init__(self, initial_hour = 0, initial_minute = 0, initial_second = 0):
        self.hour = initial_hour
        self.minute = initial_minute
        self.second = initial_second

    def format_time(self):
        """Format time to supported format"""
        if self.hour == 0:
            return f'{self.minute}:{self.second:02}'
        else:
            return f'{self.hour}:{self.minute:02}:{self.second:02}'
        
    def _add_hour(self):
        self.hour += 1

    def _add_minute(self):
        if self.minute != 59:
            self.minute += 1
        else:
            self.minute = 0
            self._add_hour()

    def _add_second(self):
        if self.second != 59:
            self.second += 1
        else:
            self.second = 0
            self._add_minute()
    
    def advance_one_second(self):
        """Add one second to the clock."""
        self._add_second()

    def now(self):
        return self.format_time()