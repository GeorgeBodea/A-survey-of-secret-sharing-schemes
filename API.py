import Shamir_Secret_Sharing_Scheme as SSSS
import SSSS_Firebase
import SSSS_DropBox
import SSSS_Clever

if __name__ == '__main__':
    share_list, threshold = SSSS.start()
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
    print("The secret reconstructed is: " + str(SSSS.reconstruct_secret(share_list)))
    print(str(shares_used) + " shares have been used to reconstruct the secret")