import re


class NumbersChecker():
    # принимает список занятых диапазонов вида [(1,10), (31,31), (33, 50)],
    # общее количество номеров (например, 100) и значение начального номера
    # возвращает список своводных диапазонов в виде
    #  [(11,30), (32,32), (51, 100)]
    def get_free_ranges(booked, num_amount, start=1):
        if not booked:
            return [(start, num_amount)]
        booked.sort(key=lambda x: x[0])
        free_ranges = []
        for elem in booked:
            if start < elem[0]:
                free_ranges.append((start, elem[0]-1))
            start = elem[1] + 1
        last_booked = booked[-1][1]
        if last_booked < num_amount:
            free_ranges.append((last_booked + 1, num_amount))
        return free_ranges

    # принимает список свободных диапазонов вида [(11,30), (32,32), (51, 100)]
    # и список зарезервированных номеров (1,11,32,33,55)
    # возвращает список с диапазонами свобоных номеров вида
    # [(12,30), (51,54), (56, 100)]
    def range_free_nums(free_ranges, booked_nums):
        booked_nums.sort()
        nums_amount = len(booked_nums)
        point = 0
        free_nums = []
        for verges in free_ranges:
            left_verge = verges[0]
            right_verge = verges[1]
            for i in range(point, nums_amount):
                counter = i
                if booked_nums[i] < left_verge:
                    continue
                elif booked_nums[i] == left_verge:
                    left_verge += 1
                    continue
                elif booked_nums[i] > right_verge:
                    break
                free_nums.append((left_verge, booked_nums[i] - 1),)
                left_verge = booked_nums[i] + 1
            point = counter
            if left_verge <= right_verge:
                free_nums.append((left_verge, right_verge),)
        return free_nums

    # форматирует список диапазонов вида [(11,30), (32,32), (51, 100)]
    # в строку вида '11-30, 32, 51-100'
    def str_free(free_nums):
        if not free_nums:
            return 'Все стартовые номера заняты.'
        info = 'Для выбора доступны номера:'
        for verges in free_nums:
            info += f' {verges[0]}'
            if verges[0] != verges[1]:
                info += f'-{verges[1]}'
            info += ','
        return info

    # проверяет наличие номера в списке диапазонов вида
    # [(11,30), (32,32), (51, 100)]
    def chek_free(num, free_nums):
        for verges in free_nums:
            if num in range(verges[0], verges[1] + 1):
                return True
        return False


def find_slug(url, prefix, postfix):
    """Извлекает slug из url по известным границам prefix, postfix"""
    pattern = f'{prefix}.+{postfix}'
    slug = re.search(pattern, url).group()
    return slug.lstrip(prefix).rstrip(postfix)
