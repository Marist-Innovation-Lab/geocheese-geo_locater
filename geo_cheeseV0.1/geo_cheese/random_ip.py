from random import randrange

def rand_ip():
    not_valid = [10, 127, 169, 172, 192, 255]

    first = randrange(1, 256)
    while first in not_valid:
        first = randrange(1, 256)

    ip = ".".join([str(first), str(randrange(1, 256)),
                   str(randrange(1, 256)), str(randrange(1, 256))])
    #print(str(ip))
    return str(ip)