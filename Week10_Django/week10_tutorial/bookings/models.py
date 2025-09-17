from django.db import models

class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RoomType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    description = models.TextField(blank=True)
    room_types = models.ManyToManyField(RoomType, related_name='rooms', blank=True)

    def __str__(self):
        return f'Room {self.number}: {self.name}'


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    staff = models.ForeignKey(Staff, on_delete=models.PROTECT)
    email = models.EmailField(null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    purpose = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Booking for {self.room} from {self.start_time} to {self.end_time}'