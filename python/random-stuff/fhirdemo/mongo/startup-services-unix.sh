docker-compose -f services/unix/docker-compose-mongo.yml -p unix_mongo up --build -d mongodb
docker-compose -f services/unix/docker-compose-sftp.yml -p unix_sftp up -d
