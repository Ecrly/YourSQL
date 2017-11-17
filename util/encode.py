import json
import base64


def _encode(data):
    data = json.dumps(data)
    data = data.encode()
    return base64.b64encode(data)


def _decode(data):
    data = base64.b64decode(data)
    data = data.decode()
    return json.loads(data)

data ={
    'name': 'chen',
    'age': 12,
}

data = _encode(data)