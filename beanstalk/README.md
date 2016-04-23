# Setup
## Managinng secrets

All application which will be deployed to AWS should be set up with
[*git secret*](https://github.com/awslabs/git-secrets)

When making commits and merges, the hook will scan for any potential
security breach such as password.

## Setup Virtual Environment

`Virtualenv` is a tool to keep the dependencies required by different
projects in separate places, by creating virtual Python environments
for them

To setup the virtual environment, we will need to install virtualenv.

```
pip install virtualenv

```

Then change to the project root and start the virtual.
```
cd ~/Github/aws_test/beanstalk/random-walker/
virtualenv venv/

```

To activate the virtual environment
```
source venv/bin/activate
```

All Python packages used should be installed through `pip`, and all
current packages should be updated and saved to a requirement file.

```
pip freeze > requirements.txt
```

If a requirement file which lists all the package required, they can
be installed via

```
pip install -r requirements.txt
```

To deactivate the virtual environment just simply type
```
deactivate
```


## Setup AWS account

## Setup AWS CLI and EB CLI

Install the AWS Command line tool.
```
pip install awsebcli
```


## Install Docker

Update and install docker.
```
sudo apt-get update && sudo apt-get install docker-engine
```

```
pip install docker-compose
```

Install the docker machine
```
curl -L https://github.com/docker/machine/releases/download/v0.7.0-rc3/docker-machine-`uname -s`-`uname -m` >/usr/local/bin/docker-machine && \
  chmod +x /usr/local/bin/docker-machine
```

If you have the [permissiong or curl
problem](https://forums.docker.com/t/permission-denied-when-trying-to-install-compose-on-ubuntu/1034/5),
then run the following.

```
sudo bash -c "curl -L https://github.com/docker/machine/releases/download/v0.7.0-rc3/docker-machine-`uname -s`-`uname -m` > /usr/local/bin/docker-machine && chmod +x /usr/local/bin/docker-machine"
```

After Docker has been installed, create a `Dockerfile` then run the
following where the `Dockerfile sits to create the container.

```
sudo docker build -t mkao006/random_walker .
```

To run the container locally

```
sudo docker run --publish=8001:8000 mkao006/random_walker
```

After the image has been built successfully, push the image to the
docker hub.

```
sudo docker push mkao006/random_walker
```

To remove failed build which has the name <none>
```
sudo docker images | grep \<none\> | tr -s ' '| cut -d ' ' -f 3 | xargs sudo docker rmi -f
```

To run inside a specific Docker image
```
docker run -i -t --entrypoint /bin/bash <imageID>
```


## Setting up the Django App

### Storing Secrets

The secrets should be directly exposed in the `settings.py` file. It
should be contained in the `settings.json` file then read into the
app. The `settings.json` file should not be added to `.gitignore` and
should not be push to remote.

The structure of the file is as follow:
```
{
    "SECRET_KEY": <secret_key_of_the_django_app>
    "BUCKET_NAME": <s3_bucket_name>,
    "AWS_ACCESS_KEY_ID": <amazon_access_key_id>,
    "AWS_SECRET_ACCESS_KEY": <amazon_secret_access_key>,
    "RDS_DB_NAME": <name_of_the_data_base>,
    "RDS_USERNAME": <username_of_the_database>,
    "RDS_PASSWORD": <password_of_the_database>,
    "RDS_HOSTNAME": <endpoint_of_the_aws_rds>,
    "RDS_PORT": <port_of_the_aws_rds>
}
```


## Elastic Beanstalk

```
eb init
```

## Database
NOTE (Michael): Need to add a section on how to create the db from
scratch.

To create a database instance for the beanstalk
```
aws rds create-db-instance\
    --db-name random_walker_db\
    --db-instance-identifier random-walker-db\
    --db-instance-class db.t2.micro\
    --allocated-storage 5\
    --engine postgres\
    --port 5432\
    --no-multi-az\
```

For more information please see [Using Elastic Beanstalk with Amazon
RDS](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/AWSHowTo.RDS.html)

For more command line reference please see [AWS CLI RDS
Reference](http://docs.aws.amazon.com/cli/latest/reference/rds/)

# Deployment
## Local

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


To start the website on elastic beanstalk, we need to first restore
the database instance. 

```
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier random-walker-db \
    --db-snapshot-identifier random-walker-db-final-snapshot\
    --db-instance-class db.t1.micro \
    --port 5432 \
    --no-multi-az\
    --region ap-southeast-1
```

When the database is restored, then we need to update the vpc security
group to the previous setting.

```
aws rds modify-db-instance\
    --db-instance-identifier random-walker-db\
    --vpc-security-group-ids sg-6ed9070a\
    --region ap-southeast-1
```



When the db instance is created then we can create the application
environment on Elastic Beanstalk. The instance type has been set to
minimum and a single instance is launched for testing to reduce cost.

```
eb create -i t2.micro --single
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

After the environment has been created with `eb create`, any change
can be deployed with

```
eb deploy
```

For more command reference please see [EB CLI Command
Reference](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-cmd-commands.html?icmpid=docs_elasticbeanstalk_console)


To stop the deployment, we first terminate Beanstalk to ensure all
information are still passed and saved to RDS.

```
eb terminate
```

We can then delete previous db snapshot, then save the current
snapshot before deleting the db instance.

```
aws rds delete-db-snapshot\
    --db-snapshot-identifier random-walker-db-final-snapshot\
    --region ap-southeast-1
aws rds delete-db-instance\
    --db-instance-identifier random-walker-db\
    --final-db-snapshot-identifier random-walker-db-final-snapshot\
    --region ap-southeast-1
```


