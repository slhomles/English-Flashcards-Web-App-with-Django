from django.db import models
from django.template.defaultfilters import default
from django.utils.text import slugify
from django.contrib.auth.models import User

# pip install google-cloud-texttospeech trước khi chạy

# Tạo các mô hình của bạn ở đây.
class Topic(models.Model):
    id_topic = models.AutoField(primary_key = True, null = False)
    name_topic = models.CharField(max_length = 50, blank = False)
    type_topic = models.CharField(max_length = 50, blank = False)
    slug_topic = models.SlugField(null=False, blank=True)
    image_topic = models.ImageField(upload_to='images/', max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug_topic:  
            self.slug_topic = slugify(self.name_topic)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.slug_topic}'

class Flashcards(models.Model):
    # API của Oxford
    APP_ID = '47f410f8'
    #APP_KEY = '23a4a9cf486e0911da092affc9950027'
    #APP_KEY = '80e49be87fe00754fcc59ff73d2a4095'
    APP_KEY = '6f4af303716548eb1af2998329cf76b0'
    #APP_KEY = '36cecd6cac61f7573a32d40d677a778e'
    # Chọn một trong các key trên

    # Merriam-Webster Dictionary API
    # KEY: "959a4e11-8731-4fbd-bd13-ec72c0a16405"

    id_flashcard = models.AutoField(primary_key= True, null = False)
    front = models.CharField(max_length = 200, blank = False)
    back = models.CharField(max_length = 300, blank = False)
    id_topic = models.ForeignKey(Topic,on_delete = models.CASCADE )
    slug_flashcard = models.SlugField(null=False, blank=True)
    pronunciation = models.URLField(blank=True, null=False)
    spell = models.CharField(max_length=100, blank=True, null=False)

    def save(self, *args, **kwargs):
        if not self.slug_flashcard:  
            self.slug_flashcard = slugify(self.front) 
        if not self.pronunciation:
            # sử dụng api của oxford
            #pronunciation_url = self.get_pronunciation(self.front)
            # sử dụng api của responsivevoice
            pronunciation_url = self.speak_word(self.front)
            if pronunciation_url:
                self.pronunciation = pronunciation_url
                # self.pronunciation = pronunciation_url[0] nếu của oxford
        if not self.spell:
            spell_word = self.get_spell(self.front)
            if spell_word:
                self.spell = spell_word
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.front}'
    
    @staticmethod
    def get_pronunciation(word):
        url = f"https://od-api-sandbox.oxforddictionaries.com/api/v2/entries/en-gb/{word.lower()}"

        response = requests.get(url, headers={"app_id": '47f410f8', "app_key": '6f4af303716548eb1af2998329cf76b0'})
        print(f"Response Status Code: {response.status_code}")

        if response.status_code == 200:  # Mã trạng thái HTTP 200 nghĩa là yêu cầu thành công
            data = response.json()
            #print("API Response Data:", json.dumps(data, indent=2))
            
            pronunciations = []  # Khởi tạo danh sách chứa các file phát âm
            
            # Duyệt qua dữ liệu để trích xuất thông tin về phát âm
            for entry in data.get('results', []):  # Lấy tất cả các kết quả
                for lexicalEntry in entry.get('lexicalEntries', []):  # Duyệt qua các dạng từ
                    # Truy cập vào phần entries, nơi chứa thông tin chi tiết
                    for lex_entry in lexicalEntry.get('entries', []):
                        for pronunciation in lex_entry.get('pronunciations', []):  # Duyệt qua các phát âm
                            # Kiểm tra nếu có file âm thanh
                            if 'audioFile' in pronunciation:
                                pronunciations.append(pronunciation['audioFile'])  # Thêm URL âm thanh vào danh sách                        
            return pronunciations
        else:
            return None
        
    @staticmethod
    def get_spell(word):
        url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={"959a4e11-8731-4fbd-bd13-ec72c0a16405"}"
    
        response = requests.get(url)
        print(f"Response Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data:
                spell = data[0].get('hwi', {}).get('prs', [{}])[0].get('mw', '')   
                return spell
            else:
                print(f"No results found for '{word}'")
                return None
        else:
            print(f"Error: {response.status_code}")
            return None
        
    @staticmethod
    def speak_word(word):
        url = f"https://code.responsivevoice.org/getvoice.php?t={word}&tl=en&sv=&vn=&pitch=0.5&rate=0.5&vol=1&key=mMBcmGky"
        response = requests.get(url)

        if response.status_code == 200:
            return url
        else:
            None

    def __str__(self):
        return f'{self.front}'
class Study(models.Model):
    id_study = models.AutoField(primary_key=True, null=False)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug_study = models.SlugField(null=False, blank=True)

    def __str__(self):
        return f'{self.id_study}'
    
    def save(self, *args, **kwargs):
        if not self.slug_study:  
            self.slug_study = slugify(f"{self.id_study}_{self.id_user.username}")
        super().save(*args, **kwargs)
    
