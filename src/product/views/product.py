from django.views import generic
from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from django.shortcuts import render
from product.models import Product
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q
from rest_framework import generics
from product.serializers import ProductSerializer, ProductVariantPriceSerializer


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    pass

def ProductListView(request):
    if request.GET.get('title'):
        title = request.GET.get('title')
        variant = request.GET.get('variant')
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        print("get url", title, variant, price_from, price_to)
        products = Product.objects.filter(
            title__icontains=title,
            productvariant__variant_title__icontains=variant,
            productvariantprice__price__range=[price_from, price_to]

        ).distinct()
        paginator = Paginator(products, 2)

    else:
        products = Product.objects.all()
        paginator = Paginator(products, 2)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.get_page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    if list(products.object_list)[-1]:
        last_page = list(products.object_list)[-1]
        first_page = list(products.object_list)[0]
        first_id = first_page.id
        last_id = last_page.id
    else:
        first_id = 0
        last_id = 0

    variant = Variant.objects.all()
    print(products)

    return render(request, 'products/list.html',context={'products':products, 'variants': variant, 'page': products, "count": paginator.count, "first": first_id, "last": last_id})

class createProductViewset(generics.ListCreateAPIView):
    queryset = ProductVariantPrice.objects.all()
    serializer_class = ProductVariantPriceSerializer