from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import InvoiceViewSet


router = routers.DefaultRouter()
router.register(r'invoice', InvoiceViewSet)

urlpatterns = [
    path('panel/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]
