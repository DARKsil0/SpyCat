from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.response import Response
from .models import SpyCat, Mission, Target
from .serializers import (
    SpyCatSerializer,
    SpyCatUpdateSerializer,
    MissionCreateSerializer,
    TargetSerializer
)


class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all().order_by("name")

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return SpyCatUpdateSerializer
        return SpyCatSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.prefetch_related("targets").select_related("cat").all()
    serializer_class = MissionCreateSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat_id:
            return Response(
                {"detail": "Cannot delete a mission that is already assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @transaction.atomic
    @action(detail=True, methods=["post"], url_path="assign-cat")
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        cat_id = request.data.get("cat_id")

        if not cat_id:
            return Response({"detail": "cat_id is required"}, status=400)

        from .models import SpyCat
        try:
            cat = SpyCat.objects.get(pk=cat_id)
        except SpyCat.DoesNotExist:
            return Response({"detail": "Cat not found"}, status=404)

        if cat.missions.filter(is_complete=False).exists():
            return Response({"detail": "This cat already has an active mission."}, status=400)

        if mission.cat_id:
            return Response({"detail": "Mission already has a cat assigned."}, status=400)

        mission.cat = cat
        mission.save(update_fields=["cat"])
        return Response(MissionCreateSerializer(mission).data)


class TargetViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = Target.objects.select_related("mission").all()
    serializer_class = TargetSerializer

