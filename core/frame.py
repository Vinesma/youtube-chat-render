from PIL import Image, ImageDraw, ImageFont

class FrameGenerator():
    
    def __init__(self, timestamps):
        self.timestamps = timestamps
        self._last_frame = None
    
    def _generate_frame(self, time_slice):
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

        for index, content in enumerate(time_slice['content']):
            offset = offset_c * index
            text = f"{content['author']}: {content['text']}"
            draw.text((5, offset), text, fill=font_color, font=font)

        image.show()
        print(f'image window supports {frame_message_count} messages')
    
    def generate_frames(self):
        """Manage and generate frames"""
        for time_slice in self.timestamps:
            if time_slice['timestamp'] == '0:02':
                self._generate_frame(time_slice)