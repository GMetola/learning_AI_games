from django.db import models

# Create your models here.
# Note to self: models are just the objects of the application! They will end as database fields.

class Village(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Resource(models.Model):
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='Wood')
    number = models.IntegerField(default=800)
    production = models.IntegerField(default=10)
    negative = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.name)

class Check(models.Model):
    date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
