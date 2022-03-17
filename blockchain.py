#! /usr/bin/env python3
import json 
import hashlib
from time import time


class Blockchain:
	
	def __init__(self):
		self.chain = []
		self.current_transaction = []

		self.new_block(100,1)
		
	def new_block(self,proof,previous_hash=None):
		block = {
			 "index":len(self.chain) + 1,
			 "timestamp":time(),
			 "transactions":self.current_transaction,
			 "proof":proof,
			 "previous_hash":previous_hash
			 }
		self.current_trasaction = []
		self.chain.append(block)
		return block

	def new_transaction(self,sender,recipient,amount):
		
		self.current_transaction.append({
			"sender":sender,
			"recipient":recipient,
			"amount":amount
			})

		return self.last_block["index"] + 1

	def hash(self,block):
		block_string = json.dumps(block,sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()
	
	@property
	def last_block(self):
		return self.chain[-1]

	def valid_proof(self,proof,last_proof):
		guess = f"{last_proof}{proof}".encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == "0000"
	
	def proof_of_work(self,last_proof):
		proof = 0
		while not self.valid_proof(last_proof,proof):
			proof += 1

		return proof
