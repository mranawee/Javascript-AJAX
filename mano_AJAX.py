#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Mano Ranaweera
#Group: Italo Duran


#Query the miRNA database through the browser using a cgi program

import pymysql
import cgi
import cgitb
#next is for packaging the output into json format
import json

#the next line is useful for debugging
#it causes errors during execution to be sent back to the browser
cgitb.enable()


#this program does NOT generate html
#instead, it queries the miRNA database and returns the results
#to be formatted by the calling AJAX function



query1 = """
        select score
        from targets join miRNA using(mid)
        where name = %s
        """
          
query2 = """
        select name, seq
        from miRNA
        where seq regexp %s
        """

#retrieve input data from the web server
form = cgi.FieldStorage() 

#next line is always required as first part of http output
print("Content-type: text/html\n")


if (form):
   
    try:
        connection = pymysql.connect(
            host='bioed.bu.edu', 
            user='mranawee',
            password='Megaspyguy4', 
            db='miRNA',
            port = 4253) 
    except pymysql.Error as e: 
         print(e)
    
    # get cursor
    cursor = connection.cursor()

         
    selector = form.getvalue("selector","")
       
   
    
    if (selector == "hist"):
         miRNA = form.getvalue("miRNA","")
         if(miRNA!=""):
         
             try:
                 cursor.execute(query1, [miRNA])
             except pymysql.Error as e:
                 print(e)
                 
             results=cursor.fetchall() 
             print(json.dumps(results))  
            
    if (selector == "RNAseq_table"):          
        seq = form.getvalue("input_seq","")
        if(seq!=""):
        
            try:
                cursor.execute(query2, [seq])
            except pymysql.Error as e:
                print(e)
                    
            results=cursor.fetchall() 
            print(json.dumps(results)) 
        
                
        
        
    
        
            
            
   



