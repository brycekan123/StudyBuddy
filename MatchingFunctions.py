

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
    if index_to_delete != -1 and len(templist)< groupsize:
        # print("inside group")
        # print(group_pref)
        # print(group_pref.iloc[index_to_delete]['Email'])
        templist.append(group_pref.iloc[index_to_delete]['Email'])
        group_pref = group_pref.drop([index_to_delete]).reset_index(drop=True)
    return group_pref, templist

def finishGroup(group_pref,index_to_delete,result_list,templist,groupsize,unmatched_group,first_row,selected_day):
    if index_to_delete != -1 and len(templist)== groupsize:
        result_list.append([templist,selected_day])
        group_pref = group_pref.drop([0]).reset_index(drop=True)
        selected_day = ""  
        templist = []
    else:
        group_pref = group_pref.drop([0]).reset_index(drop=True)
        unmatched_group.append(first_row['Email'])
    return group_pref,result_list,unmatched_group,templist,selected_day
