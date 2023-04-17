import os
try:
    os.mkdir('../data')
    os.mkdir('../covers')
except Exception as e:
    print(e)
