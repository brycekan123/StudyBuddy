import pandas as pd
import random as random
import MatchingFunctions
# Path to your CSV file
csv_file_path = '/Users/brycekan/Downloads/StudyBuddyNov15/StudyBuddy/testSampleData.csv'

# Read the CSV file
data = pd.read_csv(csv_file_path)
# Display the original data
print("Original Data:")
unmatched_group = []
result_list = []

#Matches users into groups
def process_group(group_pref, groupsize, unmatched_group,result_list):
    #filters group based on size
    group_pref = data.loc[(data["Group Size Preference"] == groupsize)].copy()
    group_pref.reset_index(drop=True, inplace=True)
    #exact matching done on group 2 prior to processing
    if groupsize == 2:
        group_pref = MatchingFunctions.exactMatch(group_pref,result_list)
    pairedlist = []
    #Uses the first row to look for any potential matches.
    selected_day = "" 
    while len(group_pref) > 0:
        print("NEW ITERATION")
        first_row = group_pref.iloc[0]
        max_count = -1
        index_to_delete = -1
        print("!!!selectedDay new iteration,", selected_day)

        #add email to a temp lsit
        if first_row["Email"] not in pairedlist:
            pairedlist.append(first_row["Email"])
        
        #Search for the best matching row
        for i in range(1, len(group_pref)):
            
            current_row = group_pref.iloc[i]
            count = 0
            #for group size 3, I find a day that matches all 3 people
            #Group size 3 will iterate this loop on second time to look for the 3rd person. 
            #on the 2nd pass(looking for P3), available_days_first will be set to the shared day
            if groupsize == 3:
                #on pass 2. available_days_first will be the common day that the 2 people share.
                if selected_day != "":
                    available_days_first = {selected_day}
                    print("Day has been chosen. Sticking with this day: ", available_days_first)
                else:
                    #first person finds the most common day in the dataframe based on their availability
                    selected_day = MatchingFunctions.find_best_day(group_pref)
                    print("SELECTED_DAY",selected_day)
                    available_days_first = {selected_day}
            else:
                available_days_first = set(day.strip() for day in first_row['Availability'].split(";"))
            available_days_current = set(day.strip() for day in current_row['Availability'].split(";"))
            #Commondays = days that the 2 people have in common
            common_days = available_days_first.intersection(available_days_current)
            print("days in common",common_days)
            #if people have overlapping days, randomly choose a day, and pair based on similarity in other fields
            
            if common_days:
                #! this is where i'm messing up. i was randommizing it. i need 
                # to somehow pass in selected day into the next iteration!
                #GROUP OF 2 IS FINE.
                selected_day = random.choice(list(common_days))
                print("selected", selected_day)
                matched_criteria = []
                if first_row['Preferred Language'] == current_row['Preferred Language']:
                    matched_criteria.append(first_row['Preferred Language'])
                    count += 1
                if first_row['Completed Class'] == current_row['Completed Class']:
                    matched_criteria.append(first_row['Completed Class'])
                    count += 1
            # count, matched_criteria, selected_day = evaluate_match(
            #     first_row, current_row, common_days, selected_day, max_count
            # )
                if count > max_count:
                    matched_criteria.append(selected_day)
                    max_count = count
                    index_to_delete = i
                    definiteMatch = matched_criteria
                    print(definiteMatch,"DEFINITEMATCH")
        
        print(group_pref)
        print(first_row["Email"],group_pref.iloc[index_to_delete]["Email"],"definite match",definiteMatch)
        print("max_count",max_count,"index matched",index_to_delete)
        group_pref,pairedlist= MatchingFunctions.checkMatchConditions(
            group_pref,index_to_delete,pairedlist,groupsize)
        print("MIDDLE", selected_day)
        group_pref,result_list,unmatched_group,pairedlist,selected_day = (
            MatchingFunctions.finishGroup(
            group_pref,index_to_delete,result_list,pairedlist,groupsize,unmatched_group,first_row,selected_day,definiteMatch
            )
        )
        print("END OF ITERATION. Selected day is: ", selected_day)
    return result_list, unmatched_group




def evaluate_match(first_row, current_row, common_days, selected_day, max_count):
    """
    Evaluate the match criteria and update the best match.
    """
    count = 0
    matched_criteria = []

    if common_days:
        selected_day = random.choice(list(common_days))
        if first_row['Preferred Language'] == current_row['Preferred Language']:
            matched_criteria.append(first_row['Preferred Language'])
            count += 1
        if first_row['Completed Class'] == current_row['Completed Class']:
            matched_criteria.append(first_row['Completed Class'])
            count += 1

    return count, matched_criteria, selected_day
#Main
groupsizelist = [2,3]
for group_size in groupsizelist:
    result_list,unmatched_group = process_group(data,group_size,unmatched_group,result_list)
MatchingFunctions.getInfo(result_list,unmatched_group)



        





