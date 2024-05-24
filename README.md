# Video & Audio Compressor App
This system compresses video & audio files submitted by a user

Check here: [FULL COURSE](https://youtu.be/siqDdrZI4x4?si=LA6zA9Yj4pn2EJJg) 

# Tools & Services:
- Django & DRF : for building the APIs
- Docker & Docker compose: Containerization
- Celery: For running background task asynchronously(e.g. video&audio compression)
- Rabbit MQ: A message broker for celery
- Flower dashboard: For monitoring celery background tasks
- PosgreSQL: Relational DB
- File Storage: AWS S3 Bucket
- VueJs: Frontend

# Running locally

Create a .env file by copying the .env.sample provided and run:

```
docker compose -f docker-compose.yml up --build
```
to build and run the container using the yaml file.

Access docs:
```sh
http://localhost:8000/api/v1/doc
```
## Frontend

![Frontend](frontend.png)

## API

![Frontend](api-pic.png)


## Flower

![Frontend](flower.png)
