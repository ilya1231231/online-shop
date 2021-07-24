from django.shortcuts import render
from django.views.generic import DetailView
from .models import Tobacco, Hookah

# Create your views here.
def test_view(request):
    return render(request, 'main/base.html')


class ProductDetailView(DetailView):
    CT_MODEL_MODEL_CLASS = {
        'tobacco': Tobacco,
        'hookah': Hookah
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    # model = Model
    # queryset = Model.objects.all()
    context_object_name = 'product'
    template_name = 'main/product_detail.html'
    slug_url_kwarg = 'slug'




