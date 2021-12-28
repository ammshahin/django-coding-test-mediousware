from django.core import paginator
from django.views import generic
from product.models import Variant
from django.shortcuts import render
from product.models import Product

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

def ProductListView(request):
    products = Product.objects.all()

    page = request.GET.get('page')

    paginator = Paginator(products, 2)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.get_page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    last_page = list(products.object_list)[-1]
    first_page = list(products.object_list)[0]
    first_id = first_page.id
    last_id = last_page.id

    variant = Variant.objects.filter(title = 'color')

    return render(request, 'products/list.html',context={'products':products, 'variant': variant, 'page': products, "count": paginator.count, "first": first_id, "last": last_id})

