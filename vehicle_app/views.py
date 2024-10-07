from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_503_SERVICE_UNAVAILABLE, HTTP_201_CREATED, \
    HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import ScopedRateThrottle
from .models import Brand, Car
import requests
from .serializers import BrandNameSerializer, CarSerializer, MakeSerializer, RegisterSerializer, BrandSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated


class CustomPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'results': data,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
        })


class BrandNameAPIView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'brand_throttle'
    permission_classes = [IsAuthenticatedOrReadOnly]  # Authenticated users can view; others can read

    def get(self, request, *args, **kwargs):
        brands = Brand.objects.all()

        if not brands.exists():
            return Response(
                {"error": "No brands found."},
                status=HTTP_404_NOT_FOUND
            )

        serializer = BrandNameSerializer(brands, many=True)
        filtered_data = [{'page_name': item['page_name']} for item in serializer.data]

        return Response(filtered_data, status=HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = BrandNameSerializer(data=request.data)
        if serializer.is_valid():
            brand = serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        brand = Brand.objects.filter(page_id=kwargs['page_id']).first()

        if brand:
            # Update the existing brand with request data
            serializer = BrandNameSerializer(brand, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        return Response({"error": "Brand not found."}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        page_id = kwargs.get('page_id')

        if not page_id:
            return Response({"error": "page_id not provided."}, status=HTTP_400_BAD_REQUEST)

        brand = Brand.objects.filter(page_id=page_id).first()

        if brand:
            brand.delete()
            return Response(status=HTTP_204_NO_CONTENT)

        return Response({"error": "Brand not found."}, status=HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        page_id = kwargs.get('page_id')

        if not page_id:
            return Response({"error": "page_id not provided."}, status=HTTP_400_BAD_REQUEST)

        brand = Brand.objects.filter(page_id=page_id).first()

        if brand:
            serializer = BrandNameSerializer(brand, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        return Response({"error": "Brand not found."}, status=HTTP_404_NOT_FOUND)


class CarListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        brand_name = request.query_params.get('brand', None)
        permission_classes = [IsAuthenticated]

        if brand_name:
            cars = Car.objects.filter(brand__page_name__icontains=brand_name)
        else:
            cars = Car.objects.all()

        if not cars.exists():
            return Response(
                {"error": "No cars found."},
                status=HTTP_404_NOT_FOUND
            )

        paginator = CustomPagination()
        paginated_cars = paginator.paginate_queryset(cars, request)
        serializer = CarSerializer(paginated_cars, many=True)

        response_data = paginator.get_paginated_response(serializer.data)

        return Response(response_data.data, status=HTTP_200_OK)


class ExternalVehicleListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        external_url = 'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/all-vehicles-model/records' \
                       '/?limit=100 '
        external_response = requests.get(external_url)

        if external_response.status_code != 200:
            return Response({"error": "Failed to fetch vehicle data"}, status=HTTP_503_SERVICE_UNAVAILABLE)

        data = external_response.json()
        results = data.get('results', [])
        makes = [{'make': record['make']} for record in results if 'make' in record]

        if not makes:
            return Response({"error": "No makes found in the data."}, status=HTTP_404_NOT_FOUND)

        paginator = CustomPagination()
        paginated_makes = paginator.paginate_queryset(makes, request)

        return paginator.get_paginated_response(MakeSerializer(paginated_makes, many=True).data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class BrandCreateAPIView(generics.CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]
