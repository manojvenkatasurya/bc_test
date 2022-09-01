from multiprocessing import Process
import requests
import time
import ed25519
import json


def client(cid, url, data):
    private_key, public_key = ed25519.create_keypair()
    pay_load = {"cid": cid, "public_key": public_key.to_ascii(
        encoding='hex').decode()}
    print(pay_load)
    res = requests.post(url=url + '/client', data=json.dumps(pay_load))
    if res.status_code != 200:
        print('server rejected public key')
        print(res.json())
        exit(1)
    print('client created successfully')
    i = 1
    while True:
        start = time.time()
        data['person_id'] = cid + str(i)
        msg = json.dumps(data)
        print(msg)
        signature = sign(msg, private_key)
        pay_load = {"cid": cid,
                    "data": msg,
                    "signature": signature}
        res = requests.post(url=url + '/clientdata', data=json.dumps(pay_load))
        if res.status_code != 200:
            print(res.status_code)
            print(res.json())
            print('data rejected by server' + str(pay_load))
        else:
            print('data accepted by server')
        i += 20
        end = time.time()
        time.sleep(1.0-float(end-start))
        if i >= 60:
            break


def create_clients(data, cid, count, url):
    for i in range(count):
        clid = str(i) + str(id)
        p = Process(target=client, args=(clid, url, data))
        p.daemon = True
        p.start()


def sign(data, private_key):
    msg_bytes = data.encode()
    signature = private_key.sign(msg_bytes, encoding='hex')
    return signature.decode()


def main():
    url = 'http://127.0.0.1:8000'
    sample_data = {"person_id": "123",
                   "name": "sample name"}
    create_clients(sample_data, 'PYCLI', 10)


sample_data = {"person_id": "123",
               "name": "sample name"}
client('cidtest', 'http://127.0.0.1:8000', sample_data)
