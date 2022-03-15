verges = (40, 60)
booked = (40, 52, 53, 60)


def get_free_nums(verges, booked):
    return [x for x in range(verges[0], verges[1]+1) if x not in booked]


print(get_free_nums(verges, booked))
