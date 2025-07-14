import sys                                # Mengakses fungsi-fungsi sistem seperti keluar dari program
import hashlib                            # Untuk membuat hash SHA-256
import json                               # Untuk mengubah data Python jadi JSON dan sebaliknya
from time import time                     # Mengambil waktu saat ini (timestamp)
from uuid import uuid4                    # Untuk membuat ID unik (UUID)
from flask import Flask                   # Membuat server API dengan Flask
from flask.globals import request         # Mengambil data dari request (misalnya POST data)
from flask.json import jsonify            # Mengubah data Python jadi JSON untuk response
import requests                           # Untuk mengirim request HTTP (misalnya POST ke node lain)
from urllib.parse import urlparse         # Memecah URL menjadi bagian2: domain, path, dll


class Blockchain (object) :
       # set difficulty target
       difficulty_target = "0000"
       
       # fungsi untuk menghitung hash block
       def hash_block(self, block) :
              # mengubah data block menjadi string - lalu diubah ke byte
              block_encoded = json.dumps(block, sort_keys=True).encode()
              
              # mengubah byte ke string hex
              return hashlib.sha256(block_encoded).hexdigest()
       
       # fungsi constructor untuk mengenerate genesis block (blok pertama)
       def __init__(self):
              # list kosong untuk menyimpan block
              self.chain = []
              
              # list kosong untuk menyimpan transaksi sementara
              self.current_transactions = []
              
              # membuat genesis block / block pertama
              genesis_hash = self.hash_block("genesis_block")
              
              # menambahkan block pertama ke blockchain
              self.append_block (
                     # menambahkan previous block ke blockchain
                     hash_of_previous_block = genesis_hash,
                     
                     # menambahkan nonce previous block ke blockchain
                     nonce = self.proof_of_work(0, genesis_hash, [])
              )
       
       # fungsi untuk mencari nonce yang cocok dengan difficulty target
       def proof_of_work(self, index, hash_of_previous_block, transactions) :
              nonce = 0
              
              while self.valid_proof(index, hash_of_previous_block, transactions, nonce) is False :
                     nonce += 1
              return nonce
       
       # fungsi validasi hash untuk mencari nonce yang cocok dengan difficulty target
       def valid_proof(self, index, hash_of_previous_block, transactions, nonce) :
              # simpan dalam konten berbentuk string byte
              content = f'{index}{hash_of_previous_block}{transactions}{nonce}'.encode()
              
              # hasing content
              content_hash = hashlib.sha256(content).hexdigest()
              
              return content_hash[:len(self.difficulty_target)] == self.difficulty_target
       
       # fungsi untuk menambahkan block
       def append_block(self, nonce, hash_of_previous_block) :
              block = {
                     "index" : len(self.chain),
                     "timestamp" : time(),
                     "transaction" : self.current_transactions,
                     "nonce" : nonce,
                     "hash_of_previous_block" : hash_of_previous_block,
              }
              
              # reset pending transaction karena transaction berhasil dilakukan
              self.current_transactions = []
              
              # tambahkan block ke chain
              self.chain.append(block)
              
              return block
       
       # fungsi untuk menambahkan data transaksi
       def add_transaction(self, sender, recipient, amount) :
              # menambahkan transaksi ke dalam list transaksi untuk memberikan reward untuk penambang
              self.current_transactions.append({
                     "amount" : amount,
                     "recipient" : recipient,
                     "sender" : sender       
              })
              
              return self.last_block["index"] + 1
       
       @property
       def last_block(self) :
              return self.chain[-1]             


app = Flask(__name__)

# address untuk penambang
node_identifier = str(uuid4()).replace('-', "")

blockchain = Blockchain()

# routes menampilkan data block
@app.route('/blockchain', methods=['GET'])
def full_chain() :
       response = {
              'chain' : blockchain.chain,
              'length' : len(blockchain.chain)
       }
       
       return jsonify(response), 200

# route untuk melakukan mining dan memberikan reward kepada penambang
@app.route('/mine', methods=['GET'])
def mine_block() :
       blockchain.add_transaction(
              sender = "0",
              recipient = node_identifier,
              amount = 1
       )
       
       last_block_hash = blockchain.hash_block(blockchain.last_block)
       
       index = len(blockchain.chain)
       nonce = blockchain.proof_of_work(index, last_block_hash, blockchain.current_transactions)
       
       block = blockchain.append_block(nonce, last_block_hash)
       response = {
              "message" : "Block baru telah ditambahkan {mined}",
              "index" : block["index"],
              "timestamp" : block["timestamp"],
              "hash_of_previous_block" : block["hash_of_previous_block"],
              "nonce" : block["nonce"],
              "transaction" : block["transaction"]
       }
       return jsonify(response), 200

# route untuk menambahkan transaksi
@app.route('/transaction/new', methods=['POST'])
def new_transaction() :
       values = request.get_json()
       
       # validasi input
       required_fields = ["sender", "recipient", "amount"]
       
       # cek validasi input jika False
       if not all (k in values for k in required_fields) :
              return ('Missing fields', 400)
       
       # cek validasi input jika True
       index = blockchain.add_transaction(
              values['sender'],
              values['recipient'],
              values['amount']
       )
       
       response = {'message' : f'Transaksi akan ditambahkan ke blok {index}'}
       
       return jsonify(response), 201

# run server API
if __name__ == '__main__':
       app.run(host='0.0.0.0', port=int(sys.argv[1]))