### Docker 
Learning Docker fundamentals for containerizing applications.

#### Setup
Install Docker Desktop from [here](https://www.docker.com/products/docker-desktop/)

#### Building the Image
Navigate to the lab folder and build the Docker image:

```
docker build -t mlops-docker-lab .
```

#### Running the Container
Run the container with port mapping:

```
docker run -p 8000:8000 mlops-docker-lab
```

Access the application at http://localhost:8000

#### Useful Commands:

View running containers:
```
docker ps
```

Stop the container:
```
docker stop <container_id>
```

Remove the image:
```
docker rmi mlops-docker-lab
```

#### Results
![DELETE request](results/DELETE%20request%20.jpg)
![GET request - after all changes](results/GET%20request%20-%20after%20all%20change.jpg)
![GET request](results/GET%20request.jpg)
![POST request](results/POST%20request.jpg)
![PUT request](results/PUT%20request.jpg)
![Docker build](results/docker%20build.jpg)
![Docker containers](results/docker%20containers.jpg)

