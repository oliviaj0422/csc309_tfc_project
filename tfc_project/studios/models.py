from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class Studio(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name = 'Studio Name',unique=True)
    address = models.TextField(max_length=500, verbose_name = 'Studio Address',
                               help_text = 'Please seperate street name, city, and province by comma.')
    geolocation = models.TextField(max_length=500, verbose_name = 'longitude, latitude',
                                   help_text = 'Please seperate longitude and latitude by '
                                               'comma. Eg. 55.854261,-4.234524')
    postalcode = models.CharField(max_length=7, verbose_name = 'Postal Code',
                                  help_text = 'Eg. M5S 1C6')
    phonenumber = models.CharField(max_length=10, verbose_name = 'Phone Number',
                                   help_text = 'Eg. 6471231230')
    amenitiestype = models.TextField(max_length=500, verbose_name = 'Amenities Type',
                                     help_text = 'Please enter amenity\'s type.'
                                                 'Seperate each integer by comma.')
    amenitiesquantity = models.TextField(max_length=500, verbose_name = 'Amenities Quantity',
                                         help_text = 'Please correspond to each amenity\'s type. '
                                                     'Seperate each integer by comma.')
    imagelist = models.TextField(blank=True, null=True, verbose_name = 'Link of Images',
                                 help_text = 'Please seperate each image by comma.')

    def __repr__(self):
        return f"<{self.name}, {self.address}, {self.geolocation}>"

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        for attr in ['id', 'name', 'address', 'geolocation', 'postalcode', 'phonenumber', 'amenitiestype','amenitiesquantity','imagelist']:
            yield attr, getattr(self, attr)
