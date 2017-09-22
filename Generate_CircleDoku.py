
# coding: utf-8

# In[2]:

import numpy as np
#import pycosat
import timeit
import time
t = timeit.Timer('char in text', setup='text = "sample string"; char = "g"')


# In[3]:

# this cell is concerned with generating valid filled circledokus

# for a circledoku of 3 rings we represent in an array as follows
#
# ring:
# [[1 1 1 1 1 1]
#  [0 0 0 0 0 0]
#  [0 0 0 0 0 0]]
#
# slice:
# [[1 0 0 1 0 0]
#  [1 0 0 1 0 0]
#  [1 0 0 1 0 0]]
#
# wedge:
# [[1 1 0 0 0 0]
#  [1 1 0 0 0 0]
#  [1 1 0 0 0 0]]

def gen_full_circledoku(n): # a circledoku with n-rings
    # this function fills a circledoku with a valid configuration
    # it is later filtered to become a unique proper puzzle with minimal givens
    succes = False
    while not succes: 
        # if the computer runs into a dead-end by random assignment, just stop and start over
        # this is very inefficient especially for larger circledoku's
        # but in this generation step we are not troubled by efficiency
        succes, doku = attempt_full_circledoku(n)
#         print("succes")
#         print(succes)
#         print("doku")
#         print(doku)
#         print("")
    return doku
            
def attempt_full_circledoku(n):
    maxDigit = 2*n
    doku = np.zeros((n, maxDigit), dtype=np.int)
    for i in range(n):
        for j in range(maxDigit):
            gen = [i, j, np.random.randint(1, maxDigit+1)]
            count = 1
            while not is_gen_valid(doku, gen):
                gen = [i, j, np.random.randint(1, maxDigit+1)]
                count += 1
                if count > maxDigit*3:
                    return False, doku
            doku[i, j] = gen[2]
    return True, doku

def is_gen_valid(doku, gen):
    # variable 'gen' is the digit the algorithm wants to genereate at certain position
    # its syntax is [x, y, digit]
    if is_gen_valid_for_ring(doku, gen) and is_gen_valid_for_slice(doku, gen) and is_gen_valid_for_wedge(doku, gen):
        return True
    else:
        return False
    
def is_gen_valid_for_ring(doku, gen):
    ring_content = doku[gen[0]][:]
    if gen[2] in ring_content:
        return False
    else:
        return True

def is_gen_valid_for_slice(doku, gen):
    n = len(doku)
    n_slice = gen[1] % n
    slice_content = doku.transpose()[n_slice::n][:]
    if gen[2] in slice_content:
        return False
    else:
        return True
    
def is_gen_valid_for_wedge(doku, gen):
    n = len(doku)
    n_wedge = int(gen[1] / 2)
    wedge_content = doku.transpose()[n_wedge*2:n_wedge*2+2][:]
    if gen[2] in wedge_content:
        return False
    else:
        return True


#for n in range(2,6):
 #   for i in range(4): 
   #     #start = t.timeit()
  #      start = time.clock()
    #    doku = gen_full_circledoku(n)
     #   filename = 'valid_circledoku_' + str(n) +'_rings_#'+str(i)
      #  np.savetxt(filename, doku, fmt='%i', delimiter=',', newline='\n' )
       # #end = t.timeit()
        #print("generating ", filename, " took ", time.clock() - start, "seconds")
        


# In[5]:

#a = gen_full_circledoku(5)

#a


# In[10]:

#np.savetxt("cdokutestfive", a, fmt='%i', delimiter=',', newline='\n' )
    


# In[ ]:



