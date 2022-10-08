from django.shortcuts import render
from django.core.paginator import Paginator
from view_breadcrumbs.generic.base import add_breadcrumb
from booking.models import Category, Room

# helper functions

PAGES = {
    'about': {
        'title': 'О Нас'
    },
    'contacts': {
        'title': 'Контакты'
    },
    'privacy': {
        'title': 'Privacy Policy'
    },
    'toc': {
        'title': 'Term Of Services'
    },
    'appoinment': {
        'title': 'Забронировать'
    },
    'rooms': {
        'title': 'Все Номера',
        'crumbs': [
            ('Наши Номера', 'rooms')
        ]
    },
    'categories': {
        'title': 'Категории Номера',
        'crumbs': [
            ('Наши Номера', 'rooms')
        ]
    },
    'testimonial': {
        'title': 'Отзывы'
    },
}


def _internal_context(request, page=None):
    context = {'request': request}

    add_breadcrumb(context, 'Главная', 'index')

    if not page:
        page = request.path[1:]

    if page in PAGES:
        page_info = PAGES[page]
        context['page_title'] = page_info['title']

        if 'crumbs' in page_info and page_info['crumbs']:
            [add_breadcrumb(context, c[0], c[1]) for c in page_info['crumbs']]

        add_breadcrumb(context, page_info['title'], page)

    rooms_gallery = Room.objects.exclude(thumbnail__isnull=True)[:6]
    context['rooms_gallery'] = rooms_gallery

    return context


# Create your views here.

def home(request):
    context = _internal_context(request)

    return render(request, 'pages/index.html', context=context)


def about(request):
    context = _internal_context(request)

    return render(request, 'pages/about.html', context=context)


def contacts(request):
    context = _internal_context(request)

    return render(request, 'pages/contacts.html', context=context)


def internal(request):
    context = _internal_context(request)

    return render(request, 'pages/internal.html', context=context)


def rooms(request):
    context = _internal_context(request)

    rooms_qs = Room.objects.all()

    category_id = request.GET.get('category')
    if category_id:
        rooms_qs = rooms_qs.filter(category_id=int(category_id))

    paginator = Paginator(rooms_qs, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context['rooms'] = page_obj

    return render(request, 'pages/rooms.html', context=context)


def categories(request):
    context = _internal_context(request)

    context['categories'] = Category.objects.all()

    return render(request, 'pages/categories.html', context=context)


def testimonial(request):
    context = _internal_context(request)

    return render(request, 'pages/testimonial.html', context=context)
