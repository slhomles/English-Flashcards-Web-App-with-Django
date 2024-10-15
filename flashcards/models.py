from django.db import models

# Create your models here.
class Topic(models.Model):
    id_topic = models.AutoField(primary_key = True, null = False)
    name_topic = models.CharField(max_length = 50, blank = False)

    def __str__(self):
        return f'{self.name_topic}'

class Flashcards(models.Model):
    id_flashcard = models.AutoField(primary_key= True, null = False)
    front = models.CharField(max_length = 200, blank = False)
    back = models.CharField(max_length = 300, blank = False)
    id_topic = models.ForeignKey(Topic,on_delete = models.CASCADE )

    def __str__(self):
        return f'{self.front}'