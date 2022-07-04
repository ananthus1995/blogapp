from django.db import models
from django.contrib.auth.models import User

class Blogs(models.Model):
    title = models.CharField(max_length=65)
    content = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')
    blog_img=models.ImageField(upload_to='blogs_pic', null=True)
    posted_date=models.DateTimeField(auto_now_add=True,null=True)
    likes=models.ManyToManyField(User)
    def __str__(self):
        return self.title
    
class Comments(models.Model):
    blog=models.ForeignKey(Blogs, on_delete=models.CASCADE)
    comments=models.CharField(max_length=50)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='users')
    bio=models.CharField(max_length=20,null=True)
    phone=models.CharField(max_length=10,null=True)