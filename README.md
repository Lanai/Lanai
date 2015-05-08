# Lanai
Lanai is a microframework for tcp server.

## How to use

```python
from lanai.app import Lanai
from lanai.server import LanaiServer
from lanai.protocol import Protocol

protocol = Protocol('hello-world')

@protocol.event
def on_hello(data):
    return dict(message='Hello World')
    
app = Lanai()
app.register_protocol(protocol)

server = LanaiServer(app, '0.0.0.0', 3000)
server.serve_forever()
```
