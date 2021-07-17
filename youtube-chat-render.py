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
