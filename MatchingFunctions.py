import random

def exactMatch(group_pref_2,result_list):
    grouped = group_pref_2.groupby(['Availability', 'Preferred Language', 'Completed Class'])
    for key, group in grouped:
        listofemails = group['Email'].tolist()
        if (len(listofemails)>1):
            for i in range(len(listofemails)):
                indices = group_pref_2.index[group_pref_2["Email"] == listofemails[i]].tolist()
                for index in indices:
                    group_pref_2 = group_pref_2.drop(index).reset_index(drop=True)
            result_list.append([listofemails,key])
    return group_pref_2

#We have found a match. Now, I add the email of the desired individual and drop them from the gruop. 
def checkMatchConditions(group_pref,index_to_delete,pairedlist,groupsize):
    #Match
    #Adding the ideal pair to the pairedList. 
    #dropping the candidate from the dataframe
    if index_to_delete != -1 and len(pairedlist)< groupsize:
        print("FoundMatch, templist < groupsize")
        pairedlist.append(group_pref.iloc[index_to_delete]['Email'])
        group_pref = group_pref.drop([index_to_delete]).reset_index(drop=True)
        print("PairedList: ",pairedlist)

    return group_pref, pairedlist
#templist is to store the people that are about to be in a group

def finishGroup(group_pref,index_to_delete,result_list,pairedlist,groupsize,unmatched_group,first_row,selected_day,definiteMatch):
    #Group 2 checkMatch will always lead to finishGroup because length of tempList will hit 2.
    #Group 3 will skip finishGroup until 3rd row is Found. len(templist) ==2 when 2nd row is found. len(templist) == 3 will trigger grouping
    print(group_pref)

    if index_to_delete != -1 and len(pairedlist)== groupsize:
        print("Match made: ",pairedlist,definiteMatch)
        result_list.append([pairedlist,definiteMatch])
        #print("RESULT",result_list)
        group_pref = group_pref.drop([0]).reset_index(drop=True)
        print("after drop",group_pref)
        #resetting for next iteration
        selected_day = "" 
        pairedlist = []
    #this is the unmatched group
    if index_to_delete == -1:
        print(first_row['Email'], "is unmatched")
        
        #dropping first row since there's no matches. Moving onto the next iteration
        group_pref = group_pref.drop([0]).reset_index(drop=True)
        print(group_pref)
        print("TEMPLIST",pairedlist)
        #if no match... definite match might need to be rest
        definiteMatch=[]
        unmatched_group.append(pairedlist)
        pairedlist = []
        selected_day = "" 
    
    return group_pref,result_list,unmatched_group,pairedlist,selected_day


import random

def find_best_day(group_df):
    # Step 1: Get the days from the first row
    first_row_days = group_df['Availability'].iloc[0].split(';')
    first_row_days = [day.strip() for day in first_row_days if day]  # Clean up and ensure no empty days
    print("First row days:", first_row_days)
    
    # Step 2: Create a dictionary to count occurrences of the first row's days
    day_count = {day: 0 for day in first_row_days}  # Initialize with 0 for the first-row days
    
    # Step 3: Iterate over each row in the DataFrame
    for i in range(len(group_df)):
        availability = group_df['Availability'].iloc[i].split(';')
        print("Available days:", availability)
        for day in availability:
            day = day.strip()  # Strip whitespace
            
            # Only count if the day is in the first row's days
            if day in day_count:
                day_count[day] += 1  # Increment count

    print("Day counts:", day_count)
    
    # Step 4: Check if there are any valid days
    if all(count == 0 for count in day_count.values()):  # No matches found
        return None

    # Step 5: Find the maximum count value
    max_count = max(day_count.values())

    # Step 6: Create a list of best days
    best_days = [day for day, count in day_count.items() if count == max_count]

    # Step 7: Randomly select one of the best days if there are ties
    if best_days:  # Ensure there are best days available
        selected_day = random.choice(best_days)
        return selected_day

    return None


def getInfo(result_list,unmatched_group):
    print("RESULT LIST: ", result_list)
    print("LENGTH OF RESULT: ", len(result_list))
    print("UNMATCHED LIST: ",unmatched_group)
    print("LENGTH OF UNMATCHED: ", len(unmatched_group))
