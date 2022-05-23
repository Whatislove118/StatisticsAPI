# StatisticsAPI
## Run app
#### 1. Create and fill .env file according to .env.example
### 2. Build container
```shell
docker build -t statistics_api .
```
### 3. Run container
```shell
docker run -dp 8080:8080 --name statistics_api statistics_api
```
## SwaggerUI located at / path (http://localhost:8080)








