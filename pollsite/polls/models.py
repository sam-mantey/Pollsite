from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib import admin
import datetime



# Create your models here.



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    @admin.display(
        boolean= True,
        ordering = "pub_date",
        description = "Published recently?",
    )

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return timezone.now() + datetime.timedelta(1) >=  self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text