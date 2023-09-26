from consumer import ApiConsumer


if __name__ == '__main__':
    consumer = ApiConsumer()
    assert(consumer.fetch(2) == [0, 1])
    assert(consumer.fetch(4) == [2, 3, 4, 5])
    assert(consumer.fetch(1) == [6])
    assert(consumer.fetch(0) == [])
    print("All tests passed!")
