user=chromamaster
repository=tranvia_zaragoza_bot
tag=latest
docker build --no-cache -t ${user}/${repository}:${tag} .
