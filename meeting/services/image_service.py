import io

from PIL import Image
from django.core.files.base import File

from django.conf import settings


class WatermarkImage:
    """Класс для добавления вотермарки на входную фотографию """

    WATERMARK_PATH = f'{settings.MEDIA_ROOT}/default/watermark.png'

    def __init__(self, image: File, width=300, height=300):
        # Открываем изображения и приводим к нужному размеру
        self.image_width = width
        self.image_height = height
        self.image = Image.open(image).resize((width, height)).convert('RGB')

    def __add_water_mark(self, width=200, height=200) -> None:
        """Функция добавляет вотермарку в self.image"""

        # Открываем изображение вотермарки и приводим к нужному размеру
        with Image.open(self.WATERMARK_PATH).resize((width, height)) as watermark:
            # Считаем координаты, чтобы вотермарка была по центру
            paste_coords = ((self.image.width - width) // 2,
                            (self.image.height - height) // 2)
            self.image.paste(watermark, paste_coords, watermark)

    def get(self) -> File:
        """Функция возвращает объект FIle, который содержит изобржаение с вотермаркой"""

        self.__add_water_mark()
        new_image = io.BytesIO()
        self.image.save(new_image, format='JPEG')
        self.image.close()
        return File(new_image)
