# build 
docker build -t errorapp .

# run
docker run --env-file .env -p 8000:8000 errorapp
