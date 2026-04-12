import requests

url = 'https://doriane.pythonanywhere.com/'
print('URL:', url)
res = requests.get(url)
print('STATUS', res.status_code)
print('CSS LINES:')
for line in res.text.splitlines():
    if 'styles.css' in line:
        print(line)
print('\nHEAD:')
print('\n'.join(res.text.splitlines()[:80]))
