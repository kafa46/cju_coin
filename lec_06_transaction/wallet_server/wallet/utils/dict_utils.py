import collections

def sorted_dict_by_key(unsorted_dic: dict):
    '''사전의 key 값에 따라 일정하게 정렬하여
    동일한 dict는 동일한 hash 값을 보장하는 함수'''
    # return collections.OrderedDict(
    #     sorted(unsorted_dic.items()), key=lambda keys: keys[0]
    # )
    return sorted(unsorted_dic.items())