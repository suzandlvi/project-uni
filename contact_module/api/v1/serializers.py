from rest_framework import serializers

from contact_module.models import ContactUs
from utils.normalize_email import normalize_email


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"

    def validate(self, attrs):
        attrs["email"] = normalize_email(attrs["email"])
        user_contacts = len(ContactUs.objects.filter(email__iexact=attrs.get("email"), is_read_by_admin=False))
        if user_contacts > 5:
            raise serializers.ValidationError("شما باید منتظر خوانده شدن تیکت های قبلی تان بمانید", code="bad_request")
        return attrs

