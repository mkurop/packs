#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Tuple
import numpy as np
from numba import njit
"""
number.py
=======================
Basic arithmetic operations for a numbers represented as the numpy array of uint8 integers. 
The format of the number is following:
* given the number representation: [1,2,3,4]
* the represented number is equal: 4 + 3 * 256 + 2 * 256**2 + 1 * 256**3
that is the 0th byte is the most significant byte
"""

@njit
def count_non_zero_digits(number : np.ndarray) -> int:
    """Counts most significant bytes being zero and returns the number of digits in the number miunus counted zero bytes
    :param number: table of digits
    :type number: np.ndarray
    :return: number of digits minus number of most significat bytes being all zero
    :rtype: int
    """

    num_of_digits = 0 

    digit = number[num_of_digits]

    while digit == 0:

        num_of_digits += 1

        if num_of_digits == number.shape[0]:

            return 0

        digit = number[num_of_digits]

        if digit != 0:

            return number.shape[0] - num_of_digits

    return number.shape[0] - num_of_digits

@njit
def multiply_numbers(a : np.ndarray, b : np.ndarray, base : int = 256) -> np.ndarray:
    """Long multiplication algorithm from the Seminumerical Algorithms by Donald Knuth.

    :param a: digits of the first number
    :type a: np.ndarray
    :param b: digits of the second number
    :type b: np.ndarray
    :param base: the base of the computation, defaults to 256
    :return: a*b in the radix base representationo
    :rtype: np.ndarray

    """

    product = np.zeros((a.shape[0]+b.shape[0],), dtype = np.uint8)

    a = a[::-1]

    b = b[::-1]


    for j in range(b.shape[0]):

        if b[j] == 0:

            product[j+a.shape[0]] = 0

            continue

        k = 0

        for i in range(a.shape[0]):

            t = np.uint32(a[i]) * np.uint32(b[j]) + np.uint32(product[i+j]) + k

            product[i+j] = t % base

            k = t // base

        product[j+a.shape[0]] = k

    return product[::-1]

@njit
def a_gt_b(a : np.ndarray, b : np.ndarray) -> bool:
    """Checks of a is grater than b
    
    :param a: digits of the first number
    :type a: np.ndarray
    :param b: digits of the second number
    :type b: np.ndarray
    :return: True if a > b False otherwise
    :rtype: bool
    """

    count_a = count_non_zero_digits(a)

    count_b = count_non_zero_digits(b)

    if count_a > count_b:

        return True

    elif count_a < count_b:

        return False

    for i in range(count_a):

        if a[i] > b[i]:

            return True

        elif a[i] < b[i]: 

            return False

    return False

@njit
def a_equal_b(a : np.ndarray, b: np.ndarray) -> bool:
    """Checks if a is equal b
    
    :param a: digits of the first nummber
    :type a: np.ndarray
    :param b: digits of the second number
    :type b: np.ndarray
    :return: True if a==b False otherwise
    :rtype: bool
    """

    count_a = count_non_zero_digits(a)

    count_b = count_non_zero_digits(b)

    if count_a != count_b:

        return False

    for i in range(count_a):

        if a[i] != b[i]:

            return False

    return True

@njit
def align_numbers(a : np.ndarray, b : np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Causes both number occupy the same number of digits by eventually appending zero digits as most significant bytes
    
    :param a: digits of the first number
    :type a: np.ndarray
    :param b: digits of the second number
    :type b: np.ndarray
    :return: byte aligned a and b
    :rtype: Tuple[np.ndarray, np.ndarray]
    """

    a_count = a.shape[0]
    b_count = b.shape[0]

    if a_count == b_count:

        return a, b

    elif a_count < b_count:

        a_new = np.zeros_like(b)

        a_new[-a_count:] = a

        return a_new, b 

    else:

        b_new = np.zeros_like(a)

        b_new[-b_count:] = b

        return a, b_new

@njit
def align_numbers_with_shrink(a : np.ndarray, b : np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """The same as align_numbers but numbers are first shrinked by removing zero most significant bytes"""

    a = shrink_number(a)
    b = shrink_number(b)

    return align_numbers(a,b)

@njit
def subtract_numbers(a : np.ndarray, b : np.ndarray, base : int = 256) -> np.ndarray:
    """Subtracts b from a using algorithm from Seminumerical Algorithms by Donald Knuth.
    a has to be greater than b

    :raises ValueError: raised if not a > b

    :param a: digits of the first number 
    :type a: np.ndarray
    :param b: digits of the second number
    :type b: np.ndarray
    :param base: base/radix, defaults to 256
    :type base: int
    :return: a - b as an array of digits radix base
    :rtype: np.ndarray
    """
    
    if not a_gt_b(a,b):

        raise ValueError('a should be grater than b ...')

    if a_equal_b(a,b):

        return np.asarray([0], dtype = np.uint8)

    a, b = align_numbers(a,b)

    a = a[::-1]

    b = b[::-1]

    print(a)

    print(b)

    c = np.zeros((a.shape[0],), dtype = np.uint8)

    k = 0

    for j in range(a.shape[0]):

        t = np.int32(a[j]) - np.int32(b[j]) + k

        c[j] = np.uint8(t % base)

        k = t // base

    return c[::-1]

@njit
def add_numbers(a : np.ndarray, b : np.ndarray, base : int = 256) -> np.ndarray:
    """Adds a to b using algorithm from Seminumerical Algorithms by Donald Knuth.

    :param a: digits of the first number
    :type a: np.ndarray
    :param b: digits of the second number
    :type b: np.ndarray
    :param base: base/radix, defaults to 256
    :type base: int
    :return: a + b as an array of digits radix base
    :rtype: np.ndarray
    """

    a, b = align_numbers(a,b)

    sum_ = np.zeros((a.shape[0]+1,), dtype = np.uint8)

    a = a[::-1]

    b = b[::-1]

    k = 0

    for j in range(a.shape[0]):

        t = np.uint32(a[j]) + np.uint32(b[j]) + k

        sum_[j] = t % base

        k = t // base

    sum_[a.shape[0]] = k

    return sum_[::-1]

@njit
def divide_numbers(a : np.ndarray, b : np.ndarray, base : int = 256) -> np.ndarray:
    """Divides a by b using algorithm from Seminumerical Algorithms by Donald Knuth.

    :raises ValueError: if b is zero, as no division by zero is defined
    :raises ValueError: if not a > b, a has to be larger than b

    :param a: digits of the first number
    :type a: np.ndarray
    :param b: digits of the second number
    :type b: np.ndarray
    :param base: base/radix, defaults to 256
    :type base: int
    :return: a // b as an array of digits radix base
    :rtype: np.ndarray
    """



    b = shrink_number(b)

    if b.shape[0] == 1 and b[0] == 0:
        raise ValueError("No division by zero possible ...")

    a = shrink_number(a)

    if a_equal_b(a,b):

        return number2digits(1) # quotient

    if not a_gt_b(a,b):
        raise ValueError("a have to be greater than b ...")

    n = b.shape[0]

    aux4 = shift_left(number2digits(1),n+1)

    m = a.shape[0] - n

    q = np.zeros((m+1,), dtype=np.uint8)

    d = base // (np.uint32(b[0])+1)

    d_ = number2digits(d)

    ad = multiply_numbers(a, d_)

    bd = multiply_numbers(b, d_)

    bd = shrink_number(bd)

    ad = ad[::-1]

    if d == 1:

        ad_ = np.zeros((ad.shape[0]+1,), dtype = np.uint8)

        ad_[:ad.shape[0]] = ad

        ad = ad_

    bd = bd[::-1]

    for j in range(m,-1,-1):

        t = np.uint32(ad[j+n]) * np.uint32(base)+ np.uint32(ad[j+n-1])

        q_hat = t // bd[n-1]

        r_hat = t % bd[n-1]

        if q_hat >= base or (q_hat * (0 if n-2 < 0 else np.uint32(bd[n-2])) > base * r_hat + np.uint32(ad[j+n-2])):

            q_hat -= 1

            r_hat += np.uint32(bd[n-1])

        if r_hat < base:

            if q_hat >= base or q_hat * (0 if n-2 < 0 else np.uint32(bd[n-2])) > base * r_hat + np.uint32(ad[j+n-2]):

                q_hat -= 1

                r_hat += np.uint32(bd[n-1])

        q[j] = np.uint8(q_hat)

        aux1 = ad[j:j+n+1]

        q_hat_digits = number2digits(q_hat)

        aux2 = multiply_numbers(q_hat_digits, bd[::-1]) 

        if a_equal_b(aux1[::-1],aux2):

            ad[j:j+n+1] = np.zeros((n+1,),dtype=np.uint8)

            continue

        elif a_gt_b(aux1[::-1],aux2):

            bux1 = subtract_numbers(aux1[::-1],aux2)

            bux2, _ = align_numbers(bux1,aux1)

            ad[j:j+n+1] = bux2[::-1]

            continue

        else:

            aux3 = subtract_numbers(aux2,aux1[::-1])

            aux5 = subtract_numbers(aux4,aux3)

            aux6 = shrink_number(aux5)

            aux7, _ = align_numbers(aux6,aux1)

            ad[j:j+n+1] = aux7[::-1]

            q[j] -= 1

            aux8 = ad[j:j+n+1]

            aux9 = add_numbers(aux8[::-1],bd[::-1])

            if aux9.shape[0] > n+1:

                aux10 = aux9[1:]

            else:

                aux10 = aux9

            ad[j:j+n+1] = aux10[::-1]

    return q[::-1]


def divide_number_with_remainder(a : np.ndarray, b : np.ndarray, base : int = 256) -> Tuple[np.ndarray, np.ndarray]:

    pass

@njit
def digits2number(digits : np.ndarray, base : int = 256) -> np.ndarray:
    """Converts given base digits into signle Python integer (which can be in theory of any size)
    
    :param digits: digits of the input number
    :type digits: np.ndarray
    :param base: base/radix, defaults to 256
    :type base: int
    :return: Python integer representation of the table if digits
    :rtype: np.ndarray
    """
    number = 0

    for i in range(digits.shape[0]):

        number += int(digits[digits.shape[0]-i-1])*base**i

    return number

@njit
def number2digits(number : int) -> np.ndarray:
    """
    Converts number to base 256 digits.

    :param number: integer (64 bit unsigned int) to convert from
    :type number: int
    :return: array of base 256 digits
    :rtype: np.ndarray
    """

    digits = np.zeros((8,),dtype=np.uint8)

    digit = np.uint64(number) & np.uint64(0xFF) 

    digits[0] = np.uint8(digit)

    num_digits = 1

    while num_digits < 8:

        digit = (np.uint64(number) >> (num_digits << 3)) & np.uint64(0xFF)

        digits[num_digits] = np.uint8(digit)

        num_digits += 1

    ret = shrink_number(digits[::-1])

    return ret

@njit
def shrink_number(number : np.ndarray) -> np.ndarray:
    """Assures that the most significat byte is non-zero digit or the number is zero and there is only one digit equal to zero
    :param number: number to be shrinked, vector of digits radix 256
    :type number: np.ndarray
    :return: shrinked number
    :rtype: np.ndarray
    """
    
    count = count_non_zero_digits(number)

    if count == 0:

        return np.asarray([0], dtype=np.uint8)

    return number[-count_non_zero_digits(number):]

@njit
def shift_left(a : np.ndarray, n : int):

    a = shrink_number(a)

    result = np.zeros((a.shape[0]+n,), dtype = np.uint8)

    result[:a.shape[0]] = a

    return result

@njit
def shift_right(a : np.ndarray, n : int):

    a = shrink_number(a)

    if a.shape[0] <= n:

        return number2digits(0)

    else:

        return a[:-n] 


if __name__ == "__main__":

    #  number = 2**56-1
    #
    #  digits = number2digits(number)
    #
    #  print(digits)
    #
    #  a = number2digits(512)
    #  print(a)
    #
    #  b = number2digits(255)
    #  print(b)
    #
    #  print(number2digits(512*255))
    #  print(512*255)
    #  print(1*256**2 + 254*256 + 0)
    #
    #  product = multiply_numbers(a,b)
    #
    #  print(product)
    #
    #  print(digits2number(product))
    #
    #  print(count_non_zero_digits(product))
    #
    #  print(shrink_number(product))
    #
    #  a = number2digits(356000)
    #  print(a)
    #
    #  b = number2digits(355)
    #  print(b)
    #
    #  print(a_gt_b(a,b))
    #
    #  print(a_equal_b(a,b))
    #
    #  a,b = align_numbers(a,b)
    #  print(a)
    #  print(b)
    #
    #  c = subtract_numbers(a,b)
    #
    #  print(c)
    #
    #  print(356000-355)
    #
    #  print(digits2number(c))
    #
    #  c = add_numbers(a,b)
    #
    #  print(356000+355)
    #
    #  print(digits2number(c))
    #
    #  a_ = 31024
    #
    #  b_ = 446
    #
    #  a = number2digits(a_)
    #
    #  b = number2digits(b_)
    #
    #  print(a)
    #  print(b)
    #
    #  c = divide_numbers(a,b)
    #  print(c)
    #  print(digits2number(c))
    #  print(a_ // b_)
    #
    #
    #

    #  a = 393316
    #
    #  b = 105931
    #
    #  a_ = number2digits(a)
    #
    #  print(a_)
    #
    #  print(digits2number(a_))
    #
    #  b_ = number2digits(b)
    #
    #  print(digits2number(b_))
    #
    #  print( a * b )
    #
    #  c_ = multiply_numbers(a_,b_)
    #
    #  print(digits2number(c_))

    a_ = np.asarray([4,207,170], dtype=np.uint8)

    b_ = np.asarray([223,3], dtype=np.uint8)

    print(divide_numbers(a_,b_))
