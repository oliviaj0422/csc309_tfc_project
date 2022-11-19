from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class Studio(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    geolocation = models.TextField(max_length=500)
    postalcode = models.CharField(max_length=7)
    phonenumber = models.CharField(max_length=100)
    amenitiestype = models.TextField(max_length=500)
    amenitiesquantity = models.TextField(max_length=500)
    imagelist = models.TextField(blank=True, null=True)

    def __repr__(self):
        return f"<{self.name}, {self.address}, {self.geolocation}>"

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        for attr in ['id', 'name', 'address', 'geolocation', 'postalcode', 'phonenumber', 'amenitiestype','amenitiesquantity','imagelist']:
            yield attr, getattr(self, attr)
