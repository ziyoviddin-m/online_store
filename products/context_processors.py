from products.models import Basket, ProductCategory

def baskets(request):
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}


def categories(request):
    return {'categories': ProductCategory.objects.all()}