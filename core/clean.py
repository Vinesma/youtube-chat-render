import os

class Clean():

    @staticmethod
    def all(frames_folder, chat_video_path):
        """Delete all non-essentials."""
        try:
            for file in os.listdir(frames_folder):
                if file.endswith('.png'):
                    os.remove(os.path.join(frames_folder, file))

            os.remove(chat_video_path)
            os.remove('30_sec_test.mp4')
        except FileNotFoundError:
            pass
