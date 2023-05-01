import requests
import os
from dao import DAO


def download_cover(url, pic_name, rec_date):
    pic_name = pic_name+'.jpg'
    year_date = rec_date[:-2]
    fold_dir_month = os.path.join('../covers',year_date)
    fold_dir_day = os.path.join(fold_dir_month, rec_date)
    file_dir = os.path.join(fold_dir_day, pic_name)
    try:
        os.mkdir(fold_dir_month)
        os.mkdir(fold_dir_day)
    except FileExistsError:
        print(rec_date, url)

    img_response = requests.get(url, headers={'Referer': 'https://www.pixiv.net/'}, stream=True)
    if img_response.status_code == 200:
        with open(file_dir, 'wb') as file:
            for chunk in img_response.iter_content(1024):
                file.write(chunk)
        print(pic_name+" downloaded successfully.")
    else:
        print("Failed to load "+pic_name)


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
        print(info_str)
        if len(splits) == 5:
            pname = splits[4]+'_'+pname
        download_cover(img_url, pname, pdate)
