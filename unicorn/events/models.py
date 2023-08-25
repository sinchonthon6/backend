from django.db import models

# Create your models here.
class Event(models.Model):
    SCHOOLS = (
        ('홍익대', '홍익대'),
        ('서강대', '서강대'),
        ('연세대', '연세대'),
        ('이화여대', '이화여대')
    )
    CATEGORIES = (
        ('밴드', '밴드'),
        ('댄스', '댄스'),
        ('전시', '전시'),
        ('연극', '연극'),
        ('스포츠', '스포츠'),
        ('기타', '기타'),

    )
    circle_name=models.CharField(max_length=50)
    title=models.CharField(max_length=100)
    school=models.CharField(max_length=20,choices=SCHOOLS)
    img=models.ImageField(null=True, blank=True)
    img_detail_1=models.ImageField(null=True, blank=True)
    img_detail_2=models.ImageField(null=True, blank=True)
    category=models.CharField(max_length=20,choices=CATEGORIES)
    start_day=models.DateField()
    finish_day=models.DateField()
    start_day=models.TimeField()
    long=models.CharField(max_length=50)
    pay= models.CharField(max_length=50)
    detail=models.TextField()
    contact= models.CharField(max_length=500)
    
    def __str__(self):
        return "{}: {} - {}".format(self.id,self.title,self.school)