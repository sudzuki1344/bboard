from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch.dispatcher import receiver, Signal

from bboard.models import Bb

@receiver(post_save, sender=Bb)
def post_save_dispatch(sender, **kwargs):
    snd = sender
    print(f'Создали обьявление с заголовком в модели {snd}')

    if kwargs['instance']:
        instance = kwargs['instance']
        instance.title = instance.title.capitalize()
        print(f'Создали обьявление с заголовками {instance.title}')

    if kwargs['created']:
        print(f'Создано обьявление в рубрике {kwargs["instance"].rubric.name}')

@receiver(pre_delete, sender=Bb)
def pre_delete_dispatch(sender, **kwargs):
    snd = sender
    print(f'Удаляем обьявление с заголовком в модели {snd}')

    if kwargs['instance']:
        instance = kwargs['instance']
        print(f'Удаляем обьявление с заголовком {instance.title}')

@receiver(post_delete, sender=Bb)
def post_delete_dispatch(sender, **kwargs):
    snd = sender
    print(f'Удалили обьявление с заголовком в модели {snd}')

    if kwargs['instance']:
        instance = kwargs['instance']
        print(f'Удалили обьявление с заголовком {instance.title}')

add_bb = Signal()

@receiver(add_bb)
def add_bb_dispatch(sender, instance, **kwargs):
    print(f'{instance.rubric.name}, {instance.price}')

