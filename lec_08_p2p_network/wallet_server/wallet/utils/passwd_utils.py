import re

from typing import Union

from wallet.config import MIN_LENGTH_OF_PASSWD


def check_passwd_length(passwd: str) -> bool:
    '''비밀번호 길이 검사'''
    passwd_len = len(passwd)
    if passwd_len < MIN_LENGTH_OF_PASSWD:
        return False
    return True


def check_upper_case(passwd: str) -> bool:
    '''대문자 포함 여부 검사'''
    pattern = re.compile('[A-Z]')
    match_str = pattern.search(passwd)
    if match_str:
        return True
    return False
    

def check_special_char(passwd: str) -> bool:
    '''특수문자 검사'''
    pattern = re.compile('\W')
    match_str = pattern.search(passwd)
    if match_str:
        return True
    return False


def check_decimal_number(passwd: str) -> bool:
    '''숫자 포함 검사'''
    pattern = re.compile('[0-9]')
    match_str = pattern.search(passwd)
    if match_str:
        return True
    return False


def check_passwd_strength(passwd: str) -> Union[bool, str]:
    '''비밀번호 강도 조사'''
    check_msg = True
    
    # 최소 글자수 검사
    if check_passwd_length(passwd) is False:
        return f'비밀번호는 최소 {MIN_LENGTH_OF_PASSWD}글자 이상이어야 합니다.'
    # 대문자 포함 검사
    if check_upper_case(passwd) is False:
        return f'비밀번호에는 대문자가 포함되어야 합니다.'
    # 특수문자 검사
    if check_special_char(passwd) is False:
        return f'비밀번호에는 특수문자가 포함되어야 합니다.'
    # 숫자 포함 검사
    if check_decimal_number(passwd) is False:
        return f'비밀번호에는 숫자가 포함되어야 합니다.'
    
    return check_msg