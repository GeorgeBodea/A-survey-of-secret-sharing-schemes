import secrets
import math
from decimal import Decimal, getcontext

MAX_BOUND = 64

getcontext().prec = 250

def g_i(i, share_list):
    product = 1
    for j in range(len(share_list)):
        x_i = share_list[i][0]
        if i != j:
            x_j = share_list[j][0]
            product *= Decimal(Decimal(-x_j) / Decimal(x_i - x_j))
    return product

def reconstruct_secret(share_list):
    i = 0
    sum = 0
    for x, y in share_list:
        sum += Decimal(y * g_i(i, share_list))
        i += 1
    sum = round(sum)
    secret = sum.to_bytes(math.ceil(sum.bit_length() / 8), 'little').decode('ASCII')
    return secret

def create_coefficients(threshold):
    return [secrets.randbelow(MAX_BOUND) for _ in range(threshold - 1)]

def create_x_coordinates(shares_number):
   x_coordinates = []
   unique_numbers = set()
   counter_unique_numbers = 0

   while(counter_unique_numbers < shares_number):
       generated_number = secrets.randbelow(MAX_BOUND)
       if generated_number not in unique_numbers:
           x_coordinates.append(generated_number)
           unique_numbers.add(generated_number)
           counter_unique_numbers += 1

   return x_coordinates

def create_y_coordinates(all_coefficients, x_coordinates):
    y_coordinates = []

    print("X Coordinates: " + str(x_coordinates))
    for x in x_coordinates:
        power = 0
        y = 0
        for coefficient in all_coefficients:
            y += coefficient * (x ** power)
            power += 1
        y_coordinates.append(y)
    print("Y coordinates: " + str(y_coordinates))
    return y_coordinates
 
def create_points(all_coefficients, shares_number):
    x_coordinates = create_x_coordinates(shares_number)
    y_coordinates = create_y_coordinates(all_coefficients, x_coordinates)
    share_list = list(zip(x_coordinates, y_coordinates))
    print("Share list: " + str(share_list))
    return share_list

def create_shares(secret, threshold, shares_number):
    all_coefficients = [secret] + create_coefficients(threshold)
    print("All coefficients: " + str(all_coefficients))
    share_list = create_points(all_coefficients, shares_number)
    return share_list