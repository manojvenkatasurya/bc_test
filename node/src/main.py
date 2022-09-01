from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.validators import validator as schema
import aiofiles
import ed25519
import jsonschema
import json
import queue
import hashlib

app = FastAPI()
q = queue.Queue(maxsize=2)
blocks = []


@app.on_event("startup")
async def startup_event():
    global private_key, public_key
    private_key, public_key = ed25519.create_keypair()
    print('startup event')


@app.on_event("shutdown")
async def startup_event():
    print('shutdown event')


@app.post("/client")
async def read_client(data: schema.Client):
    try:
        async with aiofiles.open(data.cid + 'pubkey.txt', mode='w') as f:
            await f.write(data.public_key)
        return JSONResponse(status_code=200, content={"msg": "Client public key stored successfully"})
    except Exception:
        return JSONResponse(status_code=500, content={"msg": "Failed storing Client public key"})


def validateJson(jsonData):
    try:
        jsonschema.validate(instance=jsonData, schema=schema.personSchema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


def get_hash(msg):
    msg_bytes = msg.encode()
    hash_msg = hashlib.sha3_256(msg_bytes)
    return hash_msg.hexdigest()


def create_block(q, bl):
    msgs = []
    print('started obtaining messages')
    while not q.empty():
        msg = q.get()
        msgs.append(msg)
    print('obtained messages')
    msgs_block = dict(messages=msgs)
    block_hash = get_hash(json.dumps(msgs_block))
    msg_bytes = json.dumps(msgs_block).encode()
    sign_hash = private_key.sign(msg_bytes, encoding='hex')
    block = {'signed_hash': sign_hash.decode(),
             'hash': block_hash, 'messages': msgs_block}
    blocks.append(block)
    print(blocks)


@app.post("/clientdata")
async def read_client_data(data: schema.ClientData):
    try:
        person_id = data.cid
        msg = data.data
        signature = data.signature
        async with aiofiles.open(data.cid+'pubkey.txt', mode='r') as f:
            contents = await f.read()
        pub_key = contents.encode()
        vk = ed25519.VerifyingKey(pub_key, encoding='hex')
        vk.verify(signature.encode(), data.data.encode(), encoding='hex')
        if validateJson(json.loads(data.data)):
            q.put(data.data)
            qw = q
            if q.full():
                #TODO create a fastapi background task here
                print('block creation started')
                create_block(q, blocks)
                print('block creation completed')
            return JSONResponse(status_code=200, content={"msg": "Data validated"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"msg": "signature or schema validaton failed"})
    return JSONResponse(status_code=500, content={"msg": "signature or schema validaton failed"})


@app.get("/blocks")
async def get_blocks_count():
    return JSONResponse(status_code=200, content={"active_blocks": len(blocks)})


@app.get("/blocks/{id}")
async def get_blocks_count(id: int):
    print(blocks)
    try:
        return JSONResponse(status_code=200, content={"block": blocks[id]})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"msg": "block with index does not exists"})
