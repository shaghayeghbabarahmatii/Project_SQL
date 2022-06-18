from django.contrib.auth import views
from django.urls import path
from .views import (
    CallDashboard,
    CallList,
    CallCreate,
    CallUpdate,
    CallDelete,
    Profile,
    PeygiriList,
)

app_name = 'account'

urlpatterns = [
    path('', CallDashboard.as_view(), name="dashboard"),
	path('call/', CallList.as_view(), name="home"),
    path('peygiri/', PeygiriList.as_view(), name="peygiri"),
    path('call/create', CallCreate.as_view(), name="call-create"),
    path('call/update/<int:pk>', CallUpdate.as_view(), name="call-update"),
	path('call/delete/<int:pk>', CallDelete.as_view(), name="call-delete"),
    path('profile/', Profile.as_view(), name="profile"),
]