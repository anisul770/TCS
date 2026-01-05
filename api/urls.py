from django.urls import path,include
from rest_framework_nested import routers
from cart.views import CartViewSet,CartItemViewSet
from services.views import ServiceViewSet,CategoryViewSet
from reviews.views import ReviewViewSet

router = routers.DefaultRouter()
router.register('services',ServiceViewSet,basename='services')
router.register('categories',CategoryViewSet)
router.register('carts',CartViewSet,basename='carts')

service_router = routers.NestedDefaultRouter(router,'services',lookup='service')
service_router.register('reviews',ReviewViewSet,basename='review')

cart_router = routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_router.register('items',CartItemViewSet,basename='cart-item')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(cart_router.urls)),
    path('',include(service_router.urls)),
]
