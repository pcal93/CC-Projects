pip3 install -r agent/requirements.txt

docker build -t dummy ./dummy_container

docker run -d dummy
docker run -d dummy
docker run -d dummy


python3 agent/main.py