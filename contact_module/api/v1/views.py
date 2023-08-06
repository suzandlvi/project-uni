from rest_framework.viewsets import ModelViewSet

from contact_module.api.v1.permissions import IsAdminOrCreateOnly
from contact_module.api.v1.serializers import ContactUsSerializer
from contact_module.models import ContactUs


class ContactUsAPIView(ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdminOrCreateOnly]

    # def create(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
