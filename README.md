
# TODO

Create a node(server) and client(s) to replicate blockchain functionality

## Use case - Setup
—  There are N clients with their own identities. The identity consists of a {public, private} key-pair. N can be 10 or some decent number.

—  There is a node (a server) that receives signed messages from the clients. The clients can use any protocol, such as TCP, HTTP, etc. to talk to the node. The node also has its own identity.

—  The node will persist the messages received from the clients, so some form of permanent data store is used. The implementation can use simple file-based storage, a key-value store, or an RDBMS. Keep it simple. 

—  The interaction between clients and the node can be implemented in the client/server or peer-to-peer (p2p) model.

—  The clients and node can be on the same physical machine. 

## Use case - Test description
—  Generate identities for N clients.

—  Define a message of your choice. The message can be modeled in JSON or any format of your choice. The message schema is known to both the clients and the node. 

—  Each client generates a message, signs it, and sends the signed message to the node. Each client is configured to generate and send a message every second, for 1 minute.

—  The node validates the message received as follows:
1:  The message schema is valid.
2:  The message is signed.
3:  The signature is valid and the message indeed came from the client who sent it.

—  If the validation succeeds, the node persists the message in the order the message was received.

—  When the number of messages received reaches 100, the node processes the messages as follows.
1:  Plucks the 100 messages from its queue.
2:  Creates a hash of those messages.
3:  Signs the hash.
4:  Persists the signed hash, hash, and the 100 messages in a separate list. The order of the entry (block) in the list is the order in which the group of 100 messages arrived at the node. To keep the test simple, there is no blockchain created, but a simple list of blocks.

—  The node exposes the following APIs, which can be called by the clients. Depending on the implementation, this can be just methods to call on the node, HTTP endpoints, etc. So, define the API format as required.
1:  Get the number of completed blocks.
2:  Get the block identified by index in the list.

Please identify the test cases, describe them, and demonstrate that the implementation passes the test cases.

A subset of the above functionality can be implemented, if the effort goes beyond a typical weekend’s worth of work. Please spell out what is excluded when submitting the work.

## Bonus points

The following features earn extra credits. One or more of the following can be implemented.

—  When the node creates blocks, create a Merkle tree of 100 messages. This produces Merkle root hash. Sign this hash and persist it.

—  Create a blockchain instead of the simple list of blocks. Each block contains the hash of the previous block, so you can traverse the chain from the latest to the oldest block.

—  With blockchain implemented, provide an API to get the latest (head) block.

—  With blockchain implemented and given a block hash, provide an API to retrieve the previous block.
Implement encryption so the messages sent by the clients can only be decrypted by the node. The clients encrypt the messages using node’s public key, so only the node can decrypt the message using its private key.


# Approach

-- Use FastAPI as a node to handle client requests and create block(as specified) as a backend job.

-- Use multiprocessing to create clients and send the requests with raw data to node.

-- Use file system to store keys


# Installation

## Node installation
-- Navigate to node folder

-- create a virtual env 

-- Install all requirements in that env using pip install -r requirements.txt

-- Activate the environment

-- Run the command to start fastapi server. "uvicorn src.main:app"

-- I have choosen fastapi server, because it has advantages such as concurrent execution using asyncio implementation, in-built swagger documentation for all API's created.

Note

-- API to store client keys and add data to queue will be used by client

-- API to get the block and check the count of blocks can be checked from swagger.

-- By default fastapi runs on uvicorn server and its default port is 8000

-- URL for swagger: http://127.0.0.1:8000/docs

## Client installation
-- Navigate to client folder

-- create a virtual env 

-- Install all requirements in that env using pip install -r requirements.txt

-- Activate the environment

-- Run python main.py to start cretion and execution of client

-- This program will spawn mutiple processes where each process represents an individual client.

-- Each client will will send the sample of data for every one second for 60 seconds