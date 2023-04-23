

 **Installing jenkins**

    docker run  -d -p 8080:8080 -p 50000:50000 -v /Users/snarasimhan/var2:/var/jenkins_home --name jenkins1 jenkins/jenkins:lts
	docker run -it -d -p 8080:8080 -p 50000:50000 -p 22220:22 -v /Users/snarasimhan/var2:/var/jenkins_home --name jenkins1 newjenkins
	docker run -it -d -p 8081:8080 -p 50001:50000 -p 22221:22 -v /Users/snarasimhan/var3:/var/jenkins_home --name jenkins2 newjenkins
	

 **Install neo4j**

 **Install mongo**

 **Install couchbase**
	
	

 **Get image id**

	docker images -a 

 **To stop an docker container**
	docker stop jenkins1

 **To remove a container**

	docker rm jenkins1
	
 **To remove docker image**

	docker rmi {image_id}
	
	
 **Build jenkins image**

	docker build -t newjenkins .

	
 **exec shell and copy ssh public key**

	docker exec -it jenkins2 /bin/bash

 **get running ip**

	 docker inspect <containerNameOrId>

	 https://devhints.io/docker

 **ssh into docker container**
 docker exec –it {imagename} /bin/bash