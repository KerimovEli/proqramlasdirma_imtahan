from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=20)
    slug = models.SlugField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title

# Tag modeli 
class Tag(models.Model): 
    name = models.CharField(max_length=50, unique=True) 
    slug = models.SlugField(unique=True) 
 
    def __str__(self): 
        return self.name 

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Yaradılma tarixi 
    updated = models.DateTimeField(auto_now=True)  # YENİ - Son editlənmə tarixi
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    def __str__(self):
        return self.title

class About(models.Model):
    title = models.CharField(max_length=200, default="Haqqımızda") 
    content = models.TextField() 
    image = models.ImageField(upload_to='about/', blank=True, null=True) 
    email = models.EmailField(blank=True, null=True) 
    phone = models.CharField(max_length=20, blank=True, null=True) 
    address = models.TextField(blank=True, null=True) 
    updated = models.DateTimeField(auto_now=True) 
     
    class Meta: 
        verbose_name = "About Page" 
        verbose_name_plural = "About Page" 
     
    def __str__(self): 
        return self.title 
    
class Like(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, 
related_name='likes') 
    timestamp = models.DateTimeField(auto_now_add=True) 
 
    class Meta: 
        unique_together = ('user', 'post')  # user bir postu yalnız bir dəfə like edə bilər 
 
    def __str__(self): 
        return f"{self.user.username} likes {self.post.title}" 
    
class Dislike(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, 
related_name='dislikes') 
    timestamp = models.DateTimeField(auto_now_add=True) 
 
    class Meta: 
        unique_together = ('user', 'post')  # user bir postu yalnız bir dəfə dislike edə bilər 
 
    def __str__(self): 
        return f"{self.user.username} dislikes {self.post.title}" 

class Comment(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, 
related_name='comments') 
    content = models.TextField() 
    timestamp = models.DateTimeField(auto_now_add=True) 
 
    class Meta: 
        ordering = ['-timestamp'] # ən yeni comment yuxarıda 
 
    def __str__(self): 
        return f"{self.user.username} - {self.post.title}" 
    
class Report(models.Model): 
    """Post üçün Report (Şikayət) modeli""" 
 
    REPORT_REASONS = [ 
        ('inappropriate', 'Uyğun olmayan məzmun'), 
        ('spam', 'Spam'), 
        ('offensive', 'Təhqiredici/Saldırğan'), 
        ('misinformation', 'Yanlış məlumat'), 
        ('copyright', 'Müəlliflik hüququ ihlali'), 
        ('other', 'Digər səbəb'), 
    ] 
 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, 
related_name='reports') 
    reporter_name = models.CharField(max_length=100) 
    reporter_email = models.EmailField() 
    reason = models.CharField(max_length=20, choices=REPORT_REASONS) 
    description = models.TextField(blank=True, null=True) 
    timestamp = models.DateTimeField(auto_now_add=True) 
    is_resolved = models.BooleanField(default=False) 
 
    class Meta: 
        ordering = ['-timestamp'] 
        unique_together = ('post', 'reporter_email') # Eyni kişi iki dəfə report etməsin 
 
    def __str__(self): 
        return f"{self.post.title} - {self.reporter_name}" 
    
class View(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, 
blank=True)  # anonim userlər üçün null 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, 
related_name='views') 
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # IP ilə izləmək üçün 
    timestamp = models.DateTimeField(auto_now_add=True) 
 
    def __str__(self): 
        return f"View on {self.post.title}" 