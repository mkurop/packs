#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import number

def swap(a,b):

    if a < b:
        tmp = a
        a = b
        b = tmp

    return a, b


def test_add():

    for i in range(100):

        a = random.randint(0, 1000000)

        b = random.randint(0, 1000000)

        c = a + b

        a_ = number.number2digits(a)

        b_ = number.number2digits(b)

        c_ = number.add_numbers(a_,b_)

        if not c == number.digits2number(c_):

            print(a)

            print(b)

            print(c)

            print(c_)

            print(number.digits2number(c_))

        assert c == number.digits2number(c_) 

def test_subtract():

    for i in range(100):

        a = random.randint(0, 1000000)

        b = random.randint(0, 1000000)

        a, b = swap(a,b)

        c = a - b

        a_ = number.number2digits(a)

        b_ = number.number2digits(b)

        c_ = number.subtract_numbers(a_,b_)

        assert c == number.digits2number(c_) 

def test_multiply():

    for i in range(100):

        a = random.randint(0, 1000000)

        b = random.randint(0, 1000000)

        c = a * b

        a_ = number.number2digits(a)

        b_ = number.number2digits(b)

        c_ = number.multiply_numbers(a_,b_)

        assert c == number.digits2number(c_) 

def test_division():

    for i in range(1000):

        a = random.randint(0, 1000000)

        b = random.randint(0, 1000000)

        a, b = swap(a,b)

        c = a // b

        a_ = number.number2digits(a)

        b_ = number.number2digits(b)

        c_ = number.divide_numbers(a_,b_)

        assert c == number.digits2number(c_) 

