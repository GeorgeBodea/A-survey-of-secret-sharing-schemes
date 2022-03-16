from random import random
import unittest
import secrets
import Shamir_Secret_Sharing_Scheme as SSSS

def select_random_shares(share_list, threshold):
           random_share_list = []
           unique_numbers = set()
           counter_unique_numbers = 0
           while(counter_unique_numbers < threshold):
            generated_number = secrets.choice(share_list)
            if generated_number not in unique_numbers:
             random_share_list.append(generated_number)
             unique_numbers.add(generated_number)
             counter_unique_numbers += 1
           print("Random share list: " + str(random_share_list))
           return random_share_list

def distribute_reconstruct(secret, threshold, shares_number):
        share_list = SSSS.create_shares(secret, threshold, shares_number)
        random_shares_trehshold_bounded = select_random_shares(share_list, threshold)
        assert(SSSS.reconstruct_secret(random_shares_trehshold_bounded), secret)

class test(unittest.TestCase):
    def test_3shares_2threshold(self):
        secret = 100
        shares_number = 3
        threshold = 2
        distribute_reconstruct(secret, threshold, shares_number)
    
    def test_20shares_7threshold(self):
        secret = 52516
        shares_number = 20
        threshold = 4
        distribute_reconstruct(secret, threshold, shares_number)

if __name__ == "__main__":
    unittest.main()