# kingfisher

# Getting Started  
1. Build Kingfisher image:  
```
docker build .
```
  
2. Pass imageID into docker-compose-template.sh and clean.sh  
3. Declare targets in docker-compose-template.sh   

4. Generate docker-compose.yaml  
```
docker-compose-template.sh
```
  
5. Launch merchants:  
```
docker-compose up -d
```
  
6. Clean up:  
```
sh clean.sh
```
