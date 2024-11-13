from django.db import models
from django.template.defaultfilters import default
from django.utils.text import slugify
import requests

# Create your models here.

APP_ID = '47f410f8'
APP_KEY = '23a4a9cf486e0911da092affc9950027'
#APP_KEY = '872f89f5330a2b53e421133556098eb2'
#APP_KEY = '80e49be87fe00754fcc59ff73d2a4095'
#APP_KEY = '6f4af303716548eb1af2998329cf76b0'
#APP_KEY = '36cecd6cac61f7573a32d40d677a778e'
# Chọn một trong các key trên

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
    slug_flashcard = models.SlugField(null = False)
    pronunciation = models.URLField(blank=False, null=False)

    def save(self, *args, **kwargs):
        if not self.slug_flashcard:  
            self.slug_flashcard = slugify(self.front) 
        if not self.pronunciation:
            pronunciation_urls = self.get_pronunciation(self.front)
            if pronunciation_urls:
                self.pronunciation = pronunciation_urls[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.front}'
    
    @staticmethod
    def get_pronunciation(word):
        url = f'https://od-api-sandbox.oxforddictionaries.com/api/v2/{word.lower()}'
        headers = {
            'app_id': APP_ID,
            'app_key': APP_KEY
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200: # Mã trạng thái HTTP 200 nghĩa là yêu cầu được xử lý thành công và trả về kết quả
            data = response.json()
            # Truy cập vào phần pronunciations
            pronunciations = []
            for entry in data.get('results', []): # API của Oxford trả về dữ liệu dưới dạng một chuỗi các kết quả được lưu trữ trong mục 'results'
                for lexicalEntry in entry.get('lexicalEntries', []): # lexicalEntry: đại diện cho dạng từ (động từ, danh từ, ...)
                    for pronunciation in lexicalEntry.get('pronunciations', []): # mỗi từ có thể có nhiều cách phát âm, ví dụ: phát âm Anh-Anh, phát âm Anh-Mỹ, ...
                        if 'audioFile' in pronunciation: # 'audioFile' chứa URL tới file âm thanh của phát âm từ
                            pronunciations.append(pronunciation['audioFile'])
            return pronunciations  # Trả về danh sách các file âm thanh phát âm
        else:
            return None
        
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