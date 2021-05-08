from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    open_time = models.TimeField()
    close_time = models.TimeField()
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Booking(models.Model):

    book_id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()
    status = models.BooleanField(default=False)
    book_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status_remark = models.TextField()
    book_date = models.DateField()

    def __str__(self):
        return self.book_id,self.room_id,self.book_by




