from django.shortcuts import render
from main.models import Product
from django.http import HttpResponse
from django.core import serializers


def show_products_by_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")


def show_products_by_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")


def show_product_xml_by_id(request, id):
    try:
        product_item = Product.objects.get(id=id)
        xml_data = serializers.serialize("xml", [product_item])
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)


def show_product_json_by_id(request, id):
    try:
        product_item = Product.objects.get(id=id)
        json_data = serializers.serialize("json", [product_item])
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
        return HttpResponse(status=404)


def show_index(request):
    return render(
        request,
        "index.html",
        {
            "nama": "Christopher Evan Tanuwidjaja",
            "kelas": "A",
            "app_name": "main"
        }
    )
