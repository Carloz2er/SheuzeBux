from django.shortcuts import render
from .models import Product, Category

def home(request):
    # Busca todos os produtos que estão ativos
    products = Product.objects.filter(is_active=True)

    # Busca todas as categorias para o menu de navegação
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }

    # Renderiza o template da página inicial, passando o contexto
    return render(request, 'store/home.html', context)