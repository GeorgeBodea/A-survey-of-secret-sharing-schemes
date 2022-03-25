import Shamir_Secret_Sharing_Scheme as SSSS
import SSSS_Firebase
import SSSS_DropBox
import SSSS_Clever

if __name__ == '__main__':
    share_list = SSSS.start()
    len_share_list = len(share_list)
    index_first_cut = int(len_share_list/3)
    index_second_cut = int(len_share_list*2/3)

    first_part = share_list[:index_first_cut]
    second_part = share_list[index_first_cut:index_second_cut]
    third_part = share_list[index_second_cut:]

    print("First part: " + str(first_part))
    print("Second part: " + str(second_part))
    print("Third part: " + str(third_part))
    SSSS_Firebase.start_firebase(first_part)
    SSSS_DropBox.start_dropbox(second_part)
    SSSS_Clever.start_clever(third_part)