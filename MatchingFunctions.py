

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
    if index_to_delete != -1 and len(templist)< groupsize:
        templist.append(group_pref.iloc[index_to_delete]['Email'])
        group_pref = group_pref.drop([index_to_delete]).reset_index(drop=True)
    
    return group_pref, templist

def finishGroup(group_pref,index_to_delete,result_list,templist,groupsize,unmatched_group,first_row,selected_day):
    #Group 2 checkMatch will always lead to finishGroup
    #Group 3 will skip finishGroup until 3rd row is Found. len(templist) ==2 when 2nd row is found. len(templist) == 3 will trigger grouping
    if index_to_delete != -1 and len(templist)== groupsize:
        result_list.append([templist,selected_day])
        group_pref = group_pref.drop([0]).reset_index(drop=True)
        selected_day = ""  
        templist = []
    if index_to_delete == -1:
        group_pref = group_pref.drop([0]).reset_index(drop=True)
        unmatched_group.append(first_row['Email'])
    return group_pref,result_list,unmatched_group,templist,selected_day

def resultInfo(result_list,unmatched_group):
    print("PAIRS",result_list)
    print(len(result_list))
    print("UNMATCHED",unmatched_group)