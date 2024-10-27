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


def checkMatchConditions(group_pref,index_to_delete,templist,groupsize):
    #Match
    print("in matchConditions")
    if index_to_delete != -1 and len(templist)< groupsize:
        print("FoundMatch, templist < groupsize")
        templist.append(group_pref.iloc[index_to_delete]['Email'])
        group_pref = group_pref.drop([index_to_delete]).reset_index(drop=True)
        print("TEMPLIST",templist)

    return group_pref, templist

def finishGroup(group_pref,index_to_delete,result_list,templist,groupsize,unmatched_group,first_row,selected_day,definiteMatch):
    #Group 2 checkMatch will always lead to finishGroup
    #Group 3 will skip finishGroup until 3rd row is Found. len(templist) ==2 when 2nd row is found. len(templist) == 3 will trigger grouping
    print(group_pref)

    if index_to_delete != -1 and len(templist)== groupsize:
        print("templist is groupsize",templist,definiteMatch)
        result_list.append([templist,definiteMatch])
        #print("RESULT",result_list)
        group_pref = group_pref.drop([0]).reset_index(drop=True)
        print("after drop",group_pref)
        selected_day = ""  
        templist = []
    if index_to_delete == -1:
        print("umatched",first_row['Email'], "going to be dropped")
        print("UNMATCHING",group_pref)

        group_pref = group_pref.drop([0]).reset_index(drop=True)
        print(group_pref)
        print("TEMPLIST",templist)
        #if no match... definite match might need to be rest
        definiteMatch=[]
        unmatched_group.append(templist)
        templist = []
    return group_pref,result_list,unmatched_group,templist,selected_day


def find_best_day(group_df):
    # Step 1: Create a dictionary to count occurrences of each day
    day_count = {}

    # Step 2: Iterate over each row in the DataFrame
    for i in range(len(group_df)):
        availability = group_df['Availability'].iloc[i].split(';')
        
        for day in availability:
            day = day.strip()  # Strip whitespace
            
            # Only proceed if the day is not empty
            if day:  
                if day in day_count:
                    day_count[day] += 1  # Increment count if day already exists
                else:
                    day_count[day] = 1  # Initialize count for new day

    # Step 3: Check if day_count is empty
    if not day_count:
        return None

    # Step 4: Find the maximum count value
    max_count = max(day_count.values())

    # Step 5: Create a list of best days
    best_days = []
    for day, count in day_count.items():
        if count == max_count:
            best_days.append(day)  # Add to best days if count matches max_count

    # Step 6: Randomly select one of the best days if there are ties
    if best_days:  # Ensure there are best days available
        selected_day = random.choice(best_days)
        return selected_day

    return None  # Return None if no best days were found

def getInfo(result_list,unmatched_group):
    print("RESULT LIST: ", result_list)
    print("LENGTH OF RESULT: ", len(result_list))
    print("UNMATCHED LIST: ",unmatched_group)
    print("LENGTH OF UNMATCHED: ", len(unmatched_group))
