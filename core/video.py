from subprocess import run

class Video:
    """Render video with ffmpeg"""

    @staticmethod
    def render_chat(_input, output, framerate = 1):
        """Render a window of chat messages to video."""
        command = [
            'ffmpeg',
            '-v',
            'error',
            '-framerate',
            f'{framerate}',
            '-i',
            _input,
            output,
        ]
        run(command, check=True, text=True)

    @staticmethod
    def overlay(video, chat, opacity = 0.8, position = (0, 0)):
        """Overlay the chat window onto the video at the specified position (top left corner by default)."""
        command = [
            'ffmpeg',
            '-v',
            'error',
            '-i',
            video,
            '-i',
            chat,
            '-filter_complex',
            f'[1]format=yuva444p,colorchannelmixer=aa={opacity}[in2];[0][in2]overlay={position[0]}:{position[1]}',
            'output.mp4',
        ]
        run(command, check=True, text=True)
