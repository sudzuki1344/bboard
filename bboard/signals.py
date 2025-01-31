from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch.dispatcher import receiver, Signal
from django.contrib.auth.models import User
from bboard.models import Bb, Profile

# 1. Автоматическое создание профиля пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, 'profile'):
        Profile.objects.get_or_create(user=instance)
        print(f'Профиль создан для пользователя: {instance.username}')

# 2. Существующие сигналы (улучшены для обработки kwargs)
@receiver(post_save, sender=Bb)
def post_save_dispatch(sender, instance, created, **kwargs):
    print(f'Создали объявление с заголовком: {instance.title.capitalize()}')
    if created:
        print(f'Создано объявление в рубрике {instance.rubric.name}')

@receiver(pre_delete, sender=Bb)
def pre_delete_dispatch(sender, instance, **kwargs):
    print(f'Удаляем объявление с заголовком: {instance.title}')

@receiver(post_delete, sender=Bb)
def post_delete_dispatch(sender, instance, **kwargs):
    print(f'Удалили объявление с заголовком: {instance.title}')

# 3. Новый сигнал: логирование изменений в цене
@receiver(post_save, sender=Bb)
def price_change_logger(sender, instance, **kwargs):
    if instance.pk:
        previous = Bb.objects.filter(pk=instance.pk).first()
        if previous and previous.price != instance.price:
            print(f'Цена объявления "{instance.title}" изменена: {previous.price} -> {instance.price}')


add_bb = Signal()

@receiver(add_bb)
def add_bb_dispatch(sender, instance, **kwargs):
    print(f'{instance.rubric.name}, {instance.price}')

