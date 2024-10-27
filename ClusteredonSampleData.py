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


def process_group(group_pref, groupsize, unmatched_group,result_list):
    group_pref = data.loc[(data["Group Size Preference"] == groupsize)].copy()
    group_pref.reset_index(drop=True, inplace=True)

    if groupsize == 2:
        group_pref = MatchingFunctions.exactMatch(group_pref,result_list)
    templist = []

    #added to info after each match
    while len(group_pref) > 0:
        first_row = group_pref.iloc[0]
        max_count = -1
        index_to_delete = -1
        selected_day = ""  
        #added
        if first_row["Email"] not in templist:
            templist.append(first_row["Email"])
        # Step 3: Loop through all other rows
        
        for i in range(1, len(group_pref)):
            current_row = group_pref.iloc[i]
            count = 0
            if groupsize == 3:
                if selected_day != "":
                    available_days_first = {selected_day}
                else:
                    selected_day = MatchingFunctions.find_best_day(group_pref)
                    print("selected_day",selected_day)
                    available_days_first = {selected_day}
            else:
                available_days_first = set(day.strip() for day in first_row['Availability'].split(";"))
            available_days_current = set(day.strip() for day in current_row['Availability'].split(";"))

            common_days = available_days_first.intersection(available_days_current)
            #common_days = MatchingFunctions.find_common_days(first_row['Availability'], current_row['Availability'])
            if common_days:
                selected_day = random.choice(list(common_days))
                matched_criteria = []
                if first_row['Preferred Language'] == current_row['Preferred Language']:
                    matched_criteria.append(first_row['Preferred Language'])
                    count += 1
                if first_row['Completed Class'] == current_row['Completed Class']:
                    matched_criteria.append(first_row['Completed Class'])
                    count += 1
                if count > max_count:
                    matched_criteria.append(selected_day)
                    max_count = count
                    index_to_delete = i
                    definiteMatch = matched_criteria
        
        print(group_pref)
        print(first_row["Email"],group_pref.iloc[index_to_delete]["Email"],"definite match",definiteMatch)
        print("max_count",max_count,"index matched",index_to_delete)
        group_pref,templist= MatchingFunctions.checkMatchConditions(
            group_pref,index_to_delete,templist,groupsize)
        group_pref,result_list,unmatched_group,templist,selected_day = (
            MatchingFunctions.finishGroup(
            group_pref,index_to_delete,result_list,templist,groupsize,unmatched_group,first_row,selected_day,definiteMatch
            )
        )
    
    return result_list, unmatched_group

groupsizelist = [2,3]
for group_size in groupsizelist:
    result_list,unmatched_group = process_group(data,group_size,unmatched_group,result_list)
MatchingFunctions.getInfo(result_list,unmatched_group)



        





