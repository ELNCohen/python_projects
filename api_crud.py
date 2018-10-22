from requests import put, get

get('http://127.0.0.1:5000/todos').json()
put('http://127.0.0.1:5000/todos/todo3', data={'task': 'build ANOTHER API'}).json()
put('http://127.0.0.1:5000/todos/todo2', data={'task': 'placeholder'}).json()
