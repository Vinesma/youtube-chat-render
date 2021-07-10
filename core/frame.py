from PIL import Image, ImageDraw, ImageFont

class FrameGenerator():
    
    def __init__(self, timestamps, font_size = 16, message_count = 32):
        self.timestamps = timestamps
        self.font_size = font_size
        self.message_count = message_count
        self._last_frame = None
        self._frame_count = 0
        
    def _set_last_frame(self, image, message_block_size):
        self._last_frame = {
            'image': image,
            'block_size': message_block_size
        }
    
    def _get_last_frame(self):
        return self._last_frame
    
    def _advance_frame_count(self):
        self._frame_count += 1
    
    def _get_frame_count(self):
        return self._frame_count
    
    def _generate_frame(self, time_slice):
        """Generate one frame of the chat window"""
        spacing = self.font_size + 2
        font_path='/usr/share/fonts/OTF/ipamp.ttf'
        font_color=(255, 255, 255)
        image_width = 400
        image_height = spacing * self.message_count
        image_type='RGBA'
        image_bg_color_rgba = (28, 31, 32, 230)
        message_block_size = len(time_slice['content']) * spacing
        offset_from_top = image_height - message_block_size

        image = Image.new(image_type, (image_width, image_height), image_bg_color_rgba)
        font = ImageFont.truetype(font_path, size=self.font_size)
        draw = ImageDraw.Draw(image)
        
        for index, content in enumerate(time_slice['content']):
            offset = (spacing * index) + offset_from_top
            text = f"{content['author']}: {content['text']}"
            draw.text((5, offset), text, fill=font_color, font=font)

        self._advance_frame_count()
        self._set_last_frame(image, message_block_size)
        image.show()
    
    def generate_frames(self):
        """Manage and generate frames"""
        
        for index in range(2,4):
            time_slice = self.timestamps[index]
            self._generate_frame(time_slice)
        
        # for time_slice in self.timestamps:
        #     self._generate_frame(time_slice)
                
        print(self._get_frame_count())