import client

m_client = client.Client()

# reset users list
with open('users.json', 'w') as f:
    f.write('{}')

# reset passwords list
with open('passwords.json', 'w') as f:
    f.write('{}')

# test user creation and authentication
assert m_client.create_account('hrh14', 'hrh')
assert not m_client.create_account('hrh14', 'hrh123')
assert m_client.authenticate_account('hrh14', 'hrh')
assert m_client.create_account('hrh13', 'hhh')

# test add and read
assert m_client.add('www.google.com', '111')
assert not m_client.add('www.google.com', '111')
assert m_client.read('www.google.com') == '111'
assert m_client.add('www.bing.com', '222')
assert m_client.read('www.youtube.com') is None

# test update
assert m_client.update('www.google.com', '222')
assert m_client.read('www.google.com') == '222'
assert m_client.read('www.google.com') != '111'

# test remove
assert m_client.remove('www.google.com')
assert m_client.read('www.google.com') is None
assert not m_client.read('www.youtube.com')

# test log out
assert m_client.log_out()
assert m_client.read('www.bing.com') is None
assert m_client.authenticate_account('hrh14', 'hrh')
assert m_client.read('www.bing.com') == '222'
assert m_client.log_out()
assert m_client.authenticate_account('hrh13', 'hhh')

# test change password
assert m_client.change_mpw('qqq')
assert m_client.add('www.google.com', '007')
assert m_client.read('www.google.com') == '007'
assert m_client.remove('www.google.com')
assert m_client.log_out()
assert m_client.authenticate_account('hrh13', 'qqq')

# test multi-user
new_client = client.Client()
new_client.copy(m_client)
assert new_client.authenticate_account('hrh14', 'hrh')
assert new_client.read('www.bing.com') == '222'
assert m_client.add('www.google.com', 'abc')
assert m_client.read('www.google.com') == 'abc'
