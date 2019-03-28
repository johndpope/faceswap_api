# API for the [faceswap.baraba.sh](https://faceswap.baraba.sh/) project

## Example

First photo:

![first photo](https://faceswap.baraba.sh/i/ExcitedlyScaryBombay.jpg)

Second photo:

![second photo](https://faceswap.baraba.sh/i/KnavishlyCruelTermite.jpg)

Result:

![result](https://faceswap.baraba.sh/i/WronglyLudicrousSomali.jpg)

## Run development build

```
(cd ./Docker/dev && sudo docker-compose up --build)
```

## Run tests

```
(cd ./Docker/dev/ && sudo docker-compose exec django pytest)
```

## Run production build

```
(cd ./Docker/prod && sudo docker-compose up --build)
```
