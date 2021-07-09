import os
import sys
import re
from PIL import Image, ImageDraw, ImageFont

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
    """Returns the message's author with member status removed (if applicable)."""
    author = line.split(' | ')[1].split(': ')[0]
    return re.sub(r'\((New|Member).+\)', '', author)

def get_message(line):
    """Returns the message typed in chat."""
    return line.split(': ')[-1].strip()

def read_file(path):
    """Read a file with chat contents."""
    lines = []
    count = 0

    with open(path, 'r') as _file:
        for line in _file:
            if not has_negative_timestamp(line):
                lines.append(line)
            count += 1

    print(f'Parsed {count} lines.')

    return lines

def parse_lines(lines):
    """Parse raw chat lines to return the timeline and livestream lenght"""
    messages = []
    livestream_length = get_timestamp(lines[-1])

    for line in lines:
        chat_message = {
            'author': get_author(line),
            'text': get_message(line),
            'timestamp': get_timestamp(line),
        }
        messages.append(chat_message)

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

def generate_frame(messages):
    """Generate one frame of the chat window"""
    font_size = 16
    offset_c = font_size + 2
    font_path='/usr/share/fonts/OTF/ipamp.ttf'
    font_color=(255, 255, 255)
    image_width = 400
    image_height = offset_c * 32
    image_type='RGBA'
    image_bg_color_rgba = (28, 31, 32, 230)
    frame_message_count = image_height / offset_c

    image = Image.new(image_type, (image_width, image_height), image_bg_color_rgba)
    font = ImageFont.truetype(font_path, size=font_size)
    draw = ImageDraw.Draw(image)

    for index, message in enumerate(messages):
        offset = offset_c * index
        text = f"{message['author']}: {message['text']}"
        draw.text((5, offset), text, fill=font_color, font=font)

        #@TODO remove this
        if index >= frame_message_count - 2:
            break

    image.show()
    print(f'image window supports {frame_message_count} messages')

def main():
    main_dir = os.path.abspath('.')
    raw_chat_file = os.path.join(main_dir, 'files', 'chat.txt')

    raw_chat = read_file(raw_chat_file)
    messages, livestream_length = parse_lines(raw_chat)
    # generate_frame(messages)

    # find_empty(messages, livestream_length)
    
if __name__ == "__main__":
    main()