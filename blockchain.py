#! /usr/bin/env python3
import json 
import hashlib
from time import time
from urllib.parse import urlparse
import requests

class Blockchain:
	
	def __init__(self):
		self.chain = []
		self.current_transaction = []
		self.nodes = set()
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

	def register_nodes(self,address):
		parsed_url = urlparse(address)
		self.nodes.add(parsed_url.netloc)
	
	# So a conflict is when two nodes have different blockchains
	# The longest chain among the two node will be considered rest blocks will be orphaned
	def valid_chain(self,chain):
		previous_block = chain[0]
		index = 1

		while index < len(chain):
			block = chain[index]

			if block["previous_hash"] != self.hash(previous_block):
				return False

			if not self.valid_proof(block["proof"],previous_block["proof"]):
				return False

			previous_block = block
			index += 1
		
		return True

	
	def resolve_conflicts(self):
		neighbours = self.nodes
		new_chain = None

		max_len = len(self.chain)
       
		for node in neighbours:
			response = requests.get(f'http://{node}/chain')
			print(response.status_code)
			if response.status_code == 200:
				print("run")
				length = response.json()['length']
				chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
				if length > max_len and self.valid_chain(chain):
					max_len = length
					new_chain = chain
		
		if new_chain:
			print(new_chain)
			self.chain = new_chain
			return True

		return False


