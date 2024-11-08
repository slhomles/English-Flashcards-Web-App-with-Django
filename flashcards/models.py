from django.db import models

# Tạo các mô hình của bạn ở đây.
class Topic(models.Model):
    id_topic = models.AutoField(primary_key=True, null=False)
    name_topic = models.CharField(max_length=50, blank=False)
    slug_topic = models.SlugField(default="", null=False)
    image_topic = models.ImageField(upload_to='images/', max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.name_topic}'

class Flashcards(models.Model):
    id_flashcard = models.AutoField(primary_key=True, null=False)
    front = models.CharField(max_length=200, blank=False)
    back = models.CharField(max_length=300, blank=False)
    id_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    slug_topic = models.SlugField(default="", null=False)
    slug_flashcard = models.SlugField(default="", null=False)

    def __str__(self):
        return f'{self.front}'
