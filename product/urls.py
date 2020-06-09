from django.urls import path
from . import views

app_name = 'product'


urlpatterns = [
    path('create/',views.create,name='create'),
    path('<int:pk>/',views.ProductDetail.as_view(),name='detail'),
    path('<int:product_id>/upvote',views.upvote,name='upvote'),
]