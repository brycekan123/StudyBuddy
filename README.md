Ever feel too shy to approach other students in a classroom but want to find someone to endure a difficult class with? 
Look no further :) 
# Study Buddy: Find someone to study with based on your similar backgrounds!

I created an application for students to find other classmates to study with based on their similar backgrounds. Here is how it works.
- 1st: each class will be provided a [form](https://airtable.com/app7s0IDdvLDs3Hwo/pagz52hHoU25j2eE3/form) for the students to fill out. Ex: 
- 2nd: Individuals who want to participate will provide information such as how many people in their study group, availability, preferred location, research interests and more.
- 3rd: after 48 hours, the form will close and I will run my custom matching algorithm(more explained below) to match people based on these preferences.
- 4th: I'll automatically create a discord group with the matched individuals and provide them on what information they matched on.

# Matching Algorithm:
## StudyBuddyDriver.py 
the main driver that creates a GroupMatcher object with the csv filepath runs the code to process each groupsize(2 or 3).
## ClusteredonSampleData.py 
A class to process each group size specifically based on availability and similarity.
  ### process_group: 
  creates a copy of the dataframe based on the groupsize and iterates through all the individuals(row). First, I'll compare the first row's availabiltieis with every row. 
  If the current row has same available days, I will compare the similarities in answers(columns) to the first row. 
   - common_count: The row with the highest matches will be paired with the first row, adding them both to the paired list and removing them from the dataframe.
   - checkMatchConditions: If the group size == 3, I will keep the first row in the dataframe instead as I need to find the 3rd individual to match. Repeat and iterate through entire dataframe for another match.
   - finishGroup: Once the pairedList == groupsize, I'll add them to the result list with their matched criteria. If indviiduals are unmatched, I'll add them to the unmatched List.

# Future challenges:
- Currently, I have to create a new form per classroom. This limits the scope of our audience as it would be ideal to have a universal form that students 
can fill out across campus and enter which class they'd want to be matched in.
- Matching is not done instantaneously. I currently have to wait until everyone fills out the form befoe matching individuals. I would have to keep a storage of available individuals
and query the storage everytime someone fills out the form
- My matching algorithm is quite inefficient as I am interating through a dataframe and its columns several times to check for similarities across individuals.
After learning ML and AI, I would like to implement clustering algorithms or nearest neighbors to better match individuals efficiently.
