import requests
import hashlib
import sys

def request_api_data(req_char):
    url = ('https://api.pwnedpasswords.com/range/') + req_char
    res= requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching {res.status_code}')
    return res

def get_password_leak_count(hashes, hash_to_check):
    hashes= (line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:
        if h == hash_to_check:
            return count
    return 0



def pwned_password_check(password):
    sha1password= hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leak_count(response,tail)

def main():
    input_password = input('Enter password: ')

    count =  pwned_password_check(input_password)
    if count:
        print(f'{input_password} was found {count} you should probably change it')

    else:
        print(f'{input_password} was not found. You can proceed')

#main(sys.argv[1:])


if __name__ == '__main__':
    main()