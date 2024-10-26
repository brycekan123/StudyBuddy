

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
        templist.append(group_pref.iloc[index_to_delete]['Email'])
        group_pref = group_pref.drop([index_to_delete]).reset_index(drop=True)
    return group_pref, templist
#         print("hit")
#         print(result_list)

