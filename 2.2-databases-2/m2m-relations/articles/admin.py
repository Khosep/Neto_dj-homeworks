from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        number_of_main_tags = 0
        tags = []
        for form in self.forms:
            if form.cleaned_data.get('is_main') and form.cleaned_data:
                number_of_main_tags += 1
            tag = form.cleaned_data.get('tag')
            if tag in tags:
                raise ValidationError(f'Раздел {tag} уже добавлен')
            tags.append(tag)
        # number_of_main_tags = sum([form.cleaned_data.get('is_main') for form in self.forms if form.cleaned_data])
        if not number_of_main_tags:
            raise ValidationError('Укажите основной раздел')
        elif number_of_main_tags > 1:
            raise ValidationError('Основным может быть только один раздел')
        return super().clean()  # вызываем базовый код переопределяемого метода
class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at']
    list_filter = ['published_at']
    inlines = [ScopeInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


