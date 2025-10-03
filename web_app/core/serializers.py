from rest_framework import serializers
from .models import SpyCat, Mission, Target
from .validators import validate_breed_id


class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = [
            "id",
            "name",
            "years_experience",
            "breed_id",
            "salary",
        ]
        read_only_fields = ["id"]

    def validate_breed_id(self, value):
        return validate_breed_id(value)

class SpyCatUpdateSerializer(serializers.ModelSerializer):
    """Serializer restricted to salary updates only."""

    class Meta:
        model = SpyCat
        fields = [
            "id",
            "name",
            "years_experience",
            "breed_id",
            "salary",
        ]

        read_only_fields = [
            "id",
            "name",
            "years_experience",
            "breed_id",
        ]


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["id", "name", "country", "notes", "is_complete", "mission"]
        read_only_fields = ["id", "mission"]

    def validate(self, data):
        target = self.instance
        if target:
            mission = target.mission

            if mission.is_complete:
                raise serializers.ValidationError("Mission is complete. Targets cannot be updated.")

            if target.is_complete and "notes" in data:
                raise serializers.ValidationError("Target is complete. Notes cannot be updated.")

        return data

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        mission = instance.mission
        if not mission.is_complete:
            all_done = not mission.targets.filter(is_complete=False).exists()
            if all_done:
                mission.is_complete = True
                mission.save(update_fields=["is_complete"])

        return instance



class MissionCreateSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ["id", "cat", "is_complete", "targets"]
        read_only_fields = ["id", "is_complete"]

    def validate(self, data):
        targets = data.get("targets", [])
        if not (1 <= len(targets) <= 3):
            raise serializers.ValidationError("Mission must have between 1 and 3 targets.")

        cat = data.get("cat")
        if cat and cat.missions.filter(is_complete=False).exists():
            raise serializers.ValidationError("This cat already has an active mission.")

        return data

    def create(self, validated_data):
        targets_data = validated_data.pop("targets")
        mission = Mission.objects.create(**validated_data)
        for t in targets_data:
            Target.objects.create(mission=mission, **t)
        return mission


