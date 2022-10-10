from django.urls import include, path


urlpatterns = [
    path('api/v0/', include('booking.api.v0.urls'))
]
