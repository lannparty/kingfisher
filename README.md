# kingfisher
Unapologetically naive algorithm to lose money for you through interactive brokers by trying to buy low and sell high on stocks with desired spread.  
If you're lucky you could make upwards of negative thirty dollars a day, and if you're unlucky there really is no limit to how much money you can lose, it's infinitely scalable one direction!  

  
Why this doesn't work: Read Flash Boys: Michael Lewis (2014)
# Overview  
State machine pattern, the merchant is emotional and has stamina.  
![image](https://user-images.githubusercontent.com/17228005/128608847-ce55c1ab-9162-40f0-9bab-43fe320fab13.png)


# Getting Started  
1. Build Kingfisher image:  
```
docker build .
```
  
2. Pass imageID into multi.sh and clean.sh  
3. Declare targets in multi.sh   

5. Launch merchants:  
```
sh multi.sh
```
  
6. Clean up:  
```
sh clean.sh
```
crontab
```
* 7 * * mon-fri
* 13 * * mon-fri
```
