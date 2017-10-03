
# coding: utf-8

# In[2]:

import numpy as np
import pycosat
import itertools
import random
import time


# In[3]:

# this cell is responsible for generating cnf files that represent circledoku's

# taken out cnf.extend(encode_givens(names,doku,show)) for convience in reducing sodoku function
def encode_doku_as_cnf(doku, show):
    n = len(doku)
    names = initialize_names(n)
    cnf = []
    cnf = encode_exactly_one(cnf, names, show)
    cnf = encode_ring(cnf,names,show)
    cnf = encode_wedge(cnf,names,show)
    cnf = encode_slice(cnf,names)
    cnf.extend(encode_givens(names,doku,show))
    if show:
        print("the doku is now translated to propositional logic in cnf format")
    return cnf

def initialize_names(n):
    names = np.zeros([n,2*n,2*n],dtype=np.int)
    for i in range(n):
        for j in range(2*n):
            for k in range(2*n):
                names[i][j][k]= i*(2*n)**2 + j*2*n + k+1
    return names.tolist()

def encode_exactly_one(cnf, names, show):
    if show:
        print("enter function encode_exactly_one")
    cnf.extend(encode_at_most_one(cnf, names, show))
    cnf.extend(encode_at_least_one(cnf, names, show))
    return cnf

def encode_at_most_one(cnf, names, show):
    if show:
        print("enter function encode_at_most_one")
    n = len(names)
    #enc = []
    for i in range(n):
        for j in range(2*n):
            if show:
                print("in row ", i, ", column", j, ", there may only be at most 1 number, hence the following clauses:")
            for k in range(2*n):
                for l in range(1,(2*n)-k):
                    arr = [-1*names[i][j][k],-1*names[i][j][k+l]]
                    if show:
                        print(arr)
                    per_entry = cnf.insert(0,arr)
    return cnf

def encode_at_least_one(cnf,names,show):
    if show:
        print("enter function encode_at_least_one")
        print("for every field we expect a clause of", len(names[0]), "positive literals:")
    for i in names:
        atleast=[]
        for j in i:
            atleast.append(j)
            if show:
                print(j)
        cnf.extend(atleast)
    return cnf

def encode_ring(cnf, names, show):
    if show:
        print("")
        print("enter encode_ring function")
        print("")
    n = len(names)
    for i in range(n):
        for k in range(2*n):
            at_least_clause = []
            if show:
                print("in row ", i, ", there may not be more than one", k+1)
            for j in range(2*n): 
                at_least_clause.append(names[i][j][k])
                at_most_clause = []
                for l in range(1,(2*n)-j):
                    at_most_clause = [-1*names[i][j][k], -1*names[i][j+l][k]]
                    cnf.extend([at_most_clause])
                    if show:
                        print(at_most_clause)
            cnf.extend([at_least_clause])
            if show:
                print("but there must be at least one ", k+1)
                print(at_least_clause)                
    return cnf

def encode_wedge(cnf, names, show):
    if show:
        print("")
        print("enter encode_wedge_function")
        print("")
    n = len(names) # n is number of rings, but also number of wedges
    # first, collect all the variables that stand for a number "1" (or"k") in a wedge
    # then, construct clauses that say one of these variables must be true
    # but no more than one of thesevariables may be true
    for w in range(n): # per wedge
        for k in range(2*n): # per number
            wedge_content = []
            for i in range(n): # per row
                for j in range(2*w, 2*w+2): # per column
                    wedge_content.append(names[i][j][k])
            cnf.extend([wedge_content])
            if show:
                print("in wedge ", w, "there must be the number", k+1)
                print(wedge_content)
                print("but only one ", k+1)
            for l in range(2*n): # loop over the wedgecontent
                for m in range(1, 2*n - l):
                    clause = [-1*wedge_content[l], -1*wedge_content[l+m]]
                    if show:
                        print(clause)
    return cnf

def encode_slice(cnf, names):
    n = len(names)
    for i in range(n):
        sliced = getslice(i,names)
        atleast_n =[]
        comb_n = []
        for l in range(2*n):
            atleast= [k[l] for k in sliced]
            atleast_n.append(atleast)
            atleast_neg = [-x for x in atleast]
            comb = [list(z) for z in itertools.combinations(atleast_neg,2)]
            atleast_n.extend(comb)
        cnf.extend(atleast_n)
    return cnf

def getslice(k,names):
    slice_C = []
    n = len(names)
    for i in range(n):
        for j in range(k,2*n,n):
            a = names[i][j]
            slice_C.append(a)
    return slice_C

def encode_givens(names, puzzle, show):
    givens = []
    n = len(names)
    for i in range(n):
        for j in range(2*n):
            for k in range(0,2*n):
                if puzzle[i,j] == k+1:
                        clause = [names[i][j][k]]
                        givens.extend([clause])
                if puzzle[i,j] == 0:
                    continue
            
            if show:
                print("givens-clause: ", clause)
    return givens  

