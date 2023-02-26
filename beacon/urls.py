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

from . import views,calcviews,importviews,functionviews,logviews
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
    path("scn-list/",views.scenarioListAPI),

    path("scn/version/",functionviews.new_version),

    path("entity/",views.entityAPI),
    path("entity/<int:pk>",views.EntityDetailAPIView.as_view()),

    path("revert/", functionviews.revert_version),
    path("atr/",views.attributeAPI),
    path("atr/<int:pk>",views.AttributeDetailAPIView.as_view()),
    path("def-atr/",views.defaultAttributesAPI),
    path("acc/",views.accountAPI),
    path("acc/<int:pk>",views.AccountDetailAPIView.as_view()),

    path("adj/",views.adjustmentAPI),
    path("adj/<int:pk>",views.AdjustmentDetailAPIView.as_view()),

    path("rel/",views.relationshipAPI),
    path("rel/<int:pk>",views.AdjustmentDetailAPIView.as_view()),

    path("calc/",calcviews.calculate),
    path("calc-script/",calcviews.calc_script),
    path("clear-calc/",calcviews.clear_calc),
    path("clear-data/",calcviews.clear_data),   
    path("import/",importviews.importTables),

    path("atr-type/",importviews.attributeScenarioTypes),
    path("atr-filter/",importviews.filterAttributes),

    path("scn-notes/",functionviews.scenario_notes),

    path("clone-scn/",functionviews.clone_scenario),
    path("delete-scn/",functionviews.delete_scenario),

    path("push-custom-atr/",importviews.customAttributes),
    path("calc-log-list/",logviews.calcLogListAPI),

    path("import-log/",logviews.importLogAPI),

    path("log/",logviews.logAPI),

    path("clear-db/",calcviews.clear_db),
    path("push-def-atr/",functionviews.push_default_attributes)

    # url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
