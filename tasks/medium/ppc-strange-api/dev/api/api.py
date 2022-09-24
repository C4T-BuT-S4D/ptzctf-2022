from flask import Flask, request, abort
from flasgger import Swagger, swag_from
import os

flag = os.getenv("FLAG")
if flag == None:
  raise "No flag found"

app = Flask(__name__)
app.config["SWAGGER"] = {
  "title": "Flag API",
  "specs_route": "/"
}
swagger = Swagger(app)

random_route = os.urandom(20).hex()
random_key = os.urandom(20).hex()

@app.post(f"/api/{random_route}")
@swag_from({
  "parameters": [
    {
    "name": "Secret-Key",
    "in": "header",
    "description": "Secret key which is required to access the endpoint.",
    "example": random_key
    }
  ],
  "responses": {
    "200": {
      "description": "The task's flag."
    }
  }
})
def flag_route():
  """Flag endpoint. Needs a secret key."""
  if request.headers.get("Secret-Key") != random_key:
    abort(401)
  return flag

if __name__ == '__main__':
  print([url for url in app.url_map.iter_rules()])
  app.run(host="0.0.0.0", port=int(os.getenv("PORT")))
