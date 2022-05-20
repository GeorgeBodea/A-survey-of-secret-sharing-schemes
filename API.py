import Shamir_Secret_Sharing_Scheme as SSSS
import SSSS_Firebase
import SSSS_DropBox
import SSSS_Clever

def input_api(secret, shares_number, threshold):
    # while(True):
    # secret = input("Input the secret: ")
    secret = int.from_bytes(secret.encode('ASCII'), 'little')
    # shares_number = int(input("Input the number of total shares: "))
    # threshold = int(input("Input the threshold: "))

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

def distribution_api(share_list):
    len_share_list = len(share_list)
    index_first_cut = int(len_share_list/3)
    index_second_cut = int(len_share_list*2/3)

    first_part = share_list[:index_first_cut]
    second_part = share_list[index_first_cut:index_second_cut]
    third_part = share_list[index_second_cut:]

    print("First part: " + str(first_part))
    print("Second part: " + str(second_part))
    print("Third part: " + str(third_part))

    SSSS_Firebase.upload_firebase(first_part)
    SSSS_DropBox.upload_dropbox(second_part)
    SSSS_Clever.upload_clever(third_part)

    return (first_part, second_part, third_part)

def reconstruction_api(threshold):
    firebase_shares = SSSS_Firebase.download_firebase()
    dropbox_shares = []
    clever_shares = []
    if len(firebase_shares) < threshold:    
        dropbox_shares = SSSS_DropBox.download_dropbox()
    if ( len(firebase_shares) + len(dropbox_shares) ) < threshold:
        clever_shares = SSSS_Clever.download_clever()
    
    downloaded_shares = firebase_shares + dropbox_shares + clever_shares
    number_of_shares = len(downloaded_shares)
    secret = SSSS.reconstruct_secret(downloaded_shares)
    
    print("The secret reconstructed is: " + secret)
    print(str(number_of_shares) + " shares have been used to reconstruct the secret")
    
    return secret


# if __name__ == '__main__':
#     share_list, threshold = input_api()
#     distribution_api(share_list)
#     reconstruction_api(threshold)