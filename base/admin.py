from django.contrib import admin

# Register your models here.

from .models import Project, Block, Zone, Floor, TargetFloor, ActualFloor

# username : admin
# password : orangebeam

admin.site.register(Project)
admin.site.register(Block)
admin.site.register(Zone)
admin.site.register(Floor)
admin.site.register(TargetFloor)
admin.site.register(ActualFloor)
