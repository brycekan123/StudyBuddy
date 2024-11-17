import pandas as pd
import random
import MatchingFunctions

class GroupMatcher:
    def __init__(self, csv_file_path):
        # Load the CSV data
        self.data = pd.read_csv(csv_file_path)
        self.unmatched_group = []
        self.result_list = []

    def process_group(self, groupsize):
        # Filter group based on size
        group_pref = self.data.loc[self.data["Group Size Preference"] == groupsize].copy()
        group_pref.reset_index(drop=True, inplace=True)

        # Exact matching for group size 2
        if groupsize == 2:
            group_pref = MatchingFunctions.exactMatch(group_pref, self.result_list)

        pairedlist = []
        selected_day = ""

        # Process matching in the group
        while len(group_pref) > 0:
            print("NEW ITERATION")
            first_row = group_pref.iloc[0]
            max_count = -1
            index_to_delete = -1
            print("!!!selectedDay new iteration,", selected_day)

            # Add email to a temp list
            if first_row["Email"] not in pairedlist:
                pairedlist.append(first_row["Email"])

            # Search for the best matching row
            for i in range(1, len(group_pref)):
                current_row = group_pref.iloc[i]
                count = 0

                # For group size 3, ensure a shared day
                if groupsize == 3:
                    #a day has been selected. 
                    if selected_day:
                        available_days_first = {selected_day}
                        print("Day has been chosen. Sticking with this day: ", available_days_first)
                    else:
                        selected_day = MatchingFunctions.find_best_day(group_pref)
                        print("SELECTED_DAY", selected_day)
                        available_days_first = {selected_day}
                else:
                    available_days_first = set(day.strip() for day in first_row['Availability'].split(";"))

                available_days_current = set(day.strip() for day in current_row['Availability'].split(";"))
                common_days = available_days_first.intersection(available_days_current)

                print("days in common", common_days)
                #index_to_delete,definiteMatch,max_count = MatchingFunctions.bestDay()
                #on each row, count how many matches have been done
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
            print(first_row["Email"], group_pref.iloc[index_to_delete]["Email"], "Matched on this criteria: ", definiteMatch)
            
            # Check match conditions and finalize group
            group_pref, pairedlist = MatchingFunctions.checkMatchConditions(
                group_pref, index_to_delete, pairedlist, groupsize
            )
            group_pref, pairedlist, selected_day = MatchingFunctions.finishGroup(
                group_pref, index_to_delete, self.result_list, pairedlist, groupsize, self.unmatched_group, first_row, selected_day, definiteMatch
            )
            print("END OF ITERATION. Selected day is: ", selected_day)
    
    
    def match_groups(self):
        group_sizes = [2, 3]
        for group_size in group_sizes:
            self.process_group(group_size)
        MatchingFunctions.getInfo(self.result_list, self.unmatched_group)
        result_df = pd.DataFrame(self.result_list)
        unmatched_df = pd.DataFrame(self.unmatched_group)

        # Save to CSV
        result_df.to_csv('matched_groups.csv', index=False)
        unmatched_df.to_csv('unmatched_groups.csv', index=False)

        print("Results saved to 'matched_groups.csv' and 'unmatched_groups.csv'")
    
# Path to your CSV file
csv_file_path = '/Users/brycekan/Desktop/StudyBuddyNov17/StudyBuddy/testSampleData.csv'

# Create an instance of the matcher and start matching
matcher = GroupMatcher(csv_file_path)
matcher.match_groups()