def gen_full_circledoku(n):
    basis = np.zeros((n,2*n))
    cnf = encode_doku_as_cnf(basis,False)
    sol  = next(pycosat.itersolve(cnf))
    j = 0
    full = np.zeros(n*(2*n))
    for i in sol:
        if i > 0:
            value = i%(2*n)
            if value == 0:
                value = 2*n
            full[j] = value
            j += 1
    doku = np.reshape(full,(n,2*n))
    return doku


# In[4]:

# this cell is responsible for the functions that can generate the database of full valid circledoku's

def construct_database_fulls(sizes):
    for n in sizes:
        k = 50 # amount of puzzles to generate per size/nRings
        for i in range(k):
            #tic = time.clock()
            doku = gen_full_circledoku(n)
            #toc = time.clock()
            #print("Circledoku order:", n, ", nr: ", i, " took ", toc-tic, "seconds")
            filename_small = "CircleDoku_nrings" + str(n) + "_#" +str(i)+ "_full"
            np.savetxt(filename_small, doku, fmt='%i', delimiter=',', newline='\n' )        
        collect_smalls_to_big(n, k-1, "_full")
        
def collect_smalls_to_big(nRings, nPuzzles, kind):
    filename_big = "CircleDokuDatabase_for_size_" + str(nRings) + kind
    with open(filename_big, 'w'): pass # clear the file
    f=open(filename_big,'ab')
    for i in range(nPuzzles):
        filename_small = "CircleDoku_nrings"+str(nRings)+"_#"+str(i)+ kind
        doku = np.loadtxt(filename_small, delimiter=',')
        np.savetxt(f, doku, fmt='%i', delimiter=',', newline='\n' )
    f.close()
    
def load_circleDoku_database(n, kind):
    kind = "_"+kind
    filename = "CircleDokuDatabase_for_size_"+str(n)+ kind
    a = load_database_file(filename, n)
    return a

def load_database_file(filename, n):
    a = np.loadtxt(filename, delimiter=',' )
    nDoku = int(len(a)/n)
    a = a.reshape(((nDoku, n, 2*n)))
    return a

def merge_database_files(n, file_in_1, file_in_2, file_out):
    a = load_database_file(file_in_1, n)
    b = load_database_file(file_in_2, n)
    a_len = len(a)
    b_len = len(b)
    c_len = a_len + b_len
    c = np.zeros((c_len, n, 2*n))
    c[:len(a)] = a
    c[len(a):] = b
    f=open(file_out,'ab')
    for i in range(c_len):
        doku = c[i]
        np.savetxt(f, doku, fmt='%i', delimiter=',', newline='\n' )
    f.close()

# this call, if un-commented, will fill the database of full valid circledoku's
# construct_database_fulls([2,3,4,6,7,10])


# In[4]:

# this cell is responsible for taking a full valid circledoku
# and stripping it down to a proper one with a fixed amount of givens

def reduce_circledoku(basic_rules, r, doku):
    counter=0
    n = len(doku)
    names = initialize_names(n)
    while counter < r:
        row = np.random.randint(0,n)
        col = np.random.randint(0,2*n)
        save = doku[row][col]
        if doku[row][col] == 0:
            continue
        else:
            doku[row][col] = 0
        basic_rules.extend(encode_givens(names,doku,False))
        sol= 0
        for i in pycosat.itersolve(basic_rules):
            sol+=1
            if sol > 1:
                doku[row][col] = save
                break
        if sol == 1:
            counter+=1
    return doku

def reduce_database(nRings):
    basis = np.zeros((nRings,2*nRings))
    basic_rules = encode_doku_as_cnf(basis, False)
    r = nRings**2 # we remove half the numbers in the puzzle
    dokus = load_circleDoku_database(nRings, "_full")
    for i in range(len(dokus)):
        doku = dokus[i]
        red_doku = reduce_circledoku(basic_rules, r, doku)
        filename_small = "CircleDoku_nrings" + str(nRings) + "_#" +str(i)+ "_reduced"
        np.savetxt(filename_small, doku, fmt='%i', delimiter=',', newline='\n' )        
    collect_smalls_to_big(nRings, len(dokus)-1, "_reduced")

# # the following call will reduce all full puzzles in the database
#for n in [2,3,4,6,7]:    
 #   reduce_database(n)


# In[13]:

def to_DIMAC_file(encoding, filename,n):
        with open(filename, 'w') as f:
            print("p cnf {} {}".format(n*((2*n)*2*n), len(encoding)), file=f)
            for clause in encoding:
                for literal in clause:
                    print(literal, " ", end='', file=f)
                print("0", file=f)

                
def var_per_clause_circle(n): 
    a = load_circleDoku_database(n, "_reduced")
    names = initialize_names(n)
    cnf = encode_doku_as_cnf(a[0], False)
    cnf.extend(encode_givens(names, a[0], False))
    n_clauses = len(cnf)
    var_per_clause = 0
    for clause in cnf:
        var_per_clause += len(clause)
    var_per_clause = var_per_clause/n_clauses
    return var_per_clause







