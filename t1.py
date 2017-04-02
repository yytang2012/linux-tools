def test_throw():
    a = [i for i in range(0, 10)]
    b = dict((i, i*2) for i in range(0, 9))
    try:
        c = [b[i] for i in a]
        print(c)
    except KeyError:
        print("A key does not exist in dictionary")

if __name__ == '__main__':
    test_throw()