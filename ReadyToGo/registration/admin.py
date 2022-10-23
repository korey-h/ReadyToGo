from django.contrib import admin

from .forms import CategoryChoiceField
from .models import Categories, Cups, Participants, Races


class RacesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'date', 'cup', 'town',
                    'numbers_amount', 'is_active', 'description')
    search_fields = ('name', 'date', 'cup', 'town', 'is_active')
    list_filter = ('name', 'date', 'cup', 'town', 'is_active')
    empty_value_display = '-пусто-'


class CupsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'slug', 'description')
    list_filter = ('name', )


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'race', 'year_old', 'year_yang',
                    'number_start', 'number_end', 'description')
    search_fields = ('name', 'slug', 'description', 'race')
    list_filter = ('name', 'race')


class ParticipantsAdmin(admin.ModelAdmin):

    list_display = ('race', 'category', 'name', 'surname', 'patronymic',
                    'year', 'number', 'club', 'town', 'reg_code')
    search_fields = ('name', 'surname', 'category__name', 'race__name', 'club',
                     'town', 'number',)
    list_filter = ('category__name', 'race__name', 'club', 'town')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            queryset = Categories.objects.filter(race__is_active=True)
            kwargs.update({'queryset': queryset})
            kwargs.update({'form_class': CategoryChoiceField})

        if db_field.name == 'race':
            queryset = Races.objects.filter(is_active=True)
            kwargs.update({'queryset': queryset})
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Races, RacesAdmin)
admin.site.register(Cups, CupsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Participants, ParticipantsAdmin)
