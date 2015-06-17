Install docker

Run docker
boot2docker start

(Don't forget to set the environment variables as outputed by boot2docker start)

clone the repository from https://github.com/KlubJagiellonski/Politikon

Go to the folder 

Run docker_rebuild.sh
 
Run docker_run.sh

Enter docker:
ssh root@$(boot2docker ip) -p 2233
Password: pass