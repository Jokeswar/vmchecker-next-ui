# VMChecker Next UI

## Requirements

```
apt-get update -yqq
apt-get install -yqq python3-pip

pip3 install pipenv
```

## Run a deployment stack (backend included)

1. Copy `etc/.env.compose-full` to the root folder as `.env`
2. Replace the variables inside with the correct values
3. Deploy using docker compose and the `etc/compose-full.yml` configuration

```
pipenv run docker compose -f etc/compose-full.yml -p ui up
```

## Run a development stack

Run:
```
pipenv run {docker-compose-dev|docker-compose-prod} up
```

If you have an existing vmck backend point the `VMCK_BACKEND_URL` variable in the correspoding development or production environment file found in `./etc` to the correct URL.
If not follow this [quick setup](https://github.com/systems-cs-pub-ro/vmchecker-next-api).

To create a dummy assignment and an admin account (user: admin, password: admin) run:
```
pipenv run docker-compose-fill-data
```

To properly set up the assignment:
1. Go to `http://localhost:7000/admin`.
2. Login with the admin account
3. Select the `Assignemnts` tab on the left side
4. Click on `ShortName`
5. Update the gitlab [private token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#create-a-personal-access-token) and the [project id](https://github.com/systems-cs-pub-ro/vmchecker-next/wiki/Teaching-Assistant-Handbook#23-find-the-project-id).
