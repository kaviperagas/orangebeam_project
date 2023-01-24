from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# status = (
#     ('1', 'Working'),
#     ('2', 'Stuck'),
#     ('3', 'Done'),
# )

# due = (
#     ('1', 'On Due'),
#     ('2', 'Overdue'),
#     ('3', 'Done'),
# )


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=255)
    # block_num = models.PositiveIntegerField(default=1)
    # zone_num = models.PositiveIntegerField(default=1)
    # floor_num = models.PositiveIntegerField(default=1)
    start_date = models.DateField()
    due_date = models.DateField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta():
        ordering = ['pk', '-updated', '-created']

    def __str__(self):
        return self.project_name


class Block(models.Model):
    project = models.ForeignKey(
        Project, related_name='projectblocks', on_delete=models.CASCADE)
    block_name = models.CharField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pk', '-updated', '-created']

    def __str__(self):
        return (self.block_name)


class Zone(models.Model):
    project = models.ForeignKey(
        Project, related_name='projectzones', on_delete=models.CASCADE)
    # block = models.ForeignKey(Block, on_delete=models.CASCADE)
    zone_name = models.CharField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pk', '-updated', '-created']

    def __str__(self):
        return (self.zone_name)


class Floor(models.Model):
    project = models.ForeignKey(
        Project, related_name='projectfloors', on_delete=models.CASCADE)
    # block = models.ForeignKey(Block, on_delete=models.CASCADE)
    floor_name = models.CharField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pk', '-updated', '-created']

    def __str__(self):
        return (self.floor_name)


class TargetFloor(models.Model):
    project = models.ForeignKey(
        Project, related_name='targetfloors', on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    target_floor_cycle = models.PositiveIntegerField(default=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['floor__pk', '-updated', '-created']

    def __str__(self):
        return str(self.target_floor_cycle)


class ActualFloor(models.Model):
    project = models.ForeignKey(
        Project, related_name='actualfloors', on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    actual_floor_cycle = models.PositiveIntegerField(default=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['floor__pk', '-updated', '-created']

    def __str__(self):
        return str(self.actual_floor_cycle)
