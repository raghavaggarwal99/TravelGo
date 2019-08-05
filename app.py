#!flask/bin/python
from flask import Flask, request, jsonify, logging
import json
import pymysql
import requests
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    v=request.args.get('query')
    chatid=request.args.get('passed')
    # val=jsonify(v)
    # val.headers['Access-Control-Allow-Origin']='*'
    query=str(v)
    unique_session_id=(str(chatid))
    print("below chatid")
    accessToken = "67a51d361a694109876d9b0c5639dc3e"
    base ="https://api.dialogflow.com/v1/"
   
    URL="https://console.dialogflow.com/api-client/demo/embedded/81bdd9b9-5aab-4720-b677-7981c517f194/demoQuery?q="+ query+ "&sessionId=3332218f-c750-1e76-7b0d-ebdf99e40836"

    headers = {'Content-Type': 'application/json',  
           'Authorization': 'Bearer' + accessToken,
           'dataType': 'json'
           }

    r = requests.get(url = URL, headers=headers)
    # print (r.json())
    p=r.json()
    result=(p.get("result"))
    fulfillent=result.get("fulfillment")
    response=  (fulfillent.get("speech"))
    print (response)

    date=datetime.datetime.now()

    check=response[0:7]

    conn = pymysql.connect(host='localhost',
                        database='buses',
                        user='root',
                        password='')
    cursor = conn.cursor()
 
    
    if(check.find("rag")!=-1):
        response_copy=response
        copy=response.split()

        cursor.execute("SELECT * FROM buses_schedule")
        x= cursor.execute("SELECT * FROM buses_schedule WHERE original=%s and destination =%s", (copy[2], copy[3]))
        print("in check!")
        multiple_response=[]
        if(x>=1):
            rows = cursor.fetchall()
            v=0
            for row in rows:
                if(v==0):
                    multiple_response.append("These are the following buses available for this route")
                    # multiple_response.append("Original Destination Fares Types SeatsLeft Date Time")
                    v=1
                multiple_response.append("Buses available from "+ str(row[0])+ " going to " +str(row[2])+ " with fares " + str(row[3])+ " of type "  + str(row[4])+ " with seats "  + str(row[5])+ " "  + str(row[6])+ " and timings "  + str(row[7]))
        else:
            cursor.execute("SELECT * FROM path")
            b=cursor.execute("SELECT timings, bus_id FROM path WHERE city1 = %s", copy[2])
            values=cursor.fetchall()

            a=cursor.execute("SELECT bus_id FROM path WHERE city2 =%s", copy[3])
            yes=-1
            index=-1
            ids=cursor.fetchall()
            for i in range(0,a):
                for j in range(0,b):
                    if(ids[i][0]==values[j][1]):
                        yes=1
                        index=j
                        multiple_response.append("The bus is available from dehradun to noida at timings "+ str(values[index][0]) +"and the bus id is"+ str(values[index][1])+ "The fare information is not threre!")

            if(yes!=1):
                multiple_response.append("Sorry there are no buses avaialble for this route. Maybe you can try checking it on the website")    

        traverse=0
        while traverse <len(multiple_response):
            result=cursor.execute("INSERT INTO history(Sessionid, input, output) VALUES(%s, %s,%s)", (unique_session_id,query,multiple_response[traverse]))    
            traverse+=1
        conn.commit()

        multiple_response=jsonify(multiple_response)
        multiple_response.headers['Access-Control-Allow-Origin']='*'
        return (multiple_response)
    elif(check.find("dialo")!=-1):
        multiple_response=[]
        multiple_response.append("Here is all the information you can find for bus pass")
        multiple_response.append("http://utc.uk.gov.in/pages/display/3-monthly-pass-scheme")
        traverse=0
        while traverse <len(multiple_response):
            result=cursor.execute("INSERT INTO history(Sessionid, input, output) VALUES(%s, %s,%s)", (unique_session_id,query,multiple_response[traverse]))    
            traverse+=1
        conn.commit()
        multiple_response=jsonify(multiple_response)
        multiple_response.headers['Access-Control-Allow-Origin']='*'
        return (multiple_response)
    elif(check.find("regre")!=-1):
        multiple_response=[]
        multiple_response.append("You can book your bus here!")
        multiple_response.append("https://utconline.uk.gov.in/")
        print(multiple_response)
        traverse=0
        while traverse <len(multiple_response):
            result=cursor.execute("INSERT INTO history(Sessionid, input, output) VALUES(%s, %s,%s)", (unique_session_id,query,multiple_response[traverse]))    
            traverse+=1
        conn.commit()

        multiple_response=jsonify(multiple_response)
        multiple_response.headers['Access-Control-Allow-Origin']='*'
        return (multiple_response)
    elif(check.find("custom")!=-1):
        multiple_response=[]
        multiple_response.append("Here is the list of numbers You can call to.")
        multiple_response.append("http://utc.uk.gov.in/contactus")
        traverse=0
        while traverse <len(multiple_response):
            result=cursor.execute("INSERT INTO history(Sessionid, input, output) VALUES(%s, %s,%s)", (unique_session_id,query,multiple_response[traverse]))    
            traverse+=1
        conn.commit()
        multiple_response=jsonify(multiple_response)
        multiple_response.headers['Access-Control-Allow-Origin']='*'
        return (multiple_response)
    else:
        array=[]
        array.append(response)
        val=jsonify(array)
        val.headers['Access-Control-Allow-Origin']='*'
        for traverse in array:
            result=cursor.execute("INSERT INTO history(Sessionid, input, output) VALUES(%s, %s,%s)", (unique_session_id,query,traverse))    
        conn.commit()
        print(val)
        return (val)


if __name__ == '__main__':
    app.run(debug=True)