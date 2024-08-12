from typing import Any

from rest_framework.exceptions import APIException
from rest_framework.serializers import (
    CharField,
    ChoiceField,
    IntegerField,
    ListField,
    Serializer,
    UUIDField,
)

from care.utils.queryset.consultation import get_consultation_queryset


class LinkCarecontextSerializer(Serializer):
    consultations = ListField(child=UUIDField(), required=True)

    def validate(self, attrs: Any) -> Any:
        consultation_instances = get_consultation_queryset(
            self.context["request"].user
        ).filter(external_id__in=attrs["consultations"])

        if consultation_instances.count() != len(attrs["consultations"]):
            raise APIException(
                detail="You do not have access to one or more consultations"
            )

        attrs["consultations"] = consultation_instances
        return super().validate(attrs)


class TokenOnGenerateTokenSerializer(Serializer):
    class ResponseSerializer(Serializer):
        requestId = UUIDField()

    abhaAddress = CharField(max_length=50, required=True)
    linkToken = CharField(max_length=1000, required=True)
    response = ResponseSerializer(required=True)


class LinkOnCarecontextSerializer(Serializer):
    class ResponseSerializer(Serializer):
        requestId = UUIDField()

    abhaAddress = CharField(max_length=50, required=True)
    status = CharField(max_length=1000, required=True)
    response = ResponseSerializer(required=True)


class HipPatientCareContextDiscoverSerializer(Serializer):
    class PatientSerializer(Serializer):
        class IdentifierSerializer(Serializer):
            type = ChoiceField(choices=["MOBILE", "ABHA_NUMBER", "MR"], required=True)
            value = CharField(max_length=255, required=True)

        id = CharField(max_length=50, required=True)
        name = CharField(max_length=100, required=True)
        gender = ChoiceField(choices=["M", "F", "O"], required=True)
        yearOfBirth = IntegerField(required=True)
        verifiedIdentifiers = IdentifierSerializer(many=True, required=True)
        unverifiedIdentifiers = IdentifierSerializer(many=True, required=True)

    transanctionId = UUIDField(required=True)
    patient = PatientSerializer(required=True)


class HipLinkCareContextInitSerializer(Serializer):
    class PatientSerializer(Serializer):
        class CareContextSerializer(Serializer):
            referenceNumber = CharField(max_length=50, required=True)

        referenceNumber = CharField(max_length=50, required=True)
        careContexts = CareContextSerializer(many=True, required=True)
        hiType = ChoiceField(
            choices=[
                "PRESCRIPTION",
                "DIAGNOSTIC_REPORT",
                "OP_CONSULTATION",
                "DISCHARGE_SUMMARY",
                "IMMUNIZATION_RECORD",
                "RECORD_ARTIFACT",
                "WELLNESS_RECORD",
            ],
            required=True,
        )
        count = IntegerField(required=True)

    transanctionId = UUIDField(required=True)
    abhaAddress = CharField(max_length=50, required=True)
    patient = PatientSerializer(many=True, required=True)


class HipLinkCareContextConfirmSerializer(Serializer):
    class ConfirmationSerializer(Serializer):
        linkRefNumber = CharField(max_length=50, required=True)
        token = CharField(max_length=20, required=True)

    confirmation = ConfirmationSerializer(required=True)