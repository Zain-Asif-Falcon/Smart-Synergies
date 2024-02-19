from django.db import models
from django.contrib.auth.models import User 
class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"
    
class QuestionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    web_site_data= models.CharField(max_length=10000)
    chat_contest=models.CharField(max_length=10000)


    def __str__(self):
        return f"{self.user.username ,self.web_site_data}"
    
class Baseurl(models.Model):
    endpoint=models.CharField(max_length=10000)
    def __str__(self):
        return f'{self.endpoint}'
