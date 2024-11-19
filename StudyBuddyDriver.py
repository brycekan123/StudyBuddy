from ClusteredonSampleData import GroupMatcher


import pandas as pd
def run_matching():
    # Set the path to your CSV file
    csv_file_path = '/Users/brycekan/Desktop/StudyBuddyNov17/StudyBuddy/testSampleData.csv'  # Update with your actual path.

    # Initialize the GroupMatcher with the CSV file path
    matcher = GroupMatcher(csv_file_path)

    # Call the match_groups method to perform the matching
    group_sizes = [2,3]
    for group_size in group_sizes:
        matcher.process_group(group_size)
    getInfo(matcher.getResultList(), matcher.getUnmatchedList())
    result_df = pd.DataFrame(matcher.getResultList())
    unmatched_df = pd.DataFrame(matcher.getUnmatchedList())

    # Save to CSV
    result_df.to_csv('matched_groups.csv', index=False)
    unmatched_df.to_csv('unmatched_groups.csv', index=False)

    print("Results saved to 'matched_groups.csv' and 'unmatched_groups.csv'")

print("Group matching process completed!")

def getInfo(result_list,unmatched_group):
    print("RESULT LIST: ", result_list)
    print("LENGTH OF RESULT: ", len(result_list))
    print("UNMATCHED LIST: ",unmatched_group)
    print("LENGTH OF UNMATCHED: ", len(unmatched_group))

if __name__ == "__main__":
    # This will run the run_matching function when executing this file.
    run_matching()
