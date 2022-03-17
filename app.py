#! /usr/bin/env python3

from blockchain import Blockchain
from flask import Flask,jsonify,request
from uuid import uuid4

app = Flask(__name__)

blockchain = Blockchain()

node_identifier = str(uuid4()).replace('-', '')

@app.route("/mine",methods=["GET"])
def mine():
	last_block = blockchain.last_block,
	print(last_block[0])	
	last_proof = last_block[0]["proof"]
	

	proof = blockchain.proof_of_work(last_proof)

	blockchain.new_transaction(sender="0",recipient=node_identifier,amount=1.5)

	previous_hash = blockchain.hash(last_block)
	block = blockchain.new_block(proof,previous_hash)

	response = {
			"message":"New Block Mined",
			"index":block["index"],
			"transaction":block["transactions"],
			"proof":block['proof'],
			"previous_hash":previous_hash
			}
	
	return (jsonify(response))

@app.route("/transactions/new",methods=["POST"])
def new_transaction():
	values = request.get_json()
	required = ["sender","recipient","amount"]

	if not all(k in values.keys() for k in required):
		return "Missing key values",400
	
	# returns the index of the new transaction
	index = blockchain.new_transaction(values["sender"],values["recipient"],values["amount"])
	
	response = {"message":f"Transaction added in block at {index}"}
	return jsonify(response),201

@app.route("/chain",methods=["GET"])
def get_chain():
	response = {
			"chain":blockchain.chain,
			"length":len(blockchain.chain)
	}
	return jsonify(response),200


if __name__ == "__main__":
	app.run(debug=True)
