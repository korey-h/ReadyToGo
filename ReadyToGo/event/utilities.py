import time


def create_def_category(race_obj, category_form_class):
    """ создание категории участников по умолчанию """
    year = int(time.strftime('%Y'))
    info = {
        'name': 'без категории',
        'slug': 'main_category',
        'race': race_obj,
        'year_old': year - 75,
        'year_yang': year - 8,
    }
    default = category_form_class(info)
    default.save()
