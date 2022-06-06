from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.alerts.models import ResolutionNote
from apps.alerts.tasks import send_update_resolution_note_signal
from apps.api.permissions import MODIFY_ACTIONS, READ_ACTIONS, ActionPermission, AnyRole, IsAdminOrEditor
from apps.api.serializers.resolution_note import ResolutionNoteSerializer, ResolutionNoteUpdateSerializer
from apps.auth_token.auth import PluginAuthentication
from common.api_helpers.mixins import PublicPrimaryKeyMixin, UpdateSerializerMixin


class ResolutionNoteView(PublicPrimaryKeyMixin, UpdateSerializerMixin, ModelViewSet):
    authentication_classes = (PluginAuthentication,)
    permission_classes = (IsAuthenticated, ActionPermission)

    action_permissions = {
        IsAdminOrEditor: MODIFY_ACTIONS,
        AnyRole: READ_ACTIONS,
    }

    model = ResolutionNote
    serializer_class = ResolutionNoteSerializer
    update_serializer_class = ResolutionNoteUpdateSerializer

    def get_queryset(self):
        alert_group_id = self.request.query_params.get("alert_group", None)
        lookup_kwargs = {}
        if alert_group_id:
            lookup_kwargs = {"alert_group__public_primary_key": alert_group_id}
        queryset = ResolutionNote.objects.filter(
            **lookup_kwargs,
            alert_group__channel__organization=self.request.auth.organization,
            alert_group__channel__team=self.request.user.current_team,
        )
        queryset = self.serializer_class.setup_eager_loading(queryset)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)

        # send signal to update alert group and resolution note
        method = request.method.lower()
        if method in ["post", "put", "patch", "delete"]:
            instance_id = self.kwargs.get("pk") or result.data.get("id")
            if instance_id:
                instance = ResolutionNote.objects_with_deleted.filter(public_primary_key=instance_id).first()
                if instance is not None:
                    send_update_resolution_note_signal.apply_async(
                        kwargs={
                            "alert_group_pk": instance.alert_group.pk,
                            "resolution_note_pk": instance.pk,
                        }
                    )
        return result