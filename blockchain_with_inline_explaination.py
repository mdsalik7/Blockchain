#Creating a Blockchain On Python Using Web Application Framework, Flask And Testing It On Postman

'''
What is a Web Application Framework?
A web framework or web application framework is a software framework that is designed to support the 
development of web applications including web services, web resources, and web APIs. Web frameworks provide a
standard way to build and deploy web applications.

Reason for using a Web Application Framework for a Blockchain is because we want to build a blockchain that 
can be used by anyone online using some servers.

Web Application Framework I ll be using - Flask 0.12.2

What is a Postman?
Postman is a powerful HTTP client for testing web services. Postman makes it easy to test, develop and 
document APIs by allowing users to quickly put together both simple and complex HTTP requests.

#To Be Installed -
Flask -  pip install Flask==0.12.2
Postman - https://www.getpostman.com/
'''

#Getting Started

#Importing the libraries

import datetime   
#Because each block ll have its own timestamp (the exact date and time the block was created or mined)
import hashlib  #For hashing the blocks
import json  
#For converting Python Object to JSON Strings, Will use the dump function. 
#For more in details refer to https://www.w3schools.com/python/python_json.asp
from flask import Flask, jsonify 
'''From flask lbrary, importing the flask class because to create an object of flask class which ll be the
web application itself. Jsonify is a function use to return the messages to the Postman when ll interact with
the blockchain'''

#Part I - Building a blockchain -  Architecture

class Blockchain:
    def __init__(self):
        self.chain=[]                                 #Initlization of blockchain With an empty list
        self.create_block(proof=1, previous_hash='0') 
        '''.create_block is a future function that i ll make, which ll create and also append the block to the
        blockchain after solving proof of work, Creating the Genesis Block with two arguments, previous_hash
        is in string because we ll use SHA256 lib which only uses encoded string'''
    
    def create_block(self,proof,previous_hash):       
        '''create_block function contains a dictionary with the following keys of the block to be mined,
        This function ll also be used to verify the proof of work, Dictionaries associate values with keys so
        you can look them up efficiently (by key) later on.'''
        block={'index':len(self.chain)+1, 
#Index is the new block mined or addded to the blockchain-[(self.chain) is the blockchain itself, (+1) is the new block added now]
               'timestamp':str(datetime.datetime.now()), 
               #datetimestamp is in string format so that we dont encounter any format issues working with the json format. 
               'proof':proof,         #Proof of work & Previous hash argument ll be defined later.
               'previous_hash':previous_hash,               
               }
        self.chain.append(block)                #Appending/Adding the new block to the blockchain
        return block                            #Returning the block to display the informations i.e keys on the POSTMAN.
    
    def get_previous_block(self):               #get_previous_block function ll return or get the last block of the blockchain at anytime.
        return self.chain[-1]                   #Index [-1] refers to the last element of the list self.chain[]
        
    def proof_of_work(self,previous_proof):     
        '''Proof of work function having cryptographic SHA256 puzzle/problem where the miners need to solve it
        to get the block append to the blockchain successfully. It ll have two arguments, one is (self) because
        we ll apply the proof of work method from the instance object that will be created from the class and 
        the other (previous_proof) is another element of the problem that the miners ll encounter to find the 
        new proof'''
        new_proof=1                             
        '''new_proof is a variable that is initialized to 1 because to solve the problem we are going to 
        increament this new proof variable by one at each iteration of a while loop until we get the right 
        proof. Basically we are here trying to solve the problem by hit and trial method''' 
        check_proof=False                       
        '''Check_proof is a variable that ll check the new proof is the right proof or not.
        Its the Condition for the while loop. check_proof=false means its not the right proof'''
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest() 
            '''hash_operation is a variable of a string of 64 characters which uses sha256 function from the
            hashlib library for the cryptographic problem defined (Operation) and is encoded in bytestring
            format and converted into hexadecimal number.
            https://medium.com/@dwernychukjosh/sha256-encryption-with-python-bf216db497f9
            Operation can be anything but the only condition is that it cant be symmetrical,
            it can only be unsymmetrical because when the operation is symmetrical
            i.e. new_proof+previous_proof=previous_proof+new_proof (a+b=b+a condition for symmetricity) 
            and in symmetricity when we increament the new proof at some point the new proof
            ll be a old previous proof.'''
            if hash_operation[:4]=='0000':      
                '''SLicing the hash_operation to check first four nos. are zeros, 
                More the leading zeros we put more harder to find the golden nonce.'''
                check_proof=True
            else:
                new_proof +=1       #x += y statement is just a shorthand for x = x + y in python. [condition to re run the loop]
        return new_proof
              
    def hash(self,block):                                         
