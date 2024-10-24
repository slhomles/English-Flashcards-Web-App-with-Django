from django.db import models
from django.utils.text import slugify

# Create your models here.
class Topic(models.Model):
    id_topic = models.AutoField(primary_key = True, null = False)
    name_topic = models.CharField(max_length = 50, blank = False)
    slug_topic = models.SlugField(default = "", null = False)

    def save(self, *args, **kwargs):
        if not self.slug_topic:  
            self.slug_topic = slugify(self.name_topic)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name_topic}'

class Flashcards(models.Model):
    id_flashcard = models.AutoField(primary_key= True, null = False)
    front = models.CharField(max_length = 200, blank = False)
    back = models.CharField(max_length = 300, blank = False)
    id_topic = models.ForeignKey(Topic,on_delete = models.CASCADE )
    slug_topic = models.SlugField(default = "", null = False)
    slug_flashcard = models.SlugField(default = "", null = False)

    def save(self, *args, **kwargs):
        if not self.slug_flashcard:  
            self.slug_flashcard = slugify(self.front) 
        super().save(*args, **kwargs)

    def __str__(self):

        return f'{self.front}'