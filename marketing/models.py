from django.db import models
from post.models import Post

# Create your models here.
class SearchKeywords(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    keyword= models.CharField(max_length= 500)
    url= models.URLField(max_length= 250, blank=True, default='https://www.codethemall.com')

    def save(self, *args, **kwargs):
        self.url = 'https://www.codethemall.com'+self.post.get_absolute_url()
        super(SearchKeywords, self).save(*args, **kwargs)        

    def __str__(self):
        return "Keywords:"+self.post.title


class LinkSouces(models.Model):
    name= models.CharField(max_length= 100)
    hit_time= models.DateTimeField(auto_now_add= True)

    def save(self, *args, **kwargs):
        self.name= self.name.upper()
        super(LinkSouces, self).save(*args, **kwargs)
    def __str__(self):
        return "@" + self.name+str(self.hit_time) 