def median(values):
    n = len(values)
    if n == 0:
        return 0

    values = sorted(values)
    mid = n // 2

    if n % 2 == 0:
        return (values[mid - 1] + values[mid]) / 2
    else:
        return values[mid]


def quartiles(values):
    if not values:
        return [0, 0, 0, 0, 0]

    values = sorted(values)
    n = len(values)

    q2 = median(values)
    lower_half = values[: n // 2]
    upper_half = values[(n + 1) // 2 :]

    q1 = median(lower_half)
    q3 = median(upper_half)

    return [
        values[0],   # min
        q1,          # q1
        q2,          # median
        q3,          # q3
        values[-1],  # max
    ]
