from os import path

from PIL import Image, ImageDraw, ImageFont

class FrameGenerator():
    """Manages and generates frames for the chat window

        Args (mandatory):
            timestamps - A list of timestamps for generating frames.
        
        Args (optional):
            font_size - Text font size, will be used to calculate height of window along with message_count.
            spacing - Pixel spacing between text, used to calculate the vertical space one row of text takes.
            message_count - How many messages the window can support in one frame, will be used to calculate height of window along with font_size.
            width - Width of window.
    """
    
    def __init__(self, timestamps, font_size = 18, spacing = 2, message_count = 30, width = 400):
        # Mandatory
        self.timestamps = timestamps
        # Optional
        # Font
        self.font_size = font_size
        self.font_path='/usr/share/fonts/OTF/ipamp.ttf'
        self.font_color_text=(255, 255, 255)
        self.font_color_author=(59, 162, 230)
        self.font = ImageFont.truetype(self.font_path, size=self.font_size)
        # Size and spacing
        self.message_count = message_count
        self.spacing = spacing
        self.row_height = font_size + spacing
        self.left_padding = 2
        # Image
        self.image_width = width
        self.image_height = self.row_height * message_count
        self.image_type='RGBA'
        self.image_bg_color_rgba = (28, 31, 32, 200)
        # Management
        self._last_contents = []
        self._frame_count = 0
        self._save_path = path.join('.', 'frames')
        
    def _set_last_content(self, content):
        self._last_contents = content
    
    def _advance_frame_count(self):
        self._frame_count += 1
    
    def _get_frame_count(self):
        return self._frame_count

    def append_content(self, list1, list2):
        """Append 2 lists of content, while respecting the size restrictions of the window. 
        
            list2 has less priority and thus will have items deleted first.
        """
        while len(list1) + len(list2) > self.message_count:
            if len(list2) > 0:
                del list2[0]
            else:
                del list1[0]

        return list2 + list1

    def _generate_frame(self, time_slice):
        """Generate one frame of the chat window"""

        image = Image.new(self.image_type, (self.image_width, self.image_height), self.image_bg_color_rgba)
        draw = ImageDraw.Draw(image)
        
        contents = self.append_content(time_slice['content'], self._last_contents)
        message_block_size = len(contents) * self.row_height
        offset_from_top = self.image_height - message_block_size
        
        for index, content in enumerate(contents):
            author = f'{content["author"]}:'
            message = content['text']
            offset_y = (self.row_height * index) + offset_from_top
            offset_x = draw.textlength(author, font=self.font) + self.left_padding + 3

            draw.text((self.left_padding, offset_y), author, fill=self.font_color_author, font=self.font)
            draw.text((offset_x, offset_y), message, fill=self.font_color_text, font=self.font)
            
        self._advance_frame_count()
        self._set_last_content(contents)
        image.save(path.join(self._save_path, f'frame_{self._get_frame_count():06}.png'))
    
    def generate_frames(self):
        """Manage and generate frames"""
        
        print('Generating frames, this may take a while...')

        for time_slice in self.timestamps:
            self._generate_frame(time_slice)
                
        print(f'Done. Generated {self._get_frame_count()} frames.')