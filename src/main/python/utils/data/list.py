import random
import utils.constants as constants_utils
import utils.debug as debug_utils
import copy
import re
def remove(input_list, string, verbose=False):
    for item in input_list:
        if string in item:
            if verbose:
                print(f'String {string} found in {item}')   
            input_list.remove(item)
        
    return input_list

def diff(input_list1, input_list2,verbose=False):
    if verbose:
        print(f'Length of list 1: {len(input_list1)}')
        print(f'Length of list 2: {len(input_list2)}')
    
    input_list1_sorted = sorted(input_list1)
    input_list2_sorted = sorted(input_list2)

    diff1 = []
    diff2 = []

    for list2_item in input_list2_sorted:
        if list2_item not in input_list1_sorted:
            diff2.append(list2_item)

    for list1_item in input_list1_sorted:
        if list1_item not in input_list2_sorted:
            diff1.append(list1_item)

    return diff1, diff2

def get_random_elements(input_list, number_of_elements, seed=constants_utils.get_seed(), remove=True):
    random.seed(seed)
    random.shuffle(input_list)
    selected_elements = input_list[:number_of_elements]
    if remove:
        input_list = input_list[number_of_elements:]
    return selected_elements

def filter(input_list, filter_list, reverse=False, verbose=False):
    if verbose:
        print(f'Filtering list of length {len(input_list)}')
    filtered_list = copy.deepcopy(input_list)
    for filter_item in filter_list:
        if not reverse:
            filtered_list = [item for item in filtered_list if filter_item not in item]
        else:
            filtered_list = [item for item in filtered_list if filter_item in item]
    return filtered_list

