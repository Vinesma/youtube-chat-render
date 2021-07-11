import os

from core.chat import ChatParser
from core.frame import FrameGenerator
from core.video import Video

def main():
    main_dir = os.path.abspath('.')

    # Parser
    print('Parsing messages from file...')
    raw_chat_file = os.path.join(main_dir, 'files', 'chat.txt')
    chat = ChatParser(raw_chat_file)
    timestamps = chat.parse_raw()

    # Frame generation
    print('Generating frames, this may take a while...')
    frameGen = FrameGenerator(timestamps)
    frameGen.generate_frames()

    # Video generation
    print('Generating chat...')
    Video.render_chat('./frames/frame_%06d.png', 'chat.mp4')
    print('Overlaying chat onto your video...')
    Video.overlay('video.mp4', 'chat_t.mp4', position=(554, 380))

    print('Done.')
    exit(0)

if __name__ == "__main__":
    main()
