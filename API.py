import Shamir_Secret_Sharing_Scheme as SSSS
import SSSS_Firebase
import SSSS_DropBox
import SSSS_Clever

def input_stage():
    while(True):
        secret = input("Input the secret: ")
        secret = int.from_bytes(secret.encode('ASCII'), 'little')
        shares_number = int(input("Input the number of total shares: "))
        threshold = int(input("Input the threshold: "))

        if threshold > shares_number:
            raise ValueError("The threshold should be lower than the number of total shares")

        if threshold < 1:
            raise ValueError("The threshold should be higher than 0")

        if shares_number < 1:
            raise ValueError("The number of total shares should be higher than 0")

        if SSSS.MAX_BOUND < shares_number:
            raise ValueError("The number of total shares should be lower than the possible maximum number of shares")

        share_list = SSSS.create_shares(secret, threshold, shares_number)
        return (share_list, threshold)    

if __name__ == '__main__':
    share_list, threshold = input_stage()
    len_share_list = len(share_list)
    index_first_cut = int(len_share_list/3)
    index_second_cut = int(len_share_list*2/3)

    first_part = share_list[:index_first_cut]
    second_part = share_list[index_first_cut:index_second_cut]
    third_part = share_list[index_second_cut:]

    print("First part: " + str(first_part))
    print("Second part: " + str(second_part))
    print("Third part: " + str(third_part))
    downloaded_share_list = SSSS_Firebase.start_firebase(first_part)
    if len(downloaded_share_list) < threshold:
        downloaded_share_list = downloaded_share_list + SSSS_DropBox.start_dropbox(second_part)
    if len(downloaded_share_list) < threshold:
        downloaded_share_list = downloaded_share_list + SSSS_Clever.start_clever(third_part)

    shares_used = len(downloaded_share_list) 
    print("The secret reconstructed is: " + SSSS.reconstruct_secret(share_list))
    print(str(shares_used) + " shares have been used to reconstruct the secret")