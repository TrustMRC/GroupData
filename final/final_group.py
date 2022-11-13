from Levenshtein import distance
import numpy as np
import json
from tqdm import tqdm
from utils import refine_context

dataset = [json.loads(line)for line in open("mrc_interpretation_B.txt").readlines()]

distance_mat = np.zeros((len(dataset),len(dataset)))
for i in tqdm(range(len(dataset))):
    text1 = refine_context(dataset[i]['context'])
    for j,data in zip(range(i,len(dataset)),dataset[i:]):
        text2 = refine_context(data['context'])
        # normalize levenshtein distance
        distance_mat[i][j] = distance(text1,text2) / (len(text1)+len(text2))
        distance_mat[j][i] = distance_mat[i][j]

fails = []
groups_1 = set()
THRESHOLD_1 = 0.27 # setting the THRESHOLD_1 to the 0.27
unpair_set = set()
paired_set = set()
from tqdm import tqdm
for i in tqdm(range(len(distance_mat))):
    pairs_index = np.where(distance_mat[i]<THRESHOLD_1)[0]
    if len(pairs_index) == 1 and i not in paired_set:
        unpair_set.add(i)
        continue
    mark = True
    # ensure all set are equal in one group
    for idx in pairs_index:
        dst = np.where(distance_mat[idx]<THRESHOLD_1)[0]
        # not equal
        if len(dst) != len(pairs_index) or not (dst == pairs_index).all():
            fails.append((i,dst,pairs_index))
            mark = False
    if mark:
        groups_1.add(tuple(pairs_index.tolist()))
        paired_set = paired_set.union(set(pairs_index))
    else:
        unpair_set.add(i)

full_set = set(list(range(len(dataset))))
done_set = unpair_set.union(paired_set)
assert done_set == full_set, print(full_set - done_set)
print(len(unpair_set))
print(len(fails))


groups_1 = [list(group) for group in groups_1]
groups_1.sort(key=lambda x:x[0])


unpair_set = list(unpair_set)
unpair_set.sort()
groups_2 = set()
groups_3 = set()
for idx in unpair_set:
    # print(idx)
    # print(dataset[idx]['context'])
    dst = np.where(distance_mat[idx]<0.45)[0] # allivate the threhold get more match
    if len(dst) >= 2:
        groups_2.add(tuple(dst.tolist()))
    else:
        # even worse
        groups_3.add(idx)
    # print(json.dumps(dst.tolist()))
    # print(json.dumps([dataset[j]['context'] for j in dst],indent=4,ensure_ascii=False))
    # print()
groups_2 = [list(group) for group in groups_2]
groups_2.sort(key=lambda x:x[0])

groups_3 = list(groups_3)
groups_3.sort()
groups_3 = [[unit] for unit in groups_3]

check_set = set()
for group in groups_1:
    for unit in group:
        assert unit not in check_set
        check_set.add(unit)

def check_in_pair(group:list):
    ret = set()
    for ele in group:
        if ele in check_set:
            for unit_group in groups_1:
                if ele in unit_group:
                    ret.add(tuple(unit_group))
                    
    return ret


match_result = {
    'groups_2':{},
    'groups_3':{}
}
for k,groups in zip(['groups_2','groups_3'],[groups_2,groups_3]):
    for group in groups:
        match_group = check_in_pair(group)
        if len(match_group) > 0:
            match_result[k][tuple(group)] = match_group


#### merge

final_groups = []
final_set = set()
for _,results in match_result.items():
    for k,v in results.items():
        unit_group = set(k)
        for auto_group in v:
            unit_group = unit_group.union(set(auto_group))
        final_groups.append(list(unit_group))
        final_set = final_set.union(unit_group)
for groups in [groups_1,groups_2,groups_3]:
    for unit_group in groups:
        if len(set(unit_group).intersection(final_set)) == 0:
            final_groups.append(unit_group) 
            final_set = final_set.union(set(unit_group))

assert set(list(range(len(dataset)))) == final_set

final_groups.sort(key=lambda x:x[0])
refine_dataset = [[dataset[idx] for idx in group] for group in final_groups]
with open('refine_dataset.json','w') as f:
    json.dump(refine_dataset,f,indent=4,ensure_ascii=False)
