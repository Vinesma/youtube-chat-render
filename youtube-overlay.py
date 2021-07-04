import os
import sys

def clear_screen():
    """Clears the terminal screen using the OS specific method."""
    os.system('clear' if sys.platform == 'linux' else 'cls')

def has_negative_timestamp(line):
    """Checks if the message has a negative timestamp."""
    return line.startswith('-')

def get_timestamp(line):
    """Returns the timestamp of the message."""
    return line.split(' ')[0]

def get_author(line):
    """Returns the message's author along with member status (if applicable)."""
    return line.split(' | ')[1].split(': ')[0]

def get_message(line):
    """Returns the message typed in chat."""
    return line.split(': ')[-1].strip()

def parse_file(path):
    """Read and parse a file with chat contents."""
    messages = []
    count = 0

    with open(path, 'r') as _file:
        for line in _file:
            if not has_negative_timestamp(line):
                chat_message = {
                    'author': get_author(line),
                    'text': get_message(line),
                    'timestamp': get_timestamp(line),
                }
                messages.append(chat_message)
            
            count += 1

    livestream_length = messages[-1]["timestamp"]

    print(f'Parsed {count} messages.')
    print(f'Livestream ran for: {livestream_length}')

    return [messages, livestream_length]

def advance_time(time_hour, time_minute, time_second):
    """Add one second to the clock."""
    if time_second != 59:
        time_second += 1
    else:
        time_second = 0
        if time_minute != 59:
            time_minute += 1
        else:
            time_minute = 0
            time_hour += 1
    
    if time_hour > 0:
        return [
            f'{time_hour}:{time_minute:02}:{time_second:02}',
            time_hour,
            time_minute,
            time_second,
        ]
    else:
        return [
            f'{time_minute}:{time_second:02}',
            time_hour,
            time_minute,
            time_second,
        ]

def find_empty(messages, livestream_length):
    time_hour = 0
    time_minute = 0
    time_second = 0
    count = 0
    time = f'{time_minute}:{time_second:02}'

    while time != livestream_length:
        if time != messages[count]:
            print(f'{time} has no messages.')

            time, time_hour, time_minute, time_second = advance_time(time_hour,
                                                                    time_minute, 
                                                                    time_second,
                                                                    )
        else:
            count += 1

def main():
    main_dir = os.path.abspath('.')
    raw_chat_file = os.path.join(main_dir, 'files', 'chat.txt')

    messages, livestream_length = parse_file(raw_chat_file)
    find_empty(messages, livestream_length)
    
if __name__ == "__main__":
    main()