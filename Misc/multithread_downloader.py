from urllib.request import urlopen
import urllib
import os, threading, sys
from tqdm import tqdm

def download_path(link, save_in="."):
    try:
        response = urlopen(link)
        file_ = link.split(r"/")[-1]
        urllib.request.Request(link, method="HEAD")
        get_head = urlopen(link)
        if get_head.status == 200:
            print(file_, "size:" ,get_head.headers["Content-Length"])
            size = get_head.headers["Content-Length"]
            if not size:
                raise Exception("Could not recover the size of " + link)
            size = int(size)
        else:
            raise Exception("Could not recover the size of " + file_)
        CHUNK = 20 * 1024
        with open(os.path.join(save_in, file_), "wb") as f:
            pbar = tqdm(total=size)
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)
                pbar.update(CHUNK)
            pbar.close()
    except Exception as e:
        print(e)
    return

def download_list(list_, save_in="."):
    threads = [threading.Thread(None, target=download_path, args=(l,save_in)) for l in list_]
    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    links = ['https://mirror.aarnet.edu.au/pub/ubuntu/releases/20.04.3/ubuntu-20.04.3-desktop-amd64.iso',
             'http://mirror.internode.on.net/pub/centos/8.4.2105/isos/x86_64/CentOS-8.4.2105-x86_64-dvd1.iso']
    download_list(links)
