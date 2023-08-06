from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from product_module.views import *
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly
from .serializers import *


class ProductAPIView(ModelViewSet):
    queryset = Product.objects.filter(is_active=True, is_delete=False)
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    # permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ["-created_date"]
    ordering = ['-created_date']

    # def get_queryset(self):
    #     queryset = super(ProductAPIView, self).get_queryset()
    #     print(queryset)
    #     print("--------------")
    #     count = self.request.query_params.get("count")
    #     if count:
    #         queryset = queryset[:2]
    #         print(queryset)
    #     return queryset
    # @action(detail=True, methods=['PATCH'], name='image')
    # def upload_image(self, request: HttpRequest, pk=None, *args, **kwargs):
    #     product = self.queryset.get(id=pk)
    #     serializer = self.serializer_class(partial=True, data=request.data, instance=product)
    #     serializer.is_valid(raise_exception=True)
    #     # print(serializer)
    #     image = serializer.validated_data.get("image")
    #     product.image = image
    #     product.save()
    #     return Response({"detail": "okab"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_delete = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductImageUploadView(APIView):
#     parser_class = (FileUploadParser,)
#
#     def post(self, request, *args, **kwargs):
#         file_serializer = ProductImageUploadSerializer(data=request.data)
#         if file_serializer.is_valid():
#             image = file_serializer.validated_data.get("image")
#             print(image)
#             return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCategoryAPIView(ModelViewSet):
    queryset = ProductCategory.objects.filter(is_active=True, is_delete=False, parent=None)
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {"title": ["exact"]}
    # ordering = ['-created_date"']


class ProductBrandAPIView(ModelViewSet):
    queryset = ProductBrand.objects.filter(is_active=True)
    serializer_class = ProductBrandSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {"title": ["exact"]}
    ordering = ['english_title']
