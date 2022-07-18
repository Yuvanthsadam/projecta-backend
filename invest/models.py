from django.db import models
from django.utils.timezone import now
from accounts.models import User



class IdeasConnection(models.Model):

    department_types_choice = (
        ('A', 'Category 1'),
        ('B', 'Category 2')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=100,blank=False)
    description=models.CharField(max_length=255,default="")
    open_invester=models.BooleanField("Open for Investors",default=False)
    open_collaboration=models.BooleanField("Open for Collaboration",default=False)
    sell_idea=models.BooleanField("Sell Idea",default=False)
    budget=models.CharField(max_length=100,default="")
    department_types= models.CharField(choices=department_types_choice, max_length=2,default=False) #dropdown
    patent_no = models.IntegerField()
    serial_no = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class savedIdeas(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    ideaId=models.ForeignKey(IdeasConnection,on_delete=models.CASCADE)