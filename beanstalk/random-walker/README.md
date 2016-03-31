## Development 

To launch test environment first start up the virtual environment in
the command line.

```
source venv/bin/activate
```

Then change directory to the application and run the test server

```
cd random_walker
python manage.py runserver
```

The website is then available to view at the specified port.

## Production

To start the website on elastic beanstalk, we need to first create the
environment. Replace the XXXX with the username and password.

```
eb create -db.engine postgres -db.user XXXX -db.pass XXXX
```

if the environment is created successfully, then we can open the website.

```
eb open
```

if there is a problem then we can check the log or log-on to [AWS
console](https://console.aws.amazon.com/console/home) to check the
status.

```
eb logs
```

For more information, follow this [tutorial](https://realpython.com/blog/python/deploying-a-django-app-to-aws-elastic-beanstalk/)

## Managinng secrets

The repository is set up with [*git secret*](https://github.com/awslabs/git-secrets)

When making commits and merges, the hook will scan for any potential
security breach such as password.