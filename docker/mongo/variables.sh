#loosely used names to identify containers 
#and images we want to operate on
app_name1="mongo"
app_name2="mongodb"

#docker mongodb credentials
user_id=admin
passwd_str=admin
auth_db_name=admin

#docker mongo database and collection names
db_name=pipeline

#docker mongodb hostname
hostname=localhost:27017

#docker mongodb import file . TODO - make a loop to go through the list 
#setup-collections.sh

src_file1=./mongo-seed/patients.json
collection1_name=patientsFHIR
src_file2=./mongo-seed/otm.json
collection2_name=onTrakMember
src_file3=
collection3_name=

#max threads for import. anything more than 50 fails. 
num_workers=50 