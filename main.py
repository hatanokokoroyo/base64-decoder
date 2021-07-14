import base64
import json
import os
import time

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware


class ParseParam(BaseModel):
    file_type: str
    base64: str


class ExtractParam(BaseModel):
    json_str: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # 允许进行跨域请求的来源列表，*作为通配符
    allow_credentials=True,  # 跨域请求支持cookie，默认为否
    allow_methods=['*'],  # 允许跨域请求的HTTP方法
    allow_headers=['*'],  # 允许跨域请求的HTTP头列表
)


@app.get('/', response_class=FileResponse)
def read_root():
    return FileResponse('./static/index.html')


@app.post('/parse/', response_class=FileResponse)
def parse(param: ParseParam):
    data = base64.b64decode(param.base64)
    file_type = param.file_type
    timestamp = str(int(time.time()))
    if not os.path.exists('./files'):
        os.makedirs('./files')
    file_name = timestamp + '.' + file_type
    file_path = './files/' + file_name
    with open(file_path, 'wb') as w:
        w.write(data)
    return FileResponse(file_path, filename=file_name)


@app.post('/extract/')
def find_base64_from_json(param: ExtractParam) -> list:
    data = json.loads(param.json_str)
    base64_list = find_base64_from_json_element('/', data)
    return base64_list


def find_base64_from_json_element(path: str, json_node) -> list:
    if str.endswith(path, '/'):
        path = path
    else:
        path = path + '/'
    base64_list = []
    if isinstance(json_node, dict):
        for key, value in json_node.items():
            base64_list.extend(find_base64_from_json_element(path + key, value))
    elif isinstance(json_node, list):
        cnt = 0
        for child_node in json_node:
            base64_list.extend(find_base64_from_json_element(path + '[' + str(cnt) + ']', child_node))
            cnt += 1
    elif isinstance(json_node, str):
        if len(json_node) > 100:
            base64_list.append((path, json_node))
    else:
        pass
    return base64_list


def read_file_lines(path: str):
    with open(path, 'r', encoding='utf8') as r:
        return r.readlines()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
