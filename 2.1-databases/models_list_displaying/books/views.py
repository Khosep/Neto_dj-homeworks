from django.shortcuts import render, redirect
from books.models import Book


def index_view(request):
    return redirect('books')


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {'books': books}
    return render(request, template, context)


def books_pub_date_view(request, pub_date):
    template = 'books/books_list.html'
    books = Book.objects.filter(pub_date=pub_date)
    pub_dates = list(map(str, Book.objects.order_by('pub_date').values_list('pub_date', flat=True).distinct()))
    index_curr = pub_dates.index(pub_date) + 1
    pub_date_prev = pub_dates[index_curr - 2] if index_curr > 1 else None
    pub_date_next = pub_dates[index_curr] if index_curr < len(pub_dates) else None
    context = {
        'books': books,
        'index_curr': index_curr,
        'pub_date_prev': pub_date_prev,
        'pub_date_next': pub_date_next
    }
    return render(request, template, context)
