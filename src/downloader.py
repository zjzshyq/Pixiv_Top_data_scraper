import requests
import os
from dao import DAO


def download_cover(url, pic_name, rec_date):
    pic_name = pic_name+'.jpg'
    fold_dir = '../covers/'+rec_date
    file_dir = os.path.join(fold_dir, pic_name)
    try:
        os.mkdir(fold_dir)
    except FileExistsError:
        return FileExistsError

    img_response = requests.get(url, headers={'Referer': 'https://www.pixiv.net/'}, stream=True)
    if img_response.status_code == 200:
        with open(file_dir, 'wb') as file:
            for chunk in img_response.iter_content(1024):
                file.write(chunk)
        return pic_name+" downloaded successfully."
    else:
        return "Failed to load "+pic_name


if __name__ == '__main__':
    # img_url = 'https://i.pximg.net/c/240x480/img-master/img/2023/04/15/00/01/02/107177439_p0_master1200.jpg'
    dao = DAO()
    while True:
        info_str = dao.img_queue_pop()
        if info_str is None:
            break
        splits = info_str.split(';')
        pname = splits[1]+"_"+splits[0]
        pdate = splits[2]
        img_url = splits[3]
        res = download_cover(img_url, pname, pdate)
        print(res)
