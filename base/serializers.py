from rest_framework import serializers
from django.db.models import Avg
from .models import Project, ActualFloor, Floor, Block, Zone, Video


class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block
        fields = ("block_name",)


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ("zone_name",)


class FloorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Floor
        fields = ("floor_name",)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    average_percentage = serializers.SerializerMethodField()
    projectfloors = FloorSerializer(read_only=True, many=True)
    projectblocks = BlockSerializer(read_only=True, many=True)
    projectzones = ZoneSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = ("url", "id", "project_name", "manager_name", "start_date",
                  "due_date", "average_percentage", "projectblocks", "projectzones", "projectfloors",)

    def get_average_percentage(self, obj):
        related_model_as = ActualFloor.objects.filter(project=obj)
        average = related_model_as.aggregate(Avg('actual_progress_percentage'))[
            'actual_progress_percentage__avg']
        return average


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'title', 'date_collected', 'video', 'created')
