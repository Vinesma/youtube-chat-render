class FileReader:
    """Read a supported chat file."""

    def _has_negative_timestamp(self, line):
        """Check if the message has a negative timestamp."""
        return line.startswith('-')

    def read_raw(self, file_path):
        """Read a simple raw file with chat contents.
        
            Returns:
                list of strings where each line represents one message, removes messages with negative timestamps e.g. '-0:01'
        """
        lines = []
        count = 0

        with open(file_path, 'r') as _file:
            for line in _file:
                if not self._has_negative_timestamp(line):
                    lines.append(line)
                count += 1

        print(f'Parsed {count} lines.')

        return lines
