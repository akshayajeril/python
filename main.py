import json
from time import sleep
from tokenize import String
from typing import Optional
from typing import List
from urllib import response
from fastapi import Header, APIRouter, FastAPI, Form, File, Request
from pydantic import BaseModel, AnyHttpUrl
import requests
import threading
from typing import Union
from starlette import status
from starlette.responses import Response

from pydantic import BaseModel, HttpUrl
app = FastAPI(servers=[{"url":"http://localhost:7788"}])

class translated_res(BaseModel):
    output: str
    runtimeException: str
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

callback_router = APIRouter()
@callback_router.post(
    "{$request.header.callbackUrl}"
)
def call_callback(callbackUrl:str, output:translated_res):
    print("Starting timer 10 sec")
    sleep(10)
    print("Timer 10 sec ended")
    get_inp_url = callbackUrl
    print(get_inp_url)
    inp_post_response = requests.post(
        url=get_inp_url,
        headers={
            "accept": "application/json"
        },
        json={
            "output": "This is from callback: " + output.output,
            "runtimeException": output.runtimeException
        },
        verify=False
    )
    print("WO Status Code: "+ str(inp_post_response.status_code))

@app.post("/requestTranslateCallbackDemo", callbacks=callback_router.routes)
async def requestTranslateCallbackDemo(request: Request, inputString: str, callbackUrl: Union[str, None] = Header(default=None)):
    request_example = translated_res(output=inputString, runtimeException="123")
    thr = threading.Thread(target=call_callback, args=[callbackUrl, request_example])
    thr.start()
    return 200, {"Value entered":inputString}