
# coding: utf-8

# In[1]:

### SQUARES

import numpy as np
import pycosat
import itertools
import random
import time


# In[1]:

def encode_sudoku_as_cnf(doku, show):
    n = len(doku)
    names = initialize_names(n)
    cnf = []
    cnf = encode_exactly_one(cnf, names, show)
    cnf = encode_row(cnf,names,show)
    cnf = encode_column(cnf,names,show)
    cnf = encode_region(cnf,names)
    if show:
        print("the doku is now translated to propositional logic in cnf format")
    return cnf

def initialize_names(n):
    names = np.zeros([n,n,n],dtype=np.int)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                names[i][j][k]= i*n**2 + j*n + k+1
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
    for i in range(n):
        for j in range(n):
            if show:
                print("in row ", i, ", column", j, ", there may only be at most 1 number, hence the following clauses:")
            for k in range(n):
                for l in range(1,n-k):
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

def encode_row(cnf, names, show):
    if show:
        print("")
        print("enter encode_row function")
        print("")
    n = len(names)
    for i in range(n):
        for k in range(n):
            at_least_clause = []
            if show:
                print("in row ", i, ", there may not be more than one", k+1)
            for j in range(n): 
                at_least_clause.append(names[i][j][k])
                at_most_clause = []
                for l in range(1,(n)-j):
                    at_most_clause = [-1*names[i][j][k], -1*names[i][j+l][k]]
                    cnf.extend([at_most_clause])
                    if show:
                        print(at_most_clause)
            cnf.extend([at_least_clause])
            if show:
                print("but there must be at least one ", k+1)
                print(at_least_clause)                
    return cnf

# def encode_column(cnf, names, show):
#     names_t = transpose_3d(names)   
#     names_t = names_t.tolist()
#     cnf = encode_row(cnf, names_t, show)
#     return cnf
def encode_column(cnf, names, show):
    if show:
        print("")
        print("enter encode_column function")
        print("")
    n = len(names)
    for j in range(n):
        for k in range(n):
            at_least_clause = []
            if show:
                print("in col ", j, ", there may not be more than one", k+1)
            for i in range(n): 
                at_least_clause.append(names[i][j][k])
                at_most_clause = []
                for l in range(1,(n)-j):
                    at_most_clause = [-1*names[i][j][k], -1*names[i][j+l][k]]
                    cnf.extend([at_most_clause])
                    if show:
                        print(at_most_clause)
            cnf.extend([at_least_clause])
            if show:
                print("but there must be at least one ", k+1)
                print(at_least_clause)                
    return cnf

def transpose_3d(names):
    n = len(names)
    names = np.asarray(names)
    names_t = names
    for i in range(n):
        names_t[i] = names[i].transpose()
    return names_t

def encode_region(cnf, names):
    n = int(np.sqrt(len(names)))
    for i in range(n):
        for j in range(n):
            region = collect_region(i, j, names)
            for k in range(n**2):
                at_least_clause = []
                for l in range(n**2):
                    at_least_clause.append(region[k][l])
                    for m in range(l+1, n**2):
                        at_most_clause = [ -region[l][k], -region[m][k] ]
                        cnf.extend([at_most_clause])
                cnf.extend([at_least_clause])
    return cnf
    
def collect_region(x, y, names):
    n = len(names)
    n = int(np.sqrt(n))
    names = np.asarray(names)
    region = names[x*n:x*n+n,y*n:y*n+n,:]
    region_list = []
    for n in region:
        for i in n:
            region_list.append(i.tolist())
    names.tolist()
    return region_list

def encode_givens(names, puzzle, show):
    givens = []
    n = len(names)
    for i in range(n):
        for j in range(n):
            for k in range(0,n):
                if puzzle[i,j] == k+1:
                        clause = [names[i][j][k]]
                        givens.extend([clause])
                if puzzle[i,j] == 0:
                    continue
            if show:
                print("givens-clause: ", clause)
    return givens 

def gen_full_sudoku(n):
    basis = np.zeros((n**2,n**2))
    cnf = encode_sudoku_as_cnf(basis, False)
    sol = next(pycosat.itersolve(cnf))
    j = 0
    full = np.zeros(n**4)
    for i in sol:
        if i > 0:
            value = i%(n**2)
            if value == 0:
                value = n**2
            full[j] = value
            j += 1
    doku = np.reshape(full,(n**2, n**2))
    return doku

def construct_database_fulls(sizes):
    for n in sizes:
        k = 50 # amount of puzzles to generate per size/order
        for i in range(k):
            doku = gen_full_sudoku(n)
            filename_small = "Square_sudoku_order" + str(n) + "_#" +str(i)+ "_full"
            np.savetxt(filename_small, doku, fmt='%i', delimiter=',', newline='\n' )        
        collect_smalls_to_big(n, k-1, "_full")

def collect_smalls_to_big(nRings, nPuzzles, kind):
    filename_big = "SquareSudokuDatabase_for_size_" + str(nRings) + kind
    with open(filename_big, 'w'): pass # clear the file
    f=open(filename_big,'ab')
    for i in range(nPuzzles):
        filename_small = "Square_sudoku_order"+str(nRings)+"_#"+str(i)+ kind
        doku = np.loadtxt(filename_small, delimiter=',')
        np.savetxt(f, doku, fmt='%i', delimiter=',', newline='\n' )
    f.close()
    
def reduce_sudoku(basic_rules, r, doku):
    counter=0
    n = len(doku)
    names = initialize_names(n)
    while counter < r:
        row = np.random.randint(0,n)
        col = np.random.randint(0,n)
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

def reduce_database(order):
    n = order**2
    basis = np.zeros((n, n))
    basic_rules = encode_sudoku_as_cnf(basis, False)
    r = int(.5*n**2) # we remove half the numbers in the puzzle
    dokus = load_sudoku_database(order, "_full")
    for i in range(len(dokus)):
        doku = dokus[i]
        red_doku = reduce_sudoku(basic_rules, r, doku)
        filename_small = "Square_sudoku_order" + str(order) + "_#" +str(i)+ "_reduced"
        np.savetxt(filename_small, doku, fmt='%i', delimiter=',', newline='\n' )        
    collect_smalls_to_big(order, len(dokus), "_reduced")

def load_sudoku_database(n, kind):
    kind = "_"+kind
    filename = "SquareSudokuDatabase_for_size_"+str(n)+ kind
    a = load_database_file(filename, n)
    return a

def load_database_file(filename, n):
    a = np.loadtxt(filename, delimiter=',' )
    nDoku = int(len(a)/(n**2))
    a = a.reshape(((nDoku, n**2, n**2)))
    return a

#for n in [2,3,4]:
   #  reduce_database(n)
    
def to_DIMAC_file(encoding, filename,n):
        with open(filename, 'w') as f:
            print("p cnf {} {}".format(n*((2*n)**2), len(encoding)), file=f)
            for clause in encoding:
                for literal in clause:
                    print(literal, " ", end='', file=f)
                print("0", file=f)



# determine variables per clause for square sudoku's

def var_per_clause_square(n): 
    a = load_sudoku_database(n, "_reduced")
    names = initialize_names(n)
    cnf = encode_sudoku_as_cnf(a[0], False)
    cnf.extend(encode_givens(names, a[0], False))
    n_clauses = len(cnf)
    var_per_clause = 0
    for clause in cnf:
        var_per_clause += len(clause)
    var_per_clause = var_per_clause/n_clauses
    return var_per_clause

