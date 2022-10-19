from flask import Flask
from flask import request
import requests
import json
import threading
from datetime import datetime
# initilize Flask class

from asgiref.wsgi import WsgiToAsgi
myapp = Flask(__name__)


asgi_app = WsgiToAsgi(myapp)

# get from env variable
access_token = "sk_45254697f8d0a5fb1b9171cd7ed090fe"
base_url = "company.clearbit.com/v2/companies"


@myapp.route("/")
def main():
    """
    this is home url of our app..
    """

    return  "i m here..."



def _call_clearbit(user_request, request_id):
    """
    call the vendor api
    """

    find_url = f"https://{base_url}/find?domain={user_request['domain']}" 
    print (find_url)
    
    response = requests.get(find_url, headers={'Authorization': f'Bearer {access_token}'})
    code = response.status_code
    print ("reponse code", code)
    current_year = datetime.today().year
    if code == 200:
        response =json.loads(response.text)
        data = {"age": current_year-response["foundedYear"],"employees": response["metrics"]["employees"]}
        print (data)
        # format the data as the business need or age of the company & number of employees
        # dump response to DB keeping request_id as unique key..


@myapp.route("/fetch", methods=["POST"])
def fetch():

    # get POST form data 

    if request.method == "POST":
        user_request = json.loads(request.data)

        # call clearbit API 
        request_id = 12 # dynamic...
        x = threading.Thread(target=_call_clearbit, args=(user_request, request_id,))
        x.start()
        
    
    return json.dumps({"requestid": request_id})


@myapp.route("/health", )
def health():

    # get POST form data 
    return "i m awake...."

@myapp.route("/data/<request_id>")
def getuser_data(request_id=None):

    # get data from db/no sql for this request_id and return to user

    # if request.method == "POST":
    #     user_request = json.loads(request.data)
    #     print ("data recived......")
    return "done."


if __name__ == "__main__":

    myapp.run(debug=True)
