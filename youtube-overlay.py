import os

import ffmpeg

from core.chat import ChatParser
from core.frame import FrameGenerator

def main():
    main_dir = os.path.abspath('.')
    raw_chat_file = os.path.join(main_dir, 'files', 'chat.txt')
    
    chat = ChatParser(raw_chat_file)
    timestamps = chat.parse_raw()

    frameGen = FrameGenerator(timestamps)
    frameGen.generate_frames()

    print('Generating video file...')
    ffmpeg.input('./frames/frame_*.png', pattern_type='glob', framerate=1).output('chat.mp4').run()
    
if __name__ == "__main__":
    main()