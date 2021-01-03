from django.shortcuts import render
from .models import Post, Category
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger, EmptyPage
from cart.utils import get_total_price, get_cart_items

def post_list(request):
    template_name = 'blog/blog.html'
    post_list = Post.objects.all()
    categories = Category.objects.all()

    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page) 
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    items =  get_cart_items(request)

    context = {
        'posts': post_list,
        'categories': categories,
        'items': items,
        'total_price': get_total_price(items)
    }

    return render(request, template_name, context)

def post_detail(request, slug, category_slug):
    template_name = 'blog/blog-detail.html'
    post = Post.objects.get(slug=slug, category__slug=category_slug)
    searched_category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all()
    items =  get_cart_items(request)

    context = {
        'post': post,
        'categories': categories,
        'searched_category': searched_category,
        'items': items,
        'total_price': get_total_price(items)
    }

    return render(request, template_name, context)

def post_list_by_category(request, category_slug):
    template_name = 'blog/blog.html'
    post_list = Post.objects.filter(category__slug=category_slug)
    searched_category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all()

    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page) 
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    items =  get_cart_items(request)

    context = {
        'posts': post_list,
        'categories': categories,
        'searched_category': searched_category,
        'items': items,
        'total_price': get_total_price(items)
    }

    return render(request, template_name, context)