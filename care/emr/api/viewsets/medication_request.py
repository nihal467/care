from django_filters import rest_framework as filters

from care.emr.api.viewsets.base import EMRModelViewSet, EMRQuestionnaireResponseMixin
from care.emr.api.viewsets.encounter_authz_base import EncounterBasedAuthorizationBase
from care.emr.models.medication_request import MedicationRequest
from care.emr.registries.system_questionnaire.system_questionnaire import (
    InternalQuestionnaireRegistry,
)
from care.emr.resources.medication.request.spec import (
    MedicationRequestReadSpec,
    MedicationRequestSpec,
    MedicationRequestUpdateSpec,
)
from care.emr.resources.questionnaire.spec import SubjectType


class MedicationRequestFilter(filters.FilterSet):
    encounter = filters.UUIDFilter(field_name="encounter__external_id")


class MedicationRequestViewSet(
    EncounterBasedAuthorizationBase, EMRQuestionnaireResponseMixin, EMRModelViewSet
):
    database_model = MedicationRequest
    pydantic_model = MedicationRequestSpec
    pydantic_read_model = MedicationRequestReadSpec
    pydantic_update_model = MedicationRequestUpdateSpec
    questionnaire_type = "medication_request"
    questionnaire_title = "Medication Request"
    questionnaire_description = "Medication Request"
    questionnaire_subject_type = SubjectType.patient.value
    filterset_class = MedicationRequestFilter
    filter_backends = [filters.DjangoFilterBackend]

    def get_queryset(self):
        self.authorize_read_encounter()
        return (
            super()
            .get_queryset()
            .filter(patient__external_id=self.kwargs["patient_external_id"])
            .select_related("patient", "encounter", "created_by", "updated_by")
        )


MedicationRequestViewSet.generate_swagger_schema()
InternalQuestionnaireRegistry.register(MedicationRequestViewSet)
