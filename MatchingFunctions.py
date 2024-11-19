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
            key = list(key)
            result_list.append([listofemails,key])
    return group_pref_2

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
        #print("Available days:", availability)
        for day in availability:
            day = day.strip()  # Strip whitespace
            
            # Only count if the day is in the first row's days
            if day in day_count:
                day_count[day] += 1  # Increment count

    print("Day counts:", day_count)

    # Step 5: Find the maximum count value
    max_count = max(day_count.values())

    # Step 6: Create a list of best days
    best_days = [day for day, count in day_count.items() if count == max_count]

    # Step 7: Randomly select one of the best days if there are ties
    if best_days:  # Ensure there are best days available
        selected_day = random.choice(best_days)
        return selected_day

    return None


