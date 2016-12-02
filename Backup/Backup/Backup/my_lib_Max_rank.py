__author__ = 'Diman'
from gurobipy import *
import pydot # import pydot or you're not going to get anywhere my friend :D
import networkx as nx
import my_lib as my_lib_var
import sys
#import winsound
import time
import itertools
from scipy import stats
import numpy as np
import copy
from my_lib_Max_rank import *
from numpy.linalg import matrix_rank
from my_lib import *

def Greedy_Max_Rank_Unbounded(Cost_routing, R, ProbeCost, green_edges):

  ##############Start Greedy-Max-Rank Algorithm####################################################################################
  print '#################################Start Greedy-Max-Rank Algorithm #######################################################'
  #class Queue:
  #  def __init__(self):
  #    self.items = []
  #  def isEmpty(self):
  #    return self.items == []
  #  def enqueue(self, item):
  #    self.items.insert(0,item)
  #  def dequeue(self):
  #    return self.items.pop()
  #  def size(self):
  #    return len(self.items)
  #q = Queue
  RMaxRank=[]
  temp=[]
  Added =[]
  AddedCost = []
  IncreaseInRank=0
  IncreaseWeight=0
  MaxWeight =0
  currentRank =0
  Max_Increase =0
  sort_index = np.argsort(Cost_routing[:,0])
  Sorted=[]
  Sorted = list(sort_index)
  #sort_index.tolist()
  #sort_index = Cost_routing
  #Sorted = copy.deepcopy(sort_index)
  CostMaxRank=0
  #while (CostMaxRank < ProbeCost):
  for j in Sorted:#sort_index:
    for i in Sorted:#sort_index:
      #print 'I ro print kon'
      #print i
      #print 'RMaxRank'
      #print RMaxRank
      temp= copy.deepcopy(RMaxRank)
      if (temp):
        currentRank = matrix_rank(R[temp,:])
      else:
        currentRank = 0
      if i not in temp:
        temp.append(i)
      IncreaseInRank=  matrix_rank(R[temp,:]) - currentRank
      IncreaseWeight = IncreaseInRank / Cost_routing[i,0]
      #print 'Rank of R'
      #print matrix_rank(R[temp,:])
      #print 'IncreaseInRank'
      #print IncreaseInRank
      #print 'currentRank'
      #print currentRank
      #print 'IncreaseWeight'
      #print IncreaseWeight
      #if i in RMaxRank:
      #  RMaxRank.remove(i)
      #temp.remove(i)
      if (IncreaseWeight > MaxWeight) and ((Cost_routing[i,0]+ CostMaxRank) <= ProbeCost):
        #Print 'Yaftam!'
        #Max_Increase = IncreaseInRank
        #RMaxRank.append(i)
        MaxWeight = IncreaseWeight
        Added=i
        AddedCost = Cost_routing[i,0]
        #print 'Added:'
        #print Added
        #print 'ProbeCossssssssssssssst'
        #print ProbeCost
        #print 'Added Probe Cost:'
        #print (Cost_routing[i,0]+Cost)
        #print 'AddedCost:'
        #print AddedCost
        #currentRank= matrix_rank(R[temp,:])
        #CostMaxRank = CostMaxRank + Cost_routing[i,0]
      if i != Added:
        temp.remove(i)
    if Added not in RMaxRank:
      RMaxRank.append(Added)
      print 'RMaxRank Found:'
      print RMaxRank
      CostMaxRank = CostMaxRank + AddedCost
      #print 'CostMaxRank of Rmin:'
      #print CostMaxRank
      temp.append(Added)
      currentRank = matrix_rank(R[temp,:])
      #temp.remove(Added)
      #sort_index = np.delete(sort_index, Added)
      Sorted.remove(Added)
      #print 'HHHHHHHHHHHHEEEEEEEEEEEEEYYY Print SortIndex'
      #print Sorted
      MaxWeight =0
      IncreaseWeight =0
      #del sort_index[Added]
      #sort_index.delete(Added)
      #Sorted.remove(Added)
  #####################################
  print 'Found R'
  print RMaxRank
  #for x in RMaxRank:
  print 'Maximum Rank:'
  print matrix_rank(R[RMaxRank,:])
  MaxRankMonitors=[]
  for i in RMaxRank:
    #print 'This is which index'
    #print i
    if green_edges[i][0] not in MaxRankMonitors:
      #print 'Source:'
      #print green_edges[i][0]
      MaxRankMonitors.append(green_edges[i][0])
    if green_edges[i][1] not in MaxRankMonitors:
      #print 'Destination:'
      #print green_edges[i][1]
      MaxRankMonitors.append(green_edges[i][1])
  print 'Preserving rank, we have this many monitors:'
  print len(MaxRankMonitors)
  print 'Minimum Number of Probes to preserve Rank:'
  print len(RMaxRank)
  #for x in RMaxRank:
  print 'Rank:'
  print matrix_rank(R[RMaxRank,:])
  MaxRankMonitors=[]
  for i in RMaxRank:
    #print 'This is which index'
    print i
    if green_edges[i][0] not in MaxRankMonitors:
      #print 'Source:'
      #print green_edges[i][0]
      MaxRankMonitors.append(green_edges[i][0])
    if green_edges[i][1] not in MaxRankMonitors:
      #print 'Destination:'
      #print green_edges[i][1]
      MaxRankMonitors.append(green_edges[i][1])
  MaxRank = matrix_rank(R[RMaxRank,:])
  ###########################################################
  #################################################################################
  MaxRankNull = null(R[RMaxRank,:])
  rows= len(MaxRankNull)
  columns = len(MaxRankNull.T)
  print 'Rows'
  print rows
  print 'Columns'
  print columns
  routing_rows = len(R[RMaxRank,:])
  routing_columns = len(R[RMaxRank,:].T)
  print 'Routing rows'
  print routing_rows
  print 'Routing Columns'
  print routing_columns
  iden =1
  MaxRank_Identi_link =0
  #for i in range(0,len(green_edges)-1):
  #  for j in range(0,len(my_null.T)-1):
  for i in range(0,rows):
    #print 'I ro print kon'
    #print i
    for j in range(0,columns):
      #print 'J ro print kon'
      #print j
      if (-1e-12 < MaxRankNull[i][j] < 1e-12) and (iden==1):
        iden=1
      else:
        iden=0
    if (iden == 1):
      MaxRank_Identi_link = MaxRank_Identi_link +1
      #print 'Which Row?'
      #print i
    iden=1
  #################################################################################
  print 'Number of Identofiable links:'
  print MaxRank_Identi_link
  #################################################################################
  #################################################################################
  print 'Maximum Rank is:'
  print MaxRank
  print 'With this rank, we have this many monitors:'
  print len(MaxRankMonitors)
  print 'Minimum Number of Probes to for maximum Rank:'
  print len(RMaxRank)
  print 'Cost of Preserving Rank (Hop count):'
  print CostMaxRank
  print '####################FINISHED MAX-rank algorithm ######################'
  return MaxRank_Identi_link, MaxRank,MaxRankMonitors, RMaxRank, CostMaxRank



