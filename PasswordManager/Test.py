import client

client = client.Client()

# reset users list
with open('users.json', 'w') as f:
    f.write('{}')

# reset passwords list
with open('passwords.json', 'w') as f:
    f.write('{}')

# test user creation and authentication
assert client.create_account('hrh14', 'hrh')
assert not client.create_account('hrh14', 'hrh123')
assert client.authenticate_account('hrh14', 'hrh')
assert client.create_account('hrh13', 'hhh')

# test add and read
assert client.add('www.google.com', '111')
assert not client.add('www.google.com', '111')
assert client.read('www.google.com') == '111'
assert client.add('www.bing.com', '222')
assert client.read('www.youtube.com') is None

# test update
assert client.update('www.google.com', '222')
assert client.read('www.google.com') == '222'
assert client.read('www.google.com') != '111'

# test remove
assert client.remove('www.google.com')
assert client.read('www.google.com') is None
assert not client.read('www.youtube.com')


# test log out
assert client.log_out()
assert client.read('www.bing.com') is None
assert client.authenticate_account('hrh14', 'hrh')
assert client.read('www.bing.com') == '222'
assert client.log_out()
assert client.authenticate_account('hrh13', 'hhh')

# test change password
assert client.change_mpw('qqq')
assert client.add('www.google.com', '007')
assert client.read('www.google.com') == '007'
assert client.remove('www.google.com')
assert client.log_out()
assert client.authenticate_account('hrh13', 'qqq')
