
from django.urls import path,include

from query import views

urlpatterns = [
    path("querydetail/",views.query_info,name="query_info")

 
]