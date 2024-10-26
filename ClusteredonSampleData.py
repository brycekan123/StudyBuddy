import pandas as pd
import random as random
import MatchingFunctions
# Path to your CSV file
csv_file_path = '/Users/brycekan/Downloads/StudyBuddyApplication/testSampleData.csv'

# Read the CSV file
data = pd.read_csv(csv_file_path)
# Display the original data
print("Original Data:")
#print(data)
unmatched_group = []
result_list = []

group_pref_2 = data.loc[(data["Group Size Preference"] == 2)].copy()

result_list = []
match_counter = 0
group_pref_2 = MatchingFunctions.exactMatch(group_pref_2,result_list)
templist = []
while len(group_pref_2) > 0:
    first_row = group_pref_2.iloc[0]
    max_count = -1
    index_to_delete = -1
    selected_day = ""  
    #added
    if first_row["Email"] not in templist:
         templist.append(first_row["Email"])
    # Step 3: Loop through all other rows
    for i in range(1, len(group_pref_2)):
        current_row = group_pref_2.iloc[i]
        print("current row",current_row)

        count = 0
        available_days_first = set(day.strip() for day in first_row['Availability'].split(";"))
        available_days_current = set(day.strip() for day in current_row['Availability'].split(";"))
        common_days = available_days_first.intersection(available_days_current)
        print("first",available_days_first,"current",available_days_current,"common",common_days)
        if common_days:
            print("inside")
            selected_day = random.choice(list(common_days))
            if first_row['Preferred Language'] == current_row['Preferred Language']:
                count += 1
            if first_row['Completed Class'] == current_row['Completed Class']:
                count += 1
            if count > max_count:
                max_count = count
                index_to_delete = i

    print("max_count",max_count,"index matched",index_to_delete)
    group_pref_2,templist= MatchingFunctions.checkMatchConditions(group_pref_2,index_to_delete,templist,2)

        # result_list.append([first_row['Email'],group_pref_2.iloc[index_to_delete]['Email'],selected_day])
        # print("MATCH",first_row['Email'],"matched with",group_pref_2.iloc[index_to_delete]['Email'])
        # group_pref_2 = group_pref_2.drop([0, index_to_delete]).reset_index(drop=True)
    if index_to_delete != -1 and len(templist)== 2:
        result_list.append([templist,selected_day])
        group_pref_2 = group_pref_2.drop([0]).reset_index(drop=True)
        selected_day = ""  
        templist = []
    else:
        group_pref_2 = group_pref_2.drop([0]).reset_index(drop=True)
        unmatched_group.append(first_row['Email'])
print(result_list)
print("#ofmatches",len(result_list))

print("UNMATCHED",unmatched_group)

# group_pref_3  = data.loc[(data["Group Size Preference"] == 3)].copy()
# templist = []
# selected_day = ""  
# while len(group_pref_3) > 0:
#     first_row = group_pref_3.iloc[0]
#     if first_row["Email"] not in templist:
#         templist.append(first_row["Email"])
#     max_count = -1
#     index_to_delete = -1
#     for i in range(1, len(group_pref_3)):
#         current_row = group_pref_3.iloc[i]
#         count = 0
#         if selected_day != "":
#             available_days_first = {selected_day}
#         else:
#             available_days_first = set(day.strip() for day in first_row['Availability'].split(";"))
#         available_days_current = set(day.strip() for day in current_row['Availability'].split(";"))

#         common_days = available_days_first.intersection(available_days_current)
#         if common_days:
#             selected_day = random.choice(list(common_days))
#             if first_row['Preferred Language'] == current_row['Preferred Language']:
#                 count += 1
#             if first_row['Completed Class'] == current_row['Completed Class']:
#                 count += 1
#             if count > max_count:
#                 max_count = count
#                 index_to_delete = i
                
#     # HAVE FOUND A MATCH. deleting current row
#     group_pref_3,templist= MatchingFunctions.checkMatchConditions(group_pref_3,index_to_delete,templist,3)

#     ## 2 MATCHES FOUND. now deleting first row, move on to next "first iteration"
#     if index_to_delete != -1 and len(templist)== 3:
#         result_list.append([templist,selected_day])
#         group_pref_3 = group_pref_3.drop([0]).reset_index(drop=True)
#         selected_day = ""  
#         templist = []
        
#     if index_to_delete == -1:
#         unmatched_group.append(first_row['Email'])
#         group_pref_3 = group_pref_3.drop([0]).reset_index(drop=True)

# print(result_list)

# print(len(result_list))

        
    