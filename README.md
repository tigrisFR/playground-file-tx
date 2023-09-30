# playground-file-tx

This is a pet project.</br>
**I strongly advise against using this for anything else than prototyping/tinkering.**</br>
It is a lightweight backend to test upload/download files.

As of now, everything is stored on the host environment disk.
It uses:
  - Python3 + Flask
  - SQL db for storing files metadata, Users and Invite Codes
  - disk for file storage
  - JWT for auth

## Setup and run
I have it working on AWS Cloud9 via ngrok tunneling (Cloud9 only does http and Ngrok allows us to tunnel HTTPS requests from clients)

You'll need to setup your python3 env:
```
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
deactivate
```
Then configure ngrok:
- create a ngrok free account and copy your auth token. At time of writing they also give you one domain for free: this allows you to tunnel with a stable URL instead of getting a new random one everytime you reconnect your ngrok agent.
- install ngrok on your host, for instance via `npm install -g ngrok`
- configure ngrok via `ngrok config add-authtoken <my_ngrok_auth_token>`

Then you're all set to start tunneling and run your app:
- start tunneling on one of the allowed ports (I think Cloud9 listens on: `8080`, `8081`, and `8082` by default), for instance:</br>
`ngrok http --domain=curious-manatee-guiding.ngrok-free.app 8080`</br>
or if you don't have a stable domain:</br>
`ngrok http 8080`
- confirm your app is setup to run on the same port in your *run.py*: `app.run(host='0.0.0.0', port=8080, debug=True)`
- start your back-end app via `python run.py` (don't forget to `source myenv/bin/activate` and `deactivate` your venv before and after)

Then you'll be able to have clients make request to your back-end via the HTTPS endpoint exposed by your ngrok tunnel, **but don't forget to update the list of allowed origins in your *__init__.py*:** `CORS(app, resources={r"/*": {"origins": allowed_origins}})`

## Additional considerations:

For the authentication via JWT bearer token to work, scripts assume a `JWT_SECRET_KEY=df6d8g...` (no need for quotes) is provided in an python .env file in the project root directory.
Similarily for generating invite codes, the local commands provided by *local_utils_invite_codes.py* assume that a `INVITATION_MASTER_KEY` is provided in the same .env file.
The commands in local_utils_invite_codes.py allow to locally generate and retrieve invitation codes stored in the app's DB.
