start_num = 0
end_num = 100
booked = [(10, 20),
          (51, 60),
          (34, 50),
          (62, 100)
          ]
# ожидание [(0,9), (21,33), (61,100)]


def get_free_ranges(booked):
    booked.sort(key=lambda x: x[0])
    start = start_num
    free_nums = []
    for elem in booked:
        if start < elem[0]:
            free_nums.append((start, elem[0]-1))
        start = elem[1] + 1
    if booked[-1][1] < end_num:
        free_nums.append((booked[-1][1] + 1, end_num))
    return free_nums


def chek_free(num, free_nums):
    for verges in free_nums:
        if num in range(verges[0], verges[1] + 1):
            return True
    return False


def str_free(free_nums):
    if not free_nums:
        return 'Все стартовые номера заняты.'
    info = 'Для выбора доступны номера:'
    for verges in free_nums:
        info += f' {verges[0]}'
        if verges[0] != verges[1]:
            info += f'-{verges[1]}'
        info += ','
    # info[-1] = '.'
    return info


free_ranges = [(10, 20), (51, 60)]  # свободные диапазоны номеров
nums = [1, 9, 11, 13, 20, 51, 70]  # занятые номера
# [(10,20),(51, 60)] и [1, 9, 11, 13, 20, 51, 70] ->
#  ожидание [(10,10),(12, 12), (14,19), (52,60)]


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


print(range_free_nums(free_ranges, nums))


# free_nums = get_free_ranges(booked)
# print(str_free(free_nums))
# print(chek_free(10, free_nums))
# print(chek_free(22, free_nums))
# print(chek_free(33, free_nums))
# print(chek_free(61, free_nums))
