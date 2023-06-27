# VMChecker Next UI

## Requirements

```
apt-get update -yqq
apt-get install -yqq python3-pip

pip3 install pipenv
```

## Run a deployment stack (backend included)

1. Replace the variables inside `etc/.env.compose-full` with the correct values
2. Deploy using docker compose and the `etc/compose-full.yml` configuration

```
docker compose -f etc/compose-full.yml --env-file etc/.env.compose-full -p ui up
```

# Enable LDAP authentication support

1. Inside `etc/.env.compose-full` uncomment the following variables `LDAP_SERVER_URI`, `LDAP_USER_TREE` and `LDAP_USER_FILTER`
2. Set their values appropriately:
    - `LDAP_SERVER_URI` - the LDAP server URI
    - `LDAP_USER_TREE` - the subtree where the users reside
    - `LDAP_USER_FILTER` - a user's unique identifier (if the primary key is `uid` then the variable must be set to `(uid=%(user)s)`)

**NOTE**: By default the LDAP support is not activated

By default a user admin (password: admin) will be created along with a dummy assignment.
You can visit the website by going to `http://localhost:7000/`.

To change the assignment go to `http://localhost:7000/admin/` and log in as the admin.
Next by clicking the assignments tab and then choosing one of the results you can edit that assignment.

## Run the UI securely using https

1. Replace the variables inside `etc/.env.compose-nginx` with the correct values
2. Place the certificate (*.key and *.pem files) inside `etc/cert/`. They must be saved as certificate.pem
3. Deploy using docker compose the the `compose-nginx.yml` configuration

```
docker compose -f etc/compose-nginx.yml --env-file etc/.env.compose-nginx -p nginx-ui up
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
