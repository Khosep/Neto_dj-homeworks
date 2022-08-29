from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

def home_view(request):
    context = {'dishes': list(DATA.keys())}
    return render(request, 'calculator/home.html', context)

def calculator_view(request, dish):
    dish = dish.strip('/')
    number = int(request.GET.get('servings', 1))
    context = {'recipe': {ingredient: round(amount*number, 2) for ingredient, amount in DATA.get(dish, {}).items()}}
    return render(request, 'calculator/index.html', context)
