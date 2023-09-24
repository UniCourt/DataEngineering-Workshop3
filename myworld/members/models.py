from django.db import models
  
BRANCH_CHOICES = (
   ("BA", "BA"),
   ("B.COM", "B.COM"),
   ("MBA", "MBA"),
   ("CA", "CA"),
)
        
# Create your models here.
class Students(models.Model):
   first_name = models.CharField(max_length=200)
   last_name = models.CharField(max_length=200)
   address = models.CharField(max_length=200)
   roll_number = models.IntegerField()
   mobile = models.CharField(max_length=10)
   branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, null=True)
        
   def __str__(self):
       return self.first_name + " " + self.last_name
        
class Blog(models.Model):
   title = models.CharField(max_length=500)
   release_date = models.DateTimeField('Realse Date')
   blog_time = models.CharField(max_length=50)
   author = models.CharField(max_length=200)
   cont_d=models.CharField(max_length=20000,default="Nothing")
   recommend=models.CharField(max_length=200,default="Nothing")
   created_date = models.DateTimeField('Created Date', auto_now_add=True, null=True)
            
   def __str__(self):                               
       return self.title
