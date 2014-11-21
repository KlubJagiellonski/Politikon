docker build -t politikon . && docker rm politikon_instance && docker run -it -v `pwd`:/app -p 2233:22 -p 8000:8000 --name politikon_instance politikon
