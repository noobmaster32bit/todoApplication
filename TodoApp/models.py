from django.db import models

# Create your models here.

class Task(models.Model):
    title=models.CharField(max_length=200)
    user=models.CharField(max_length=200)
    options=(
        ("pending","pending"),
        ("completed","completed"),
        ("in progress","in progress")
    )
    status=models.CharField(max_length=200,choices=options,default="pending")
    created_date=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.title
    