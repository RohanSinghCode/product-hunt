from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class product(models.Model):
    title = models.TextField(max_length=255)
    url = models.TextField()
    pub_date = models.DateField()
    image = models.ImageField(upload_to='product_images/' ,default='default/default.jpg')
    votes_total = models.IntegerField(default=1)
    body=models.TextField()
    hunter = models.ForeignKey(User,on_delete=models.CASCADE,default="")


    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b &e %y')


