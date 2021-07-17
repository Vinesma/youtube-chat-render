"""
MIT License

Copyright (c) 2021 Otavio Cornelio da Silva

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os

from core.chat import ChatParser
from core.frame import FrameGenerator
from core.video import Video
from core.args import Args
from core.clean import Clean

def main():
    # Initialize args
    args = Args()
    args.load_args()
    
    # Check if a folder exists for outputting frames to
    if not os.path.exists(args.output_frames_path):
        raise Exception(f'Please create the {args.output_frames_path} folder!')
    
    # If dry running, generate a 30 sec video file for testing
    if args.dry_run:
        Video.gen_dry_run(args.input_video_path)

    # Start
    if args.start_at in args.start_positions[:1]:
        # Parser
        print('Parsing messages from file...')
        chat = ChatParser(args.input_chat_path)
        timestamps = chat.parse_raw()

        # Frame generation
        print('Generating frames, this may take a while...')
        frameGen = FrameGenerator(
            timestamps,
            font_size=args.chat_font_size,
            spacing=args.chat_message_spacing,
            width=args.chat_width,
            message_count=args.chat_message_amount,
            dry_run=args.dry_run,
            )
        frameGen.generate_frames()

    # Video generation step
    if args.start_at in args.start_positions[:2]:
        print('Generating chat...')
        Video.render_chat(
            os.path.join(args.output_frames_path, 'frame_%06d.png'),
            args.output_chat_path
            )

    # Overlay step
    if args.start_at in args.start_positions[:3]:
        print('Overlaying chat onto your video...')

        if args.dry_run:
            print('This is a test run because of --dry-run')
            input_video_path = '30_sec_test.mp4'
        else:
            input_video_path = args.input_video_path 

        Video.overlay(
            input_video_path,
            args.output_chat_path,
            position=(
                args.overlay_position_x,
                args.overlay_position_y
                ),
            opacity=args.overlay_opacity
            )

    if not args.no_clean:
        Clean.all(args.output_frames_path, args.output_chat_path)

    print('Done.')
    exit(0)

if __name__ == "__main__":
    main()
