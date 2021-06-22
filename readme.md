# base environment works for some odd reason.

docker build -t material-api .

https://softwarejargon.com/dockerizing-python-flask-app-and-conda-environment/

# ---------- MATERIAL-API IMAGE

sudo docker build -t material-twint .
docker run -it -p 8101:8101 material-twint
