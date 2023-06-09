# NiftyBridge AI assistant

FastAPI service that answers questions about the contents of a [PDF file](https://www.dropbox.com/s/9npstuvp2vhnq4z/Untitled%205.pdf?dl=0)

Maximum message length must not exceed 4096

## Installation

Python3 must be already installed


```shell
git clone https://github.com/hikehikehike/Nifty
cd Nifty
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
#### Rename file ".env.sample" to ".env"
#### In file ".env" add your [OPENAI_API_KEY](https://platform.openai.com/account/api-keys)
```shell
uvicorn main:app --reload
```
Go to the link http://127.0.0.1:8000/

----------
## Installation from Docker
Install and run [Docker](https://www.docker.com/) on your machine
```shell
git clone https://github.com/hikehikehike/Nifty
cd Nifty
```
#### Rename file ".env.sample" to ".env"
#### In file ".env" add your [OPENAI_API_KEY](https://platform.openai.com/account/api-keys)
```shell
docker build -t nifty .
docker run -p 8000:8000 nifty
```

Go to the link http://127.0.0.1:8000/
