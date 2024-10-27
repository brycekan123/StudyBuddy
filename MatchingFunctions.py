

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

