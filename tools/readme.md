some little tools


build anwen-api-doc:
python restdown ../docs/anwen-api.md  -b ./anwen-api

local-markdown-editor:
chromium-browser edit.html

build cookie_secret
base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
