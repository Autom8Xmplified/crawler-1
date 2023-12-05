import re
from fastapi import FastAPI, Request, Response
import uvicorn
import os, time
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
from api import jotform


origins = [
   "*"
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=origins,  allow_headers=["*"])
]

app = FastAPI(middleware=middleware)

ALLOWED_ORIGINS = '*' 

class JotForm(BaseModel):
    url: str
    contact_person: str
    contact_number: str
    street: str
    email: str
    city:str
    loanNumber: str
    state: str
    zip: str
    inspectionDateTime: str
    InspectorName: str
    Summary: str

# handle CORS preflight requests
@app.options('/*')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

# set CORS headers
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response


@app.get('/main')
async def welcome():
	return "Welcome to API"
    
@app.post('/jotform-submit')
async def fillForm(form_data: JotForm):
    # Fetch Data
    url  = form_data.url
    contact_person = form_data.contact_person
    contact_number = form_data.contact_number
    street = form_data.street
    email  = form_data.email
    city = form_data.email
    loanNumber = form_data.loanNumber
    state = form_data.state
    zip = form_data.zip
    inspectionDateTime = form_data.inspectionDateTime
    InspectorName = form_data.InspectorName
    Summary  = form_data.Summary

    # Send Crawler to perform input on fields
    res = jotform.Fill_Form(url, contact_person, contact_number, street, email, city, loanNumber, state, zip, inspectionDateTime, InspectorName, Summary)
    if(res == "completed"):
        res = jotform.Submit()
        time.sleep(5)
        if(res == "submitted"):
            return "Data Submitted"
    else:
        return "Failed to Input Data"
	    
@app.post('/jotform-preview')
async def fillForm_preview(form_data: JotForm):
    # Fetch Data
    url  = form_data.url
    contact_person = form_data.contact_person
    contact_number = form_data.contact_number
    street = form_data.street
    email  = form_data.email
    city = form_data.email
    loanNumber = form_data.loanNumber
    state = form_data.state
    zip = form_data.zip
    inspectionDateTime = form_data.inspectionDateTime
    InspectorName = form_data.InspectorName
    Summary  = form_data.Summary
    try:
        Summary = re.sub(r"(\<space>+)|(\Summary:+)", "\n", Summary)
    except Exception:
         pass

    # Send Crawler to perform input on fields
    res = jotform.Fill_Form(url, contact_person, contact_number, street, email, city, loanNumber, state, zip, inspectionDateTime, InspectorName, Summary)
    if(res == "completed"):
        res = jotform.Preview()
        time.sleep(5)
        if(res == "completed"):
            return "Data Previewed"
    else:
        return "Failed to Input Data"
	    
if __name__ == "__main__":
	uvicorn.run(app, host='0.0.0.0', port=os.environ.get('PORT', '5000'))
