#stop all running docker containers
docker kill $(docker ps -q)

#remove all exited & created docker containers
docker rm $(docker ps -a -f status=exited -f status=created -q)
