import requests, os, redis

def download_cover(url, sub_name, date):
    fname = sub_name+'.jpg'
    fold_dir = './src/covers/'+date
    file_dir = os.path.join(fold_dir, fname)
    try:
        os.mkdir(fold_dir)
    except:
        1

    img_response = requests.get(url, headers={'Referer': 'https://www.pixiv.net/'}, stream=True)
    if img_response.status_code == 200:
        with open(file_dir, 'wb') as file:
            for chunk in img_response.iter_content(1024):
                file.write(chunk)
        print(fname+" downloaded successfully.")
    else:
        print("Failed to load "+fname)

def sav2rd(pid, page_dict):
    rd = redis.Redis(host='localhost', port=6379, db=0)
    dict_drop_none = {}
    for k in page_dict:
        dict_drop_none[k] = '' if page_dict[k] is None else page_dict[k]
    rd.hmset(pid, dict_drop_none)

def sav2csv():
    1

def rd2csv():
    1


if __name__=='__main__':
    sav2rd('test', {'a':1,'b':2,})
