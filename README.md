# kingfisher

Getting Started  
Build Kingfisher image:  
```
docker build .
```
  
Pass imageID into docker-compose-template.sh and clean.sh  
Declare targets in docker-compose-template.sh   

Generate docker-compose.yaml  
```
docker-compose-template.sh
```
  
Launch merchants:  
```
docker-compose up -d
```
  
Clean up:  
```
sh clean.sh
```
