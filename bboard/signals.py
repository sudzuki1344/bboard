from django.db.models.signals import post_save, pre_save, pre_init, post_init, pre_delete, post_delete
from django.dispatch import receiver, Signal

from bboard.models import Bb


# @receiver(pre_init, sender=Bb)
# @receiver(post_init, sender=Bb)
# @receiver(pre_save, sender=Bb)
@receiver(post_save, sender=Bb)
def post_save_dispatcher(sender, **kwargs):
    snd = sender
    print(f'Создаём объявление в модели {snd}')

    if kwargs['instance']:
        instance = kwargs['instance']
        instance.title = instance.title.capitalize()
        print(f'Объявление с заголовком {instance.title}')

    if kwargs['created']:
        print(f'Создано объявление в рубрике {kwargs["instance"].rubric.name}')

# post_save.connect(post_save_dispatcher)
# post_save.connect(post_save_dispatcher, sender=Bb)
# post_save.connect(post_save_dispatcher, dispatch_uid='post_save_dispatcher_1')
# post_save.connect(post_save_dispatcher, dispatch_uid='post_save_dispatcher_2')

# post_save.disconnect(receiver=post_save_dispatcher)
# post_save.disconnect(receiver=post_save_dispatcher, sender=Bb)
# post_save.disconnect(dispatch_uid='post_save_dispatcher_2')


@receiver(pre_delete, sender=Bb)
def pre_delete_dispatcher(sender, **kwargs):
    snd = sender
    print(f'Удаляем объявление в модели {snd}')

    if kwargs['instance']:
        instance = kwargs['instance']
        print(f'Удаляем бъявление с заголовком {instance.title}')


@receiver(post_delete, sender=Bb)
def post_delete_dispatcher(sender, **kwargs):
    snd = sender
    print(f'Удалили объявление в модели {snd}')

    if kwargs['instance']:
        instance = kwargs['instance']
        print(f'Удалили бъявление с заголовком {instance.title}')


# add_bb = Signal(providing_args=['instance', 'rubric'])  # устаревшая запись
add_bb = Signal()

@receiver(add_bb)
def add_bb_dispatcher(sender, instance, **kwargs):
    print(f'{instance.rubric.name}, {instance.price}')
