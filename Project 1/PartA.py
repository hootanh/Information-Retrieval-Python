# Name: Hootan Hosseinzadeganbushehri


import sys, re


'''
    This function is getting the file name as a parameter. It 
    opens the specified text file and read through all lines  
    independent of capitalization. It also turn all characters 
    to lower characters and gets rid off all extra character 
    except the alphanumeric characters which are "a" through 
    "z" and "0" to "9" in the tokens(words). Finally, it counts 
    all the tokens(words) inside the file and keeps track of 
    each word within a dictionary. Complexity time for this 
    function is O(n^2) since it has a nested for loop.    
'''
def _read_process(a_file):
    answer = {}
    infile = open(a_file, 'r')
    text = infile.read()
    words = text.lower().split()
    filters = re.compile('[^a-z0-9]')
    result = [re.split(filters, word) for word in words]
    infile.close()
    result = [j for i in result for j in i if j]
    for i in result:
        if i in answer:
            answer[i] += 1
        else:
            answer[i] = 1
    return answer


'''
    This function receives a dictionary as a parameter created 
    by _read_process function which is a dictionary of 
    tokens(words) as keys and values are their count of their
    appearance in the text. Finally, it prints out the sorted 
    output from the dictionary by their decreasing frequency. 
    (so, highest frequency words first). Resolve ties alphabetically
    and in ascending order. Complexity time for this function is
    O(n Log n) since it uses the sorted Python built-in function.
'''
def _print_result(a_dict):
    for k, v in sorted(a_dict.items(), key = lambda x: (-x[1], x[0])):
        print(k + "\t" + str(v))
    

if __name__ == '__main__':
    if len(sys.argv) == 2:
        final_result = _read_process(sys.argv[1])
        _print_result(final_result)