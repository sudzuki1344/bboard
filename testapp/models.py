from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Spare(models.Model):
    name = models.CharField(max_length=30)
    notes = GenericRelation('Note', related_query_name='spare')


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare, through='Kit',
                                    through_fields=('machine', 'spare'))
    notes = GenericRelation('Note')


class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.IntegerField()


class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_id")
#Прямое
class Message(models.Model):
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-published']

class PrivateMessage(Message):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.OneToOneField(Message, on_delete=models.CASCADE, parent_link=True)

    class Meta:
        ordering = []

class SuperPrivateMessage(PrivateMessage):

    class Meta:
        proxy = True
        ordering = ['-content']

#Абстрактное
# class Message(models.Model):
#     content = models.TextField()
#     name = models.CharField(max_length=20)
#     email = models.EmailField()
#
#     class Meta:
#         abstract = True
#         ordering = ['name']
#
# class PrivateMessage(Message):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=40)
#     email = None

class SMS(models.Model):
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender}, To: {self.receiver} - {self.sent_at}"