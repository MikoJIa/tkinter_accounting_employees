from datetime import datetime

l = ['01.03.24', '11.01.24', '12.04.24', '15.03.24', '16.04.24', '17.04.24', '17.04.24']
array = sorted(l, key=lambda k: datetime.strptime(k, '%d.%m.%y'), reverse=False)
print(array)