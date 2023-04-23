docker-compose -f services/win/docker-compose-mongo.yml -p win_mongo up --build -d mongodb
docker-compose -f services/win/docker-compose-sftp.yml -p win_sftp up -d