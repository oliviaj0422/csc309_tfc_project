from django.db import models


# Create your models here.


class Class(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    coach = models.CharField(max_length=100, null=False, blank=False)
    keywords = models.CharField(max_length=200, null=False, blank=False)
    capacity = models.PositiveIntegerField(null=False, blank=False)
    # the start time of the first instance of this class
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    studio = models.CharField(max_length=100, null=False, blank=False,
                              default="studio")

    def __str__(self):
        return f'{self.name} in {self.studio}'


class ClassInstance(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    coach = models.CharField(max_length=100, null=False, blank=False)
    keywords = models.CharField(max_length=200, null=False, blank=False)
    capacity = models.PositiveIntegerField(null=False, blank=False)
    space_availability = models.PositiveIntegerField(null=False, blank=False)
    # the start date of the first instance of this class
    start_time = models.DateTimeField()
    duration = models.DurationField()
    studio = models.CharField(max_length=100, null=False, blank=False)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} in {self.studio} starting on {self.start_time}'

    def get_duration(self):
        seconds = self.duration.total_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return '{} minutes, {} hours'.format(minutes, hours)

    def get_class_info(self):
        return {"id": self.id,
                "name": self.name, "description": self.description,
                "coach": self.coach, "keywords": self.keywords,
                "capacity": self.capacity,
                "space availability": self.space_availability,
                "start time": self.start_time.date(),
                "duration": self.get_duration(),
                "is cancelled": self.is_cancelled}


class UserEnrolledClass(models.Model):
    user_id = models.PositiveIntegerField(null=False, blank=False)
    class_id = models.PositiveIntegerField(null=False, blank=False)
    def __str__(self):
        return f'user with id{self.user_id} has enrolled in class with id{self.class_id}'
