import csv
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from shop.models import Product  # 确保你导入了正确的模型类

class Command(BaseCommand):
    help = 'Upload products and images from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to upload products from')
        parser.add_argument('image_folder', type=str, help='The folder containing product images')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        image_folder = kwargs['image_folder']

        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过表头
            for row in reader:
                product = Product(
                    name=row[0],
                    description=row[1],
                    price=row[2],
                    category_id=row[3]  # 假设你的CSV文件有这些字段
                )
                # 处理图片
                image_path = os.path.join(image_folder, row[4])  # 假设 image_filename 在 CSV 的第五列
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as image_file:
                        product.image.save(row[4], File(image_file), save=False)
                product.save()
        self.stdout.write(self.style.SUCCESS('Successfully uploaded products and images'))