def Greedy_Max_Rank_Alg1(Cost_routing, R):
  #Description: This algorithm is the same as Algorithm 1 in http://reports-archive.adm.cs.cmu.edu/anon/cald/CMU-CALD-05-103.pdf
  # This algorithm has (1 - 1/e)/2 approximation with respect to OPT
  ##############Start Greedy-Max-Rank Algorithm####################################################################################
  print '#################################Start Greedy-Max-Rank Algorithm #######################################################'
  #class Queue:
  #  def __init__(self):
  #    self.items = []
  #  def isEmpty(self):
  #    return self.items == []
  #  def enqueue(self, item):
  #    self.items.insert(0,item)
  #  def dequeue(self):
  #    return self.items.pop()
  #  def size(self):
  #    return len(self.items)
  #q = Queue
  RMaxRank=[]
  temp=[]
  Added =[]
  AddedCost = []
  IncreaseInRank=0
  IncreaseWeight=0
  MaxWeight =0
  currentRank =0
  Max_Increase =0
  sort_index = np.argsort(Cost_routing[:,0])
  Sorted=[]
  Sorted = list(sort_index)
  #sort_index.tolist()
  #sort_index = Cost_routing
  #Sorted = copy.deepcopy(sort_index)
  CostMaxRank=0
  #Enumerate all single Elements:#####################
  print 'Start enumerating all single element solutions:'
  A1 =[]
  CostA1 = 0
  FA1=0 # This shows the increase in rank
  tempMaxFA1 = 0
  tempA1 = []
  for k in Sorted:
    tempA1.append(k)
    FA1= matrix_rank(R[tempA1,:])
    if (FA1 > tempMaxFA1) and (Cost_routing[k,0] <= ProbeCost):
      tempMaxFA1 = FA1
      A1 = k
    tempA1.remove(k)
  FA1 = tempMaxA1
  print 'A1'
  print A1
  print 'MaxIncrease in Rank in A1'
  print FA1
  #Finished enumerating all singl items
  #while (CostMaxRank < ProbeCost):
  for j in Sorted:#sort_index:
    for i in Sorted:#sort_index:
      #print 'I ro print kon'
      #print i
      #print 'RMaxRank'
      #print RMaxRank
      temp= copy.deepcopy(RMaxRank)
      if (temp):
        currentRank = matrix_rank(R[temp,:])
      else:
        currentRank = 0
      if i not in temp:
        temp.append(i)
      IncreaseInRank=  matrix_rank(R[temp,:]) - currentRank
      IncreaseWeight = IncreaseInRank / Cost_routing[i,0]
      #print 'Rank of R'
      #print matrix_rank(R[temp,:])
      #print 'IncreaseInRank'
      #print IncreaseInRank
      #print 'currentRank'
      #print currentRank
      #print 'IncreaseWeight'
      #print IncreaseWeight
      #if i in RMaxRank:
      #  RMaxRank.remove(i)
      #temp.remove(i)
      if (IncreaseWeight > MaxWeight) and ((Cost_routing[i,0]+ CostMaxRank) <= ProbeCost):
        #Print 'Yaftam!'
        #Max_Increase = IncreaseInRank
        #RMaxRank.append(i)
        MaxWeight = IncreaseWeight
        Added=i
        AddedCost = Cost_routing[i,0]
        #print 'Added:'
        #print Added
        #print 'ProbeCossssssssssssssst'
        #print ProbeCost
        #print 'Added Probe Cost:'
        #print (Cost_routing[i,0]+Cost)
        #print 'AddedCost:'
        #print AddedCost
        #currentRank= matrix_rank(R[temp,:])
        #CostMaxRank = CostMaxRank + Cost_routing[i,0]
      if i != Added:
        temp.remove(i)
    if Added not in RMaxRank:
      RMaxRank.append(Added)
      print 'RMaxRank Found:'
      print RMaxRank
      CostMaxRank = CostMaxRank + AddedCost
      #print 'CostMaxRank of Rmin:'
      #print CostMaxRank
      temp.append(Added)
      currentRank = matrix_rank(R[temp,:])
      #temp.remove(Added)
      #sort_index = np.delete(sort_index, Added)
      Sorted.remove(Added)
      #print 'HHHHHHHHHHHHEEEEEEEEEEEEEYYY Print SortIndex'
      #print Sorted
      MaxWeight =0
      IncreaseWeight =0
      #del sort_index[Added]
      #sort_index.delete(Added)
      #Sorted.remove(Added)
  #####################################
  print 'Found R'
  print RMaxRank
  #for x in RMaxRank:
  print 'Maximum Rank:'
  print matrix_rank(R[RMaxRank,:])
  MaxRankMonitors=[]
  for i in RMaxRank:
    #print 'This is which index'
    #print i
    if green_edges[i][0] not in MaxRankMonitors:
      #print 'Source:'
      #print green_edges[i][0]
      MaxRankMonitors.append(green_edges[i][0])
    if green_edges[i][1] not in MaxRankMonitors:
      #print 'Destination:'
      #print green_edges[i][1]
      MaxRankMonitors.append(green_edges[i][1])
  print 'Preserving rank, we have this many monitors:'
  print len(MaxRankMonitors)
  print 'Minimum Number of Probes to preserve Rank:'
  print len(RMaxRank)
  #for x in RMaxRank:
  print 'Rank:'
  print matrix_rank(R[RMaxRank,:])
  MaxRankMonitors=[]
  for i in RMaxRank:
    #print 'This is which index'
    print i
    if green_edges[i][0] not in MaxRankMonitors:
      #print 'Source:'
      #print green_edges[i][0]
      MaxRankMonitors.append(green_edges[i][0])
    if green_edges[i][1] not in MaxRankMonitors:
      #print 'Destination:'
      #print green_edges[i][1]
      MaxRankMonitors.append(green_edges[i][1])
  MaxRank = matrix_rank(R[RMaxRank,:])
  ###########################################################
  #################################################################################
  MaxRankNull = null(R[RMaxRank,:])
  rows= len(MaxRankNull)
  columns = len(MaxRankNull.T)
  print 'Rows'
  print rows
  print 'Columns'
  print columns
  routing_rows = len(R[RMaxRank,:])
  routing_columns = len(R[RMaxRank,:].T)
  print 'Routing rows'
  print routing_rows
  print 'Routing Columns'
  print routing_columns
  iden =1
  MaxRank_Identi_link =0
  #for i in range(0,len(green_edges)-1):
  #  for j in range(0,len(my_null.T)-1):
  for i in range(0,rows):
    #print 'I ro print kon'
    #print i
    for j in range(0,columns):
      #print 'J ro print kon'
      #print j
      if (-1e-12 < MaxRankNull[i][j] < 1e-12) and (iden==1):
        iden=1
      else:
        iden=0
    if (iden == 1):
      MaxRank_Identi_link = MaxRank_Identi_link +1
      #print 'Which Row?'
      #print i
    iden=1
  #################################################################################
  print 'Number of Identofiable links:'
  print MaxRank_Identi_link
  #################################################################################
  #################################################################################
  print 'Maximum Rank is:'
  print MaxRank
  print 'With this rank, we have this many monitors:'
  print len(MaxRankMonitors)
  print 'Minimum Number of Probes to for maximum Rank:'
  print len(RMaxRank)
  print 'Cost of Preserving Rank (Hop count):'
  print CostMaxRank
  print '####################FINISHED MAX-rank algorithm ######################'
  return MaxRank_Identi_link, MaxRank,MaxRankMonitors, RMaxRank, CostMaxRank
  
