from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, CategoryViewSet, BookViewSet, LoanViewSet, DashboardView

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'books', BookViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
]