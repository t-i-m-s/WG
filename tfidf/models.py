from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=50, unique=True)  # само слово
    tf_last = models.IntegerField()  # встреч в последнем документе
    met_count = models.IntegerField()  # в скольки документах встретилось

    def __str__(self):
        return self.word
