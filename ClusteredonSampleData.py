import pandas as pd
import random
import MatchingFunctions

class GroupMatcher:
    def __init__(self, csv_file_path):
        # Load the CSV data
        self.data = pd.read_csv(csv_file_path)
        self.unmatched_group = []
        self.result_list = []
        self.paired_list = []
        self.max_count = -1
        self.index_to_delete = -1
        self.definiteMatch = []
        self.columnNames = self.data.columns.tolist()
    
    def process_group(self, groupsize):
        # Filter group based on size
        group_pref = self.data.loc[self.data["Group Size"] == groupsize].copy()
        group_pref.reset_index(drop=True, inplace=True)
        # Exact matching for group size 2
        if groupsize == 2:
            group_pref = MatchingFunctions.exactMatch(group_pref, self.result_list)

        self.paired_list = []
        selected_day = ""
        # Process matching in the group
        while len(group_pref) > 0:
            print(group_pref)
            print("NEW ITERATION")
            first_row = group_pref.iloc[0]
            self.max_count = -1
            self.index_to_delete = -1
            # Add email to a temp list
            if first_row["Email"] not in self.paired_list:
                self.paired_list.append(first_row["Email"])
            # Search for the best matching row
            for i in range(1, len(group_pref)):
                current_row = group_pref.iloc[i]
                # For group size 3, ensure a shared day
                if groupsize == 3:
                    if selected_day:
                        available_days_first = {selected_day}
                    else:
                        selected_day = MatchingFunctions.find_best_day(group_pref)
                        print("SELECTED_DAY", selected_day)
                        available_days_first = {selected_day}
                else:
                    available_days_first = set(day.strip() for day in first_row['Availability'].split(","))
                available_days_current = set(day.strip() for day in current_row['Availability'].split(","))
                common_days = available_days_first.intersection(available_days_current)
                # Use the commonCount method
                if common_days:
                    self.common_count(common_days, first_row, current_row, i)
            # Debugging best match result
            if self.index_to_delete != -1:
                print(
                    f"Matched: {first_row['Email']} with {group_pref.iloc[self.index_to_delete]['Email']} "
                    f"on criteria: {self.definiteMatch}"
                )
            # Check match conditions and finalize group
            group_pref = self.checkMatchConditions(group_pref,groupsize)
            group_pref,selected_day = self.finishGroup(group_pref,first_row,groupsize,selected_day)
    
    def checkMatchConditions(self,group_pref,groupsize):
        #Match
        #Adding the ideal pair to the pairedList. 
        #dropping the candidate from the dataframe
        if self.index_to_delete != -1 and len(self.paired_list)< groupsize:
            print("FoundMatch, templist < groupsize")
            self.paired_list.append(group_pref.iloc[self.index_to_delete]['Email'])
            group_pref = group_pref.drop([self.index_to_delete]).reset_index(drop=True)
            print("PairedList: ",self.paired_list)
        return group_pref

    def finishGroup(self,group_pref,first_row,groupsize,selected_day):
    #Group 2 checkMatch will always lead to finishGroup because length of tempList will hit 2.
    #Group 3 will skip finishGroup until 3rd row is Found. len(templist) ==2 when 2nd row is found. len(templist) == 3 will trigger grouping
        if self.index_to_delete != -1 and len(self.paired_list)== groupsize:
            print("Match made: ",self.paired_list,self.definiteMatch)
            self.result_list.append([self.paired_list,self.definiteMatch])
            #print("RESULT",result_list)
            group_pref = group_pref.drop([0]).reset_index(drop=True)
            #resetting for next iteration
            selected_day = "" 
            self.paired_list = []
        #this is the unmatched group
        if self.index_to_delete == -1:
            print(first_row['Email'], "'s group is unmatched. Dropping both from dataframe")
            #dropping first row since there's no matches. Moving onto the next iteration
            group_pref = group_pref.drop([0]).reset_index(drop=True)
            print("Resetting pairedLists",self.paired_list)
            #if no match... definite match might need to be rest
            self.definiteMatch=[]
            #extend puts them all into a list
            self.unmatched_group.append(self.paired_list)
            self.paired_list = []
            selected_day = "" 
        
        return group_pref,selected_day

    def common_count(self, common_days, first_row, current_row, i):
        """
        Determines the count of matching criteria between two rows and updates the best match variables.
        """
        count = 0
        selected_day = random.choice(list(common_days))
        matched_criteria = []
        #add in which columns I want to use to match people with!
        columns_to_match = ['Classes']
        for column in columns_to_match:
            splitfirst = first_row[column].split(',')
            splitcurr = current_row[column].split(',')
            for element in splitfirst:
                if element in splitcurr:
                    matched_criteria.append(element)
                    count+=1

        if count > self.max_count:
            matched_criteria.append(selected_day)
            self.max_count = count
            self.index_to_delete = i
            self.definiteMatch = matched_criteria
        print("MAX",self.max_count,"INDEX",self.index_to_delete,"MATCHING CRITERIA",self.definiteMatch)

    def getResultList(self):
        return self.result_list
    
    def getUnmatchedList(self):
        return self.unmatched_group
    
    def getColumnNames(self):
        return self.columnNames

