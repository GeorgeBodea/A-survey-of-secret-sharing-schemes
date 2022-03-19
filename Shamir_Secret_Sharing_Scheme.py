import secrets

MAX_BOUND = 64

def g_i(i, share_list):
    product = 1
    for j in range(len(share_list)):
        x_i = share_list[i][0]
        if i != j:
            x_j = share_list[j][0]
            product *= float(float(-x_j) / float(x_i - x_j))
    return product

def reconstruct_secret(share_list):
    # THE SECRET IS RECOVERED BY PLUGING IN X = 0
    i = 0
    sum = 0

    # Ignore first share (the secret). It won't be distributed
    for x, y in share_list:

        sum += float(y * g_i(i, share_list))
        i += 1
    print(round(sum))


# Having the threshold k = 3, we would need a polynomial function composed
# of elements of grade 2, that is, 3 elements, the last beeing the secret
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

def start():
    while(True):
        secret = int(input("Input the secret as a number: "))
        shares_number = int(input("Input the number of total shares: "))
        threshold = int(input("Input the threshold: "))

        if threshold > shares_number:
            raise ValueError("The threshold should be lower than the number of total shares")

        if threshold < 1:
            raise ValueError("The threshold should be higher than 0")

        if shares_number < 1:
            raise ValueError("The number of total shares should be higher than 0")

        if MAX_BOUND < shares_number:
            raise ValueError("The number of total shares should be lower than the possible maximum number of shares")

        share_list = create_shares(secret, threshold, shares_number)
        return share_list
    # reconstruct_secret(share_list[:threshold])

if __name__ == '__main__':
    start()