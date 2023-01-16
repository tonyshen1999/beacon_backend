"""beacon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from . import views,calcviews
from rest_framework import routers



router = routers.DefaultRouter()
router.register(r'periods', views.PeriodViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("pd/",views.periodAPI),
    path("pd/<str:period>/",views.PeriodDetailAPIView.as_view()),
    
    # path("scn/",views.ScenarioListCreateAPIView.as_view()),
    path("scn/",views.scenariosAPI),
    path("scn/<int:pk>",views.ScenarioDetailAPIView.as_view()),

    path("entity/",views.entityAPI),
    path("entity/<int:pk>",views.EntityDetailAPIView.as_view()),


    path("atr/",views.AttributeListCreateAPIView.as_view()),
    path("atr/<int:pk>",views.AttributeDetailAPIView.as_view()),

    path("acc/",views.accountAPI),
    path("acc/<int:pk>",views.AccountDetailAPIView.as_view()),

    path("adj/",views.adjustmentAPI),
    path("adj/<int:pk>",views.AdjustmentDetailAPIView.as_view()),

    path("calc/",calcviews.calculate),
    # url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
