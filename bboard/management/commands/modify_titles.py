from django.core.management.base import BaseCommand
from bboard.models import Bb
import re

class Command(BaseCommand):
    help = 'Модифицирует заголовки объявлений и удаляет записи с нечетными цифрами'

    def handle(self, *args, **options):
        # Шаг 1: Изменяем все заголовки, добавляя id
        bbs = Bb.objects.all()
        self.stdout.write('Начинаю обновление заголовков...')
        modified_count = 0
        
        for bb in bbs:
            original_title = bb.title
            # Проверяем, не содержит ли заголовок уже id в скобках
            if not re.search(r'\(\d+\)$', original_title):
                bb.title = f"{original_title} ({bb.id})"
                bb.save()
                modified_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Обновлено заголовков: {modified_count}'
        ))

        # Шаг 2: Удаляем записи с нечетными цифрами
        bbs = Bb.objects.all()
        self.stdout.write('Начинаю поиск записей с нечетными цифрами...')
        deleted_count = 0
        
        for bb in bbs:
            # Находим все цифры в заголовке
            numbers = re.findall(r'\d+', bb.title)
            should_delete = False
            
            # Проверяем каждое число
            for num in numbers:
                if any(int(digit) % 2 != 0 for digit in num):
                    should_delete = True
                    break
            
            if should_delete:
                self.stdout.write(f'Удаляю запись: {bb.title}')
                bb.delete()
                deleted_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Удалено записей с нечетными цифрами: {deleted_count}'
        )) 