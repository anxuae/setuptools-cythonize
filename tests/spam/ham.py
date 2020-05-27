# -*- coding: utf-8 -*-

from spam.egg.bean import devour
from spam.egg.sausage import hate


def eat():
    return "miam"


def main():
    print("Eat ham:", eat())
    print("Devour bean:", devour())
    print("Hate sausage:", hate())


if __name__ == '__main__':
    main()
