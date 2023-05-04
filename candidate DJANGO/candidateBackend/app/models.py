from django.db import models

class Candidate(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    description = models.TextField()
    cv = models.FileField(upload_to='cv/')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
