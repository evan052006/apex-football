from django.urls import path
from main.views import show_index, show_products_by_xml, show_products_by_json, show_product_xml_by_id, show_product_json_by_id, create_product, show_product

app_name = 'main'

urlpatterns = [
    path('', show_index, name='show_index'),
    path('create_product', create_product, name='create_product'),
    path('show_product/<str:id>/', show_product, name='show_product'),
    path('xml', show_products_by_xml, name='show_products_by_xml'),
    path('json', show_products_by_json, name='show_products_by_json'),
    path('xml/<str:id>/', show_product_xml_by_id, name='show_product_xml_by_id'),
    path('json/<str:id>/', show_product_json_by_id, name='show_product_json_by_id')
]
