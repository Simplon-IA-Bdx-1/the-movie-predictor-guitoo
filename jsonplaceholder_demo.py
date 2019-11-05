#!/usr/bin/env python3

import requests
from pprint import pprint


print('Get first post:')
result = requests.get('https://jsonplaceholder.typicode.com/posts/1')
print(f'status code: {result.status_code}')
print(f'header keys: {list(result.headers.keys())}')
print('content type: {}'.format(result.headers['Content-Type']))
result_json=result.json()
pprint(result_json)

print('Get the body of the post:')
body=result_json['body']
print(body)

print('Get the list of all the post by Id 1 and print the first one')
result = requests.get('https://jsonplaceholder.typicode.com/posts?userId=1')
pprint(result.json()[0])

print('Post a post:')
result = requests.post('https://jsonplaceholder.typicode.com/posts', data={'title':'title', 'body':'test'})
pprint(result.json())

print('Post a post with json')
result = requests.post('https://jsonplaceholder.typicode.com/posts', json={'body':'test', 'body':'test'})
pprint(result.json())

print('Replace the first post:')
result = requests.put('https://jsonplaceholder.typicode.com/posts/1', data={'title':'title', 'body':'test'})
pprint(result.json())

print('Modifiy the body of the first post:')
result = requests.patch('https://jsonplaceholder.typicode.com/posts/1', data={'body':'test'})
pprint(result.json())
