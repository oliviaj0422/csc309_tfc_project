from datetime import datetime, timedelta
from django.db import models

# Create your models here.
from django.db.models import CASCADE

from studios.models import Studio


def get_weekday(x):
    if x == 1:
        return 'Monday'
    if x == 2:
        return 'Tuesday'
    if x == 3:
        return 'Wednesday'
    if x == 4:
        return 'Thursday'
    if x == 5:
        return 'Friday'
    if x == 6:
        return 'Saturday'
    if x == 7:
        return 'Sunday'


class Class(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False,
                            unique=True)
    description = models.CharField(max_length=200, null=False, blank=False)
    coach = models.CharField(max_length=100, null=False, blank=False)
    keywords = models.CharField(max_length=200, null=False, blank=False)
    capacity = models.PositiveIntegerField(null=False, blank=False)
    start_time = models.DateTimeField(help_text='This is the start time of the first instance of this class.')
    duration = models.DurationField()
    end_time = models.DateTimeField(help_text='Every instance of this class ends before end time.')
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE)

    def __str__(self):
        return f'{self.name} in {self.studio.name} on {get_weekday(self.start_time.isoweekday())} from {self.start_time.strftime("%H:%M")} to {(self.start_time + self.duration).strftime("%H:%M")}'

    def save(self, *args, **kwargs):
        t1 = self.start_time
        t2 = self.end_time
        i = t1
        super(Class, self).save(*args, **kwargs)
        old_class_instances = ClassInstance.objects.filter(the_class=self)
        if old_class_instances:
            for old_instance in old_class_instances:
                old_instance.is_cancelled = True
                old_instance.save()
        while i < t2:
            ClassInstance.objects.create(the_class=self,
                                         space_availability=self.capacity,
                                         start_time=i,
                                         end_time=i + self.duration,
                                         coach=self.coach,
                                         description=self.description,
                                         keywords=self.keywords,
                                         class_name=self.name)
            i = i + timedelta(days=7)

    def get_class_name(self):
        return self.name


class ClassInstance(models.Model):
    the_class = models.ForeignKey(to=Class, on_delete=CASCADE)
    class_name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    coach = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    space_availability = models.PositiveIntegerField(null=False, blank=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.the_class.name} with id{self.id} in {self.the_class.studio.name} starting at {self.start_time.strftime("%H:%M")} on {self.start_time.strftime("%Y-%m-%d")} ({get_weekday(self.start_time.isoweekday())})'


class UserEnrolledClass(models.Model):
    user_id = models.PositiveIntegerField(null=False, blank=False)
    class_instance = models.ForeignKey(to=ClassInstance, on_delete=CASCADE)
    class_instance_name = models.CharField(max_length=200)
    class_instance_start_time = models.DateTimeField()
    class_instance_end_time = models.DateTimeField()
    def __str__(self):
        return f'user with id{self.user_id} has enrolled in class with id{self.class_instance.id}'
