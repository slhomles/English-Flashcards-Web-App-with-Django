from django.db import models
from django.template.defaultfilters import default
from django.utils.text import slugify

# Create your models here.
class Topic(models.Model):
    id_topic = models.AutoField(primary_key = True, null = False)
    name_topic = models.CharField(max_length = 50, blank = False)
    type_topic = models.CharField(default="", max_length = 50, blank = False)
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
    slug_flashcard = models.SlugField(default = "", null = False)

    def save(self, *args, **kwargs):
        if not self.slug_flashcard:  
            self.slug_flashcard = slugify(self.front) 
        super().save(*args, **kwargs)

    def __str__(self):

        return f'{self.front}'
    
class User(models.Model):
    id_user = models.AutoField(primary_key= True, null=False)
    username = models.CharField(max_length=200, blank=False)
    slug_user = models.SlugField(null=False)

    def __str__(self):
        return f'{self.username}'
    
    def save(self, *args, **kwargs):
        if not self.slug_user:  
            self.slug_user = slugify(self.username) 
        super().save(*args, **kwargs)

class Study(models.Model):
    id_study = models.AutoField(primary_key=True, null=False)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug_study = models.SlugField(null=False)

    def __str__(self):
        return f'{self.id_study}'
    
    def save(self, *args, **kwargs):
        if not self.slug_study:  
            self.slug_study = slugify(f"{self.id_study}_{self.id_user.username}")
        super().save(*args, **kwargs)