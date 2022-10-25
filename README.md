# VMChecker Next UI

## Run a development stack

Run:
```
pipenv run {docker-compose-dev|docker-compose-prod} up
```

If you have an existing vmck backend point the `VMCK_BACKEND_URL` variable in the correspoding development or production environment file found in `./etc` to the correct URL.
If not follow this [quick setup](https://github.com/systems-cs-pub-ro/vmchecker-next-api).
