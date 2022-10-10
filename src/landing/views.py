from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from view_breadcrumbs.generic.base import add_breadcrumb
from booking.models import Category, Room
from booking.search import Search
import urllib.parse

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
    'appointment': {
        'title': 'Забронировать'
    },
}


def intval(value):
    if value is None:
        return None

    try:
        return int(value)
    except ValueError:
        return 0


def _internal_context(request, page=None):
    context = {'request': request}

    # breadcrumbs
    add_breadcrumb(context, 'Главная', 'index')

    if not page:
        page = request.path[1:]

    if page in PAGES:
        page_info = PAGES[page]
        context['page_title'] = page_info['title']

        if 'crumbs' in page_info and page_info['crumbs']:
            [add_breadcrumb(context, c[0], c[1]) for c in page_info['crumbs']]

        add_breadcrumb(context, page_info['title'], page)

    # footer gallery
    rooms_gallery = Room.objects.exclude(thumbnail__isnull=True)[:6]
    context['rooms_gallery'] = rooms_gallery

    # categories for search
    context['search_categories'] = dict(Category.objects.values_list('id', 'name'))

    # search options
    context['search'] = {
        'date_arrival': request.GET.get('search[date_arrival]', ''),
        'days': request.GET.get('search[days]', ''),
        'category': intval(request.GET.get('search[category]', 0)),
        'tenants': request.GET.get('search[tenants]', ''),
    }

    return context


# Create your views here.

def home(request):
    context = _internal_context(request)

    context['categories'] = Category.objects.all()[:8]
    context['rooms'] = Room.objects.all()[:6]

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


def room_details(request, id):
    context = _internal_context(request)

    room = get_object_or_404(Room, pk=id)

    context['room'] = room

    return render(request, 'pages/room.html', context=context)


def appointment(request):
    context = _internal_context(request)

    search_context = context['search']
    context['search_results'] = Search().search(**search_context, offset=request.GET.get('page'))

    return render(request, 'pages/appointment.html', context=context)


def categories(request):
    context = _internal_context(request)

    context['categories'] = Category.objects.all()

    return render(request, 'pages/categories.html', context=context)


def testimonial(request):
    context = _internal_context(request)

    return render(request, 'pages/testimonial.html', context=context)