#Its a hash function that ll hash each block. Hash function ll be needed by the POW function and previous function that we ll define next.
        encoded_block=json.dumps(block,sort_keys=True).encode()   
        '''encoded_block is a variable which ll convert the block dictionary having the four keys to Json format
        i.e. object to a string. We use json dumps instead of direct string method because in Part 2 we ll put 
        the block dictionary into a json file, therefore the blocks originally ll have a JSON format'''
        return hashlib.sha256(encoded_block).hexdigest()      #Returning the cryptographic hash of the encoded block.
    
    def is_chain_valid(self,chain):     
        '''Its a function that ll check each block has correct proof of work i.e proof of the problem that
        we defined is correct with the four leading zeros for each block and the previous_hash of the block
        is equal to hash of the previous block, One of the arguments is chain because the checks ll be 
        performed on each blocks of the chain.'''
        previous_block=chain[0]         
        '''previous_block is a variable that is initiazed to chain[0] i.e. the 1st block of the blockchain.
        We ll start a while loop because we are going to itterate on all the blocks of the chain.
        At the end of the while loop we ll update the value of the previous_block variable to the new block.'''
        block_index=1  
        #block_index is a looping variable representing block number for each block. It has been intialized to the first block. 
        while block_index<len(chain):   
            '''block_index<len(chain) indicates the last block of the chain, This condition wont stop the 
            loop until block index has reached the final index of the chain. At the end of the while loop 
            ll increament block index by 1 until it reaches the final index given by the length of the chain.'''
           
            #1ST CHECK - previous hash of the current block is the hash of the previous block
            
            block=chain[block_index]    #current block that to be checked
            if block['previous_hash']!=self.hash(previous_block):  
                '''This condition is for invalid blocks which means Hash of the current created block
                (stored as a key, 'previous_hash' in the dictionary) is not equal to hash of the previous block
                (hash function that we defined to hash each block in the chain).
                We need to take self because hash is a method of our blockchain class.'''
                return False                      #If the above condition meets we have to return False because the block is invalid.
            
            #2ND CHECK - Proof of each block is valid
            
            previous_proof=previous_block['proof']  #Taking previous_proof of the previous block by the key proof from the dictionary. 
            proof=block['proof']              #Taking Proof of the current block [block=chain[block_index] is the current block]
            hash_operation=hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest() 
            '''Computing the hash operation of the previous block and proof of the current block and 
            checking if this hash operation starts with four leading zeros, this ll indicate wether the
            proof of the current block is valid or not.'''
            if hash_operation[:4]!='0000':              #If the hash operation doesnt have the four leading block it ll return False.
                return False
            previous_block = block 
#Updating previous_block so it becomes current block because at the next iiteration of loop, current block ll become the next block of chain.
            block_index +=1        #Updating the loop variable.
        return True                #Returning True if everything goes right.

#Part II - Mining the Blockchain
#Creating a Web App
app = Flask(__name__)    #To Create Web App, Follow Flask Quickstart for in depth details.
    
#Creating a Blockchain
blockchain=Blockchain() #Creating blockchain object for the Blockchain class.

#Mining a new block - 1st GET Request
@app.route('/mine_block',methods=['GET']) 
#the route() decorator to tell Flask what URL should trigger our function, Follow Flask Quickstart for details. 
#For GET method argument follow 'HTTP Methods' from the quickstart.
def mine_block():       
    '''mine_block function mines a block by solving proof of work problem by finding the proof based on the 
    previous proof i.e. the last proof given on the last block. Getting this proof means success in mining 
    the block. Once the proof is achieved, we ll get the other keys required to create a block 
    i.e index, timestamp, proof, previous_hash.
    In order to to get the proof we apply proof_of_work function and in order to apply
    proof_of_work function we need previous proof, to get previous_proof we have get_previous_block function
    with applying the proof key of dictionary.'''
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block) 
    '''To add a block to the blockchain we have a function create_block which not only create just but also 
    append it to the blockchain, to call create_block function we need previous_hash argument, 
    to get previous_hash argument we uses hash function to the previous hash of the blockchain.'''
    block=blockchain.create_block(proof,previous_hash) #Since create_block is a method so we need to call it from blockchain object.
    '''Its a variable which ll contain the information of the block and as well as a message. We are going
    to return the response in json format, so we are making the response a dictionary so we ll include the keys
    of the block we just mined and a new key as congratulation message.'''
    response={'message':'Congrats, You just mined a block',
              'index':block['index'],
              'timestamp':block['timestamp'],
              'proof':block['proof'],
              'previous_hash':block['previous_hash']}
    return jsonify(response), 200 
'''We are also returning HTTP Status code for success meaning everything was fine i.e. the block was mined 
and successfully added to the chain and there was no error so we are good to display- 
https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200'''

#Getting the full Blockchain - 2nd GET Request
@app.route('/get_chain',methods=['GET'])
def get_chain(): #get_chain is a function that ll get the whole blockchain so the below responses can be performed or achieved.
    response={'chain':blockchain.chain, 
#From the blockchain object we ll get the chain attribute that is the chain variable. This ll get the whole blockchain to display. 
              'length':len(blockchain.chain)
              }
    '''As new blocks ll be mined and the chain ll be populated with new blocks so to calculate the 
    length of the chain we ll use the len to get the total number of blocks in the blockchain 
    i.e. length of the blockchain.'''
              
    return jsonify(response), 200
 
#Running the app
app.run(host='0.0.0.0', port=5000)
