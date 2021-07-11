import os

from core.chat import ChatParser
from core.frame import FrameGenerator

def main():
    main_dir = os.path.abspath('.')
    raw_chat_file = os.path.join(main_dir, 'files', 'chat.txt')
    
    chat = ChatParser(raw_chat_file)
    timestamps = chat.parse_raw()

    frameGen = FrameGenerator(timestamps)
    frameGen.generate_frames()
    
if __name__ == "__main__":
    main()