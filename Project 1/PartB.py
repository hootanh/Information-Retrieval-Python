# Name: Hootan Hosseinzadeganbushehri


import sys, re


'''
    This function is getting the file name as a parameter. It 
    opens the specified text file and read through all lines  
    independent of capitalization. It also turn all characters 
    to lower characters and gets rid off all extra character 
    except the alphanumeric characters which are "a" through 
    "z" and "0" to "9" in the tokens(words). Finally, it creates 
    a set of all the tokens(words) and returns it from the
    function. Complexity time for this function is O(n^2) since 
    it has a nested for loop.    
'''
def _read_process(a_file):
    infile = open(a_file, 'r')
    text = infile.read()
    words = text.lower().split()
    filters = re.compile('[^a-z0-9]')
    result = [re.split(filters, word) for word in words]
    infile.close()
    result = [j for i in result for j in i if j]
    return set(result)


'''
    This function takes two sets of tokens(words) as the
    parameters which is created by the _read_process function.
    It finds out the intersection between these two sets and
    makes a list of the common tokens(words). Finally, the
    function returns the length of the created list of common
    tokens(words) which is an integer representing that how 
    many common tokens(words) are in both given sets.
    Complexity time for this function is O(n).
'''
def _token_matching(set_1, set_2):
    return len(list(set_1 & set_2))
    
    
if __name__ == '__main__':
    if len(sys.argv) == 3:
        temp_1 = _read_process(sys.argv[1])
        temp_2 = _read_process(sys.argv[2])
        print(_token_matching(temp_1, temp_2))