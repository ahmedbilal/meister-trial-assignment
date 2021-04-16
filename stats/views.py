import os
import logging
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    ListCreateAPIView,
)
from .serializers import (
    LoginSerializer,
    CountrySerializer,
    UserSerializer,
    SalesSerializer,
)
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .models import City, Country, Sale
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, Max

index_file_path = os.path.join(settings.REACT_APP_DIR, "build", "index.html")


def react(request):
    """
    A view to serve the react app by reading the index.html from the
    build  react app and serving it as a Httpresponse.
    """
    try:
        with open(index_file_path) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        logging.exception("Production build of app not found")


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        token, created = self.perform_create(serializer)
        return JsonResponse(
            {"token": token.key, "user_id": serializer.validated_data["user"].id}
        )

    def perform_create(self, serializer):
        return Token.objects.get_or_create(user=serializer.validated_data["user"])


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        token = get_object_or_404(Token, user=request.user)
        token.delete()
        return HttpResponse(status=200)


class UserView(RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user_id = kwargs.pop("pk")
        user = get_object_or_404(get_user_model(), id=user_id)
        return JsonResponse(
            {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "gender": user.gender,
                "age": user.age,
                "country": user.city.country.id,
                "city": user.city.id,
            }
        )


class CountryList(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class SaleView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Sale.objects.all()
    serializer_class = SalesSerializer

    def create(self, request, *args, **kwargs):
        data = request.data["sales_data"]
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        Sale.objects.filter(user=self.request.user).delete()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class StatisticsView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_user = request.user
        user_aggregate = (
            get_user_model()
            .objects.get(id=3)
            .sales.aggregate(
                total_revenue=Sum("revenue"),
                total_sales=Count("id"),
                highest_revenue=Max("revenue"),
            )
        )
        all_user_aggregate = (
            get_user_model()
            .objects.all()
            .aggregate(
                total_revenue=Sum("sales__revenue"), total_sales=Count("sales__id")
            )
        )

        highest_revenue_sale_for_current_user = (
            get_user_model()
            .objects.get(id=3)
            .sales.filter(revenue=user_aggregate["highest_revenue"])
            .first()
        )

        average_sales_for_current_user = (
            user_aggregate["total_revenue"] / user_aggregate["total_sales"]
        )
        average_sales_for_all_user = (
            all_user_aggregate["total_revenue"] / all_user_aggregate["total_sales"]
        )
        return JsonResponse(
            {
                "average_sales_for_current_user": average_sales_for_current_user,
                "average_sale_all_user": average_sales_for_all_user,
                "highest_revenue_sale_for_current_user": {
                    "sale_id": highest_revenue_sale_for_current_user.id,
                    "revenue": highest_revenue_sale_for_current_user.revenue,
                },
                "product_highest_revenue_for_current_user": {
                    "product_name": "Tape dispenser",
                    "price": 20,
                },
                "product_highest_sales_number_for_current_user": {
                    "product_name": "Tape dispenser",
                    "price": 432,
                },
            }
        )
