from pymongo import MongoClient
import argparse

client = MongoClient("mongodb://localhost:27017")

db = client.Sumip

def insert_contact(fname,lname,email,msg):
    db.contact.insert_one({'first name':fname,
                            'last name':lname,
                            'email':email,
                            'message':msg})

args = argparse.ArgumentParser()

args.add_argument('-m','--mode',dest="mode",required=True,help="Database operation")
args.add_argument('--fname',dest="fname",help="Database operation")
args.add_argument('--lname',dest="lname",help="Database operation")
args.add_argument('--email',dest="email",help="Database operation")
args.add_argument('--msg',dest="msg",help="Database operation")
opts = args.parse_args()
mode = opts.mode

if(mode == "insert-contact"):
    insert_contact(opts.fname,opts.lname,opts.email,opts.msg)