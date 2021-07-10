import re

from core.utils.fileReader import FileReader
from core.utils.timestamp import Time

class ChatParser:
    
    def __init__(self, file_path):
        self.file_path = file_path

    def _get_timestamp(self, line):
        """Returns the timestamp of the message."""
        return line.split(' ')[0]

    def _get_author(self, line):
        """Returns the message's author with member status removed (if applicable)."""
        author = line.split(' | ')[1].split(': ')[0]
        return re.sub(r'\((New|Member).+\)', '', author)

    def _get_message(self, line):
        """Returns the message typed in chat."""
        return line.split(': ')[-1].strip()

    def parse_raw(self):
        """Parse raw chat lines to return the timeline and livestream length

            Returns:
                List of grouped timestamps. With author and text
        """
        reader = FileReader()
        lines = reader.read_raw(self.file_path)
        time = Time()

        livestream_length = self._get_timestamp(lines[-1])
        timestamps = []
        line_count = 0
        same_timestamp = False
        
        # Do this until the end of the livestream
        while time.now() != livestream_length:
            line = lines[line_count]
            now = time.now()

            # Check if the timestamp matches a message
            if now != self._get_timestamp(line):
                # If not: set an empty message at that timestamp and add one second to the clock
                time_slice = {
                    'timestamp': now,
                    'content': []
                }
                timestamps.append(time_slice)

                time.advance_one_second()
            else:
                # If yes: save the message and look ahead for one more in the same timestamp
                if not same_timestamp:
                    time_slice = {
                        'timestamp': self._get_timestamp(line),
                        'content': [
                            {
                                'author': self._get_author(line),
                                'text': self._get_message(line),
                            }
                        ]
                    }

                    timestamps.append(time_slice)
                else:
                    timestamps[-1]['content'].append({
                        'author': self._get_author(line),
                        'text': self._get_message(line),
                    })
                
                # If there is one more in the same timestamp: update the line count but not the clock
                if now == self._get_timestamp(lines[line_count + 1]):
                    line_count += 1
                    same_timestamp = True
                else:
                    line_count += 1
                    time.advance_one_second()
                    same_timestamp = False

        print(f'Livestream ran for: {livestream_length}')
        return timestamps
