# CONTRIBUTING

## How to run the Dcoerfile locally
```
docker build -t flask-smorest-api . 
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api sh -c "flask run --host 0.0.0.0"
```