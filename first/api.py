DATA = [i for i in range(0, 100)]
PAGE_SIZE = 5


def api_call(page):
    index = page * PAGE_SIZE
    return DATA[index:index + PAGE_SIZE]

