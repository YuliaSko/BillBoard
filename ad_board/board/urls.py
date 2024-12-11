from django.urls import path, include
from .views import *


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='user_profile'),
    path('ad/<int:pk>', AdView.as_view(), name='ad_detail'),
    path('category/<str:pk>', CategoryAdList.as_view(), name='category_list'),
    path('create/', AdCreate.as_view(), name='ad_create'),
    path('response/create/<int:pk>', ResponseCreateView.as_view(), name='response'),
    path('search/', AdSearch.as_view(), name='search'),
    path('my_ads/<int:pk>/', AdListUser.as_view(), name='my_ad'),
    path('ad/<int:pk>/edit', AdUpdate.as_view(), name='edit'),
    path('ad/<int:pk>/delete', AdDelete.as_view(), name='delete'),
    path('my_resp/<int:pk>/', ResponseListUser.as_view(), name='my_resp'),
    path('resp_to_ad/<int:pk>/', ResponsesToAdsList.as_view(), name='resp_to_ad'),
    path('response/accept/<int:pk>/', response_accept, name='response_accept'),
    path('response/<int:pk>/delete', ResponseDelete.as_view(), name='resp_delete'),
]


