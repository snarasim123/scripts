	FROM jenkins/jenkins:lts
	# if we want to install via apt
	USER root
	RUN apt-get update && apt-get install -y vim make git ssh 
	RUN apt-get install --assume-yes openssh-server default-jre python3
	USER jenkins
	CMD ssh-keygen -t rsa -f ~/.ssh/id_rsa -q -P "" 
#		&& \
#		echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC5V/nsE3kKMrvQImlxExAi779mxrZd8s89T2qGRqDWsY9xjnRMYAYtwi/BF1+AJSY0qLTyPPDLfCMllwVIeyXN9Mo1au8cvvpw2VIk0QCx0MhPNjjfMILYuKHdqufDKbL9miboxXn2HtyCaNmeyTYcTZtcXgpMrv8XVeYJo3GOyw7VgW8DuWB+1nltpVCQoFXHetrHHFICuG+y5cFXmTadrEvcX7Ec2TPv6CKvexNIsJyHJlNHBO6lb5CRZMLCQgA7px6Gx2mcRV8cMnChfVl9detWWv5X3NXcJyE2DIh6hErZFyHu/MfhAFKBYRb+nruk6pJfcIOmB7+ZGTjVBYqZ jenkins@665f8eac78b2" > ~/.ssh/authorized_keys && \
#		chmod 700 ~/.ssh/authorized_keys 


