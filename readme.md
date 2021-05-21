# base environment works for some odd reason.

docker build -t material-api .

https://softwarejargon.com/dockerizing-python-flask-app-and-conda-environment/

# ---------- MATERIAL-API IMAGE

sudo docker build -t material-api .
docker tun -it -p 5000:5000 material-api
