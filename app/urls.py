from django.urls import path
from .views import (
    ProductCategoryListView, ProductCategoryDetailView, ProductCategoryUpdateView, ProductCategoryDeleteView,
    SubCategoryListView, SubCategoryDetailView, SubCategoryUpdateView, SubCategoryDeleteView,
    ColorListView, ColorDetailView, ColorUpdateView, ColorDeleteView,ProductFilterView,UserProductInfoView,
    ProductListView, ProductDetailView, ProductUpdateView, ProductDeleteView,TopCategoriesView
)

urlpatterns = [
    
    path('product-categories/', ProductCategoryListView.as_view(), name='product-category-list'),
    path('product-categories/<int:pk>/', ProductCategoryDetailView.as_view(), name='product-category-detail'),
    path('product-categories/<int:pk>/update/', ProductCategoryUpdateView.as_view(), name='product-category-update'),
    path('product-categories/<int:pk>/delete/', ProductCategoryDeleteView.as_view(), name='product-category-delete'),

    path('sub-categories/', SubCategoryListView.as_view(), name='sub-category-list'),
    path('sub-categories/<int:pk>/', SubCategoryDetailView.as_view(), name='sub-category-detail'),
    path('sub-categories/<int:pk>/update/', SubCategoryUpdateView.as_view(), name='sub-category-update'),
    path('sub-categories/<int:pk>/delete/', SubCategoryDeleteView.as_view(), name='sub-category-delete'),

    path('colors/', ColorListView.as_view(), name='color-list'),
    path('colors/<int:pk>/', ColorDetailView.as_view(), name='color-detail'),
    path('colors/<int:pk>/update/', ColorUpdateView.as_view(), name='color-update'),
    path('colors/<int:pk>/delete/', ColorDeleteView.as_view(), name='color-delete'),

    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('top-categories/', TopCategoriesView.as_view(), name='top-categories'),
    path('product-filter/', ProductFilterView.as_view(), name='product-filter'),
    path('user-info/<int:pk>/', UserProductInfoView.as_view(), name='user-info'),    

]
