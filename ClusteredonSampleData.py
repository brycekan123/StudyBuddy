import pandas as pd
import random as random
import MatchingFunctions
# Path to your CSV file
csv_file_path = '/Users/brycekan/Downloads/10272024StudyBuddy/StudyBuddy/testSampleData.csv'

# Read the CSV file
data = pd.read_csv(csv_file_path)
# Display the original data
print("Original Data:")
unmatched_group = []
result_list = []
#GROUP2
group_pref_2 = data.loc[(data["Group Size Preference"] == 2)].copy()

group_pref_2 = MatchingFunctions.exactMatch(group_pref_2,result_list)
templist = []
groupsize = 2

# #added to info after each match
# while len(group_pref_2) > 0:
#     first_row = group_pref_2.iloc[0]
#     max_count = -1
#     index_to_delete = -1
#     selected_day = ""  
#     #added
#     if first_row["Email"] not in templist:
#          templist.append(first_row["Email"])
#     # Step 3: Loop through all other rows
    
#     for i in range(1, len(group_pref_2)):
#         current_row = group_pref_2.iloc[i]
#         count = 0
#         available_days_first = set(day.strip() for day in first_row['Availability'].split(";"))
#         available_days_current = set(day.strip() for day in current_row['Availability'].split(";"))

#         common_days = available_days_first.intersection(available_days_current)
#         #common_days = MatchingFunctions.find_common_days(first_row['Availability'], current_row['Availability'])
#         if common_days:
#             selected_day = random.choice(list(common_days))
#             matched_criteria = []
#             if first_row['Preferred Language'] == current_row['Preferred Language']:
#                 matched_criteria.append(first_row['Preferred Language'])
#                 count += 1
#             if first_row['Completed Class'] == current_row['Completed Class']:
#                 matched_criteria.append(first_row['Completed Class'])
#                 count += 1
#             if count > max_count:
#                 matched_criteria.append(selected_day)
#                 max_count = count
#                 index_to_delete = i
#                 definiteMatch = matched_criteria
    
#     print(group_pref_2)
#     print(first_row["Email"],group_pref_2.iloc[index_to_delete]["Email"],"definite match",definiteMatch)
#     print("max_count",max_count,"index matched",index_to_delete)
#     group_pref_2,templist= MatchingFunctions.checkMatchConditions(
#         group_pref_2,index_to_delete,templist,groupsize)
#     group_pref_2,result_list,unmatched_group,templist,selected_day = (
#         MatchingFunctions.finishGroup(
#         group_pref_2,index_to_delete,result_list,templist,groupsize,unmatched_group,first_row,selected_day,definiteMatch
#         )
#     )
# print(result_list)
# print("#ofmatches",len(result_list))

# print("UNMATCHED",unmatched_group)


groupsize=3
group_pref_3  = data.loc[(data["Group Size Preference"] == 3)].copy()
group_pref_3.reset_index(drop=True, inplace=True)
print(group_pref_3)
templist = []
selected_day = ""  
while len(group_pref_3) > 0:
    first_row = group_pref_3.iloc[0]
    if first_row["Email"] not in templist:
        templist.append(first_row["Email"])
    max_count = -1
    index_to_delete = -1

    
    for i in range(1, len(group_pref_3)):
        current_row = group_pref_3.iloc[i]
        count = 0
        match_criteria = []
        #if will trigger on second iteration
        if selected_day != "":
            available_days_first = {selected_day}
        else:
            selected_day = MatchingFunctions.find_best_day(group_pref_3)
            print("selected_day",selected_day)
            available_days_first = {selected_day}
        available_days_current = set(day.strip() for day in current_row['Availability'].split(";"))

        common_days = available_days_first.intersection(available_days_current)

        if common_days:
            selected_day = random.choice(list(common_days))
            if first_row['Preferred Language'] == current_row['Preferred Language']:
                match_criteria.append(first_row['Preferred Language'])
                count += 1
            if first_row['Completed Class'] == current_row['Completed Class']:
                match_criteria.append(first_row['Completed Class'])
                count += 1
            if count > max_count:
                match_criteria.append(selected_day)
                max_count = count
                index_to_delete = i
                #definiteMatch will only update if curRow == max row. Will be passed to resultList
                definiteMatch = match_criteria

                
    # HAVE FOUND A MATCH. deleting current row
    group_pref_3,templist= MatchingFunctions.checkMatchConditions(
        group_pref_3,index_to_delete,templist,groupsize)
    group_pref_3,result_list,unmatched_group,templist,selected_day = (
        MatchingFunctions.finishGroup(
        group_pref_3,index_to_delete,result_list,templist,groupsize,unmatched_group,first_row,selected_day,definiteMatch
        )
    )

print(result_list)

print(len(result_list))

print(unmatched_group)

        
    