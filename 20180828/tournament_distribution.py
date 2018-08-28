#-*- coding:utf-8 -*-

import numpy as np
import random

def Nseed_group(Nseed, ranker_team, team_participant):
    #Input
    #Nseed: Number of seeds
    #ranker_team(vector): seed_team[i] means the team number of the (i+1)th ranker
    #team_participant: Number of participants of each teams (NumPy vector)
    team_ranker=cal_team_ranker(team_participant.shape[0], ranker_team)
    
    #Output
    #group list
    
    #get group list including only rankers
    group_list=groups_only_ranker(ranker_team)
    
    #add empty groups (unseed blocks) into group list
    group_list=add_empty_groups(group_list, np.max(team_participant))
    
    #unranker distribution
    team_unranker=team_participant-team_ranker    ##Number of unrankers of each teams
    group_list=dist_unranker(group_list, team_unranker, team_participant)
    
    return group_list
    
def cal_team_ranker(n_group, ranker_team):
    team_ranker=np.zeros(n_group)
    
    for i in range(n_group):
        team_ranker[i]=np.sum(ranker_team==(i+1))
        
    return team_ranker

def NumOfDigits_2(x):
    #Input
    #x: number
    
    #Output
    #k: the integer as "2^(k-1) < x <= 2^k"
    
    k=1
    while pow(2, k)<x:
        k+=1
        
    return k

def add_empty_groups(group_list, max_team_participant):
    #add empty groups (unseed blocks)
    #Input
    #group_list: group list with only seed blocks
    #max_team_participant: max number of one team participants (add empty blocks as number of blocks >= 2^k between two seed blocks)
    
    #Output
    #
    k1=pow(2, NumOfDigits_2(max_team_participant))
    k2=len(group_list)
    
    while k2<k1:
        temp=[]
        for i in range(np.int(k2/2)):
            temp.append(group_list[2*i])
            temp.append([])
            temp.append([])
            temp.append(group_list[2*i+1])
        
        group_list=temp
        k2=len(group_list)
        
    return group_list

def groups_only_ranker(ranker_team):
    #Input
    #ranker_team(vector): ranker_team[i] means the team number of the (i+1)th ranker
    
    #Output
    #groups(list): 
    
    #get the order of seeds in tournament 
    position=np.array([1, 2])
    p=1
    N=ranker_team.shape[0]
    while N>pow(2, p):
        i=0
        while i<pow(2, p-1):
            position=np.r_[position[:4*i+1], np.zeros(2), position[4*i+1:]]
            i+=1

        i=0
        while i<pow(2, p):
            if position[2*i]==0:
                position[2*i]=pow(2, p+1)+1-position[2*i+1]
            else:
                position[2*i+1]=pow(2, p+1)+1-position[2*i]
            i+=1    
        p+=1
    
    #make list of seed groups
    groups=[]
    for i in range(N):
        groups.append([ranker_team[np.int(position[i]-1)]])
        
    return groups

def dist_unranker(group_list, team_unranker, team_participant):
    for i in range(team_unranker.shape[0]):
        group_list=add_teamx(group_list, i+1, np.int(team_unranker[i]), np.int(team_participant[i]))
        
    return group_list

def add_teamx(group_list, x, added_n, group_n):
    digit=NumOfDigits_2(group_n)
    for i in range(added_n):
        group_list=add_teamx_one(group_list, pow(2, digit), x)
        
    return group_list

def add_teamx_one(group_list, group_num, x):
    num_group_teamx=np.zeros(group_num)
    num_group_allteam=np.zeros(group_num)
    
    num_partition=np.int(len(group_list)/group_num)
    
    for i in range(group_num):
        num_group_teamx[i]=np.sum(np.array([b for a in group_list[num_partition*i:num_partition*(i+1)] for b in a])==x)
        num_group_allteam[i]=len([b for a in group_list[num_partition*i:num_partition*(i+1)] for b in a])
        
    few_teamx_group_index=[]
    few_allteam_group_index=[]
    
    for i in range(group_num):
        if num_group_teamx[i]==np.min(num_group_teamx):
            few_teamx_group_index.append(i)
            
        if num_group_allteam[i]==np.min(num_group_allteam):
            few_allteam_group_index.append(i)
            
    index=choice_index(few_teamx_group_index, few_allteam_group_index)
    if num_partition==1:
        group_list[index].append(x)
    else:
        group_list[num_partition*index:num_partition*(index+1)]=add_teamx_one_partly(group_list[num_partition*index:num_partition*(index+1)], x)
    return group_list

def choice_index(few_teamx_group_index, few_allteam_group_index):
    commons=list(set(few_teamx_group_index) & set(few_allteam_group_index))
    if len(commons)==0:
        index=random.choice(few_teamx_group_index)
    elif len(commons)==1:
        index=commons[0]
    else:
        index=random.choice(commons)
        
    return index
    
def add_teamx_one_partly(group_list_partly, x):
    num_participants_in_partly_groups=np.zeros(len(group_list_partly))
    for i in range(num_participants_in_partly_groups.size):
        num_participants_in_partly_groups[i]=len(group_list_partly[i])
        
    few_allteam_partly_group_index=[]
    for i in range(num_participants_in_partly_groups.size):
        if num_participants_in_partly_groups[i]==np.min(num_participants_in_partly_groups):
            few_allteam_partly_group_index.append(i)
            
    index=few_allteam_partly_group_index[np.random.choice(len(few_allteam_partly_group_index))]
    group_list_partly[index].append(x)
    return group_list_partly

ranker_team=np.array([1, 4, 7, 3, 2, 6, 7, 12, 3, 2, 18, 15, 21, 4, 1, 3])
team_participant=np.array([12, 18, 10, 8, 16, 13, 12, 14, 7, 5, 6, 9, 7, 11, 5, 4, 8, 8, 9, 10, 13, 12])

temp=Nseed_group(16, ranker_team, team_participant)

for i in temp:
    print(i)
