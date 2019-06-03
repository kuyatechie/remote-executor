remote-executor app
==========

Description
-----------
This software is composed of different components.

1. web      :       A Django based web application that accepts HTTP request via REST API. 
                    The purpose of this component is to accept scripting tasks from users.
                    A task is a combination of script name and the corresponding argument pairs.

2. worker   :       A Python based app that accepts scripting tasks and execute it in the server.
                    It reads the messages from a message queue, execute the scripting tasks and records the metadata.

3. mq       :       A message queue based from RabbitMQ. 
                    It is a standalone component that accepts scripting task from web server, put it in a queue and wait
                    for some worker to process the task.
                    
4. db       :       A PostgreSQL database that stores the records and metadata of the tasks being done. The webserver 
                    create the task item to the database and assigns a unique identifier to each tasks while the workers
                    adds the information metadata about the execution of the tasks based on the unique id.

5. ftp      :       An ftp server based on Python pyftpdlib. It basically allows the users to copy files into the system.


Also these components are being managed by different tools
1. docker   :       A containerization tool capable of deploying applications at ease. It allows separation of dependencies
                    and rapid deployment to different host servers. Together with docker-compose, this tool is used to
                    pull base containers needed by the components and create environment separation so that the application 
                    is easily managed. These components make use of docker: web, mq, db.
                    
2. supervisord      A Python based tool capable of monitoring and controlling Linux processes. The components being managed
                    are ftp and workers.

      
System Requirements:
-------------------
This application is tested in an Ubuntu based environment (Lubuntu 4.18.0-13-generic #14-Ubuntu) installed in VirtualBox. 
Though these are just minimum requirements, operational requirements will mostly depends on the scripts being run and the 
number of component instances.

Operating System: Debian based Linux (Fedora based can be used but still untested)

Recommended Operating System: Lubuntu 4.18.0-13-generic #14-Ubuntu (See https://lubuntu.net/downloads/)

Processor: 4 cores

Memory: 4096 MB

Storage: At least 10GB

Ports: web port 8000, db port 5432, mq port 5672, ftp port 2121 (need these ports unused)


Installation Requirements:
-------------------------
/1/ Python 2.7 (tested using Python 2.7.15)

Linux based systems are usually shipped with Python 2.7 already installed. 
If not, please follow official documentation on how to install this. 
https://www.python.org/downloads/

Check Python installation:
```
arvin@ubuntu:~/workspaces/remote-executor$ python -V
Python 2.7.15+
```

/2/ Docker

To install Docker please follow official documentation here: 
https://docs.docker.com/install/linux/docker-ce/ubuntu/
It is important that the user has permission to use docker.

Quick Guide for installation in Lubuntu:
```
sudo apt-get install     apt-transport-https     ca-certificates     curl     software-properties-common
wget https://download.docker.com/linux/ubuntu/dists/cosmic/pool/test/amd64/containerd.io_1.2.1~rc.0.1_amd64.deb
wget https://download.docker.com/linux/ubuntu/dists/cosmic/pool/test/amd64/docker-ce-cli_18.09.1~2.1.rc1-0~ubuntu-cosmic_amd64.deb
wget https://download.docker.com/linux/ubuntu/dists/cosmic/pool/test/amd64/docker-ce_18.09.1~2.1.rc1-0~ubuntu-cosmic_amd64.deb
sudo dpkg -i containerd.io_1.2.1~rc.0.1_amd64.deb docker-ce-cli_18.09.1~2.1.rc1-0~ubuntu-cosmic_amd64.deb docker-ce_18.09.1~2.1.rc1-0~ubuntu-cosmic_amd64.deb 
sudo groupadd docker
sudo usermod -aG docker $USER
```

Check Docker:
```
arvin@ubuntu:~/workspaces/remote-executor$ docker -v
Docker version 18.09.1-rc1, build bca0068

arvin@ubuntu:~/workspaces/remote-executor$ sudo docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS
```

Installation of dependencies:
-----------------------------
/1/ Docker-Compose
To install Docker-Compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Check Docker Compose
```
arvin@ubuntu:~/workspaces/remote-executor$ sudo docker-compose -v
docker-compose version 1.23.1, build b02f1306
```

/2/ Set up directories and environment variables in the parent directory:
```
arvin@ubuntu:~/workspaces/remote-executor$ sudo chmod 755 install.sh
arvin@ubuntu:~/workspaces/remote-executor$ ./install.sh
arvin@ubuntu:~/workspaces/remote-executor$ export APPDIR=$(pwd)

```
Check:
```
arvin@ubuntu:~/remote-executor$ cat .env 
APPDIR=/home/arvin/workspaces/remote-executor
```

WARNING: If using different terminals to launch components, it is necessary to set the environment variable $APPDIR
to correct the default paths.
```
export APPDIR=<path to remote-executor directory>
```

/3/ Python dependencies and other dependencies

To install dependencies
```
arvin@ubuntu:~/workspaces/remote-executor$ sudo apt-get install python-django-common postgresql-client-common postgresql-client-10 python-pip supervisor -y
```

To install Python Dependencies execute in the parent directory:
```
arvin@ubuntu:~/workspaces/remote-executor$ pip install -r $APPDIR/requirements.txt
```

/4/ Pull docker images from Docker Hub
```
arvin@ubuntu:~/workspaces/remote-executor$ sudo docker pull python:3.6-alpine
arvin@ubuntu:~/workspaces/remote-executor$ sudo docker-compose pull
```

/5/ Build docker images
```
arvin@ubuntu:~/workspaces/remote-executor$ sudo docker-compose build
mq uses an image, skipping
db uses an image, skipping
Building web
Step 1/8 : FROM python:3.6-alpine
 ---> 1d981af1e3b4
Step 2/8 : ENV PYTHONUNBUFFERED 1
 ---> Using cache
 ---> 7d4ba95beb88
Step 3/8 : RUN mkdir /app
 ---> Using cache
 ---> c5967ad11497
Step 4/8 : WORKDIR /app
 ---> Using cache
 ---> 4f26a9f38ac9
Step 5/8 : COPY . .
 ---> 18dd448c1eb2
Step 6/8 : RUN apk update &&     apk add postgresql-dev musl-dev gcc &&     pip install --no-cache-dir -r requirements.txt
 ---> Running in a1183c3f179e
fetch http://dl-cdn.alpinelinux.org/alpine/v3.8/main/x86_64/APKINDEX.tar.gz
fetch http://dl-cdn.alpinelinux.org/alpine/v3.8/community/x86_64/APKINDEX.tar.gz
...
...
...
```

After these the application is ready to launch!


Launching the app
-----------------
/1/ Launch web, db and mq via docker-compose.
```
arvin@ubuntu:~/workspaces/remote-executor$ sudo docker-compose up --detach
Creating web ... done
Creating db ... done
Creating mq ... done
```
It can be run in the foreground by removing --detach in the command overriding configurations.

/2/ Check if services are already up. Check database if done initialization. 
If not wait for it to initialize. (See developer notes to make db data persistent)
```
arvin@ubuntu:~/workspaces/remote-executor$ sudo docker-compose ps
Name              Command               State                           Ports                        
-----------------------------------------------------------------------------------------------------
db     docker-entrypoint.sh postgres    Up      0.0.0.0:5432->5432/tcp                               
mq     docker-entrypoint.sh rabbi ...   Up      25672/tcp, 4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp
web    python3 manage.py runserve ...   Up      0.0.0.0:8000->8000/tcp  

arvin@ubuntu:~/workspaces/remote-executor$ sudo docker exec -it db psql -U postgres
psql (11.1)
Type "help" for help.

postgres=#exit

```

/3/ Migrate database model to newly created database
```
arvin@ubuntu:~/workspaces/remote-executor$ sudo docker exec -it web python3 manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, task
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying task.0001_initial... OK
```

/4/ Launch worker and ftp servers
```
arvin@ubuntu:~/workspaces/remote-executor$ supervisord -c supervisord.conf
```
It can be run in the foreground by adding --nodaemon in the command overriding configurations


How to use:
-----------
### Sending scripting task request
Basically, for a script to be executed, an HTTP Request (json format) should be sent to the web server (using port 8000).
The web server can receive json structured format containing two variables, "script" and "arguments"
Currently there are sample scripts installed located in $APPDIR/scripts folder ready for use:

ls.sh - can list information in the $APPDIR/homedir. It can accept arguments like the linux "ls" shell command.
mkdir.sh - can create directory in the $APPDIR/homedir. It can accept arguments like the linux "mkdir" shell command.
touch.sh - can create directory in the $APPDIR/homedir. It can accept arguments like the linux "touch" shell command.

To extend the list of scripts that can be run, a shell script can be created in the $APPDIR/scripts directory.
To be able to pass (and parse) arguments, the  "$@" can be used inside the script to read all parameters and 
perform scripting tasks.

Command arguments are often declared in pairs, option and value. Example options are "--source", "--destination".
For single arguments, the value field can be blank.
For multiple parameters, it can be assigned to value field separated using spaces like "param1 param2 ..."

JSON format: { "script" : "filename", "arguments" : { "option1" : "value1", "option2" : "value2", ... } }

REST API: POST <hostname>:8000/task/create

#### Sample HTTP requests:

##### touch.sh
To use the touch script to create new file in the homedir, we can dissect the command to json structure.

Sample command: touch.sh sample_file.txt

script: touch.sh

arguments: "" : "sample_file.txt"

REST API: POST localhost:8000/task/create

JSON message body structure: { "script" : "touch.sh", "arguments" : { "" : "sample_file.txt" } }

###### HTTP Response

All scripting tasks are assigned an individual unique id "uid" to track the progress.

```
{
  "id": 1,
  "uid": "604a5e38-06f9-11e9-a0e9-0242ac140004",
  "created": "2018-12-23T21:26:14.356933Z",
  "script": "touch.sh",
  "arguments": {
    "": "sample_file.txt"
  },
  "started": null,
  "finished": null,
  "diskspace_before": null,
  "diskspace_after": null,
  "retcode": null
}
```

Logs are created by worker using uid as filename


```
arvin@ubuntu:~/remote-executor/logs/worker/tasks$ ll
total 8
drwxrwxr-x 2 arvin arvin 4096 Dec 24 05:28 ./
drwxrwxr-x 3 arvin arvin 4096 Dec 24 04:12 ../
-rw-rw-r-- 1 arvin arvin    0 Dec 24 05:28 604a5e38-06f9-11e9-a0e9-0242ac140004_stderr.log
-rw-rw-r-- 1 arvin arvin    0 Dec 24 05:28 604a5e38-06f9-11e9-a0e9-0242ac140004_stdout.log
```

The sample file is created in homedir and verified by accessing ftp.

```
arvin@ubuntu:~/remote-executor$ ftp localhost 2121
Connected to localhost.
220 Hello! Welcome to the remote-executor app.
Name (localhost:arvin): ftp
331 Username ok, send password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> dir
200 Active data connection established.
125 Data connection already open. Transfer starting.
-rw-rw-r--   1 arvin    arvin           0 Dec 23 21:28 sample_file.txt
226 Transfer complete.
ftp>
```

##### mkdir.sh

To use the mkdir script to create new dir in the homedir (if it doesn't exist), we can dissect the command to json structure.

Sample command: mkdir.sh -p sample_dir

script: mkdir.sh

arguments: { "-p" : "", "" : "sample_dir" }

REST API: POST localhost:8000/task/create

JSON message body structure: { "script" : "touch.sh", "arguments" : { "-p" : "", "" : "sample_dir" } }

###### HTTP Response

All scripting tasks are assigned an individual unique id "uid" to track the progress.

```
{
  "id": 3,
  "uid": "6143f61e-06fb-11e9-bec4-0242ac140004",
  "created": "2018-12-23T21:40:34.991223Z",
  "script": "mkdir.sh",
  "arguments": {
    "-p": "",
    "": "sample_dir"
  },
  "started": null,
  "finished": null,
  "diskspace_before": null,
  "diskspace_after": null,
  "retcode": null
}
```

Logs are created by worker using uid as filename

```
arvin@ubuntu:~/remote-executor/logs/worker/tasks$ ll 6143f61e-06fb-11e9-bec4-0242ac140004*
-rw-rw-r-- 1 arvin arvin 0 Dec 24 05:40 6143f61e-06fb-11e9-bec4-0242ac140004_stderr.log
-rw-rw-r-- 1 arvin arvin 0 Dec 24 05:40 6143f61e-06fb-11e9-bec4-0242ac140004_stdout.log
```

The sample dir is created in homedir and verified by accessing ftp.

```
arvin@ubuntu:~/remote-executor/logs/worker/tasks$ ftp localhost 2121
Connected to localhost.
220 Hello! Welcome to the remote-executor app.
Name (localhost:arvin): ftp
331 Username ok, send password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> dir
200 Active data connection established.
125 Data connection already open. Transfer starting.
drwxrwxr-x   2 arvin    arvin        4096 Dec 23 21:40 sample_dir
-rw-rw-r--   1 arvin    arvin           0 Dec 23 21:28 sample_file.txt
226 Transfer complete.
ftp>
```


##### Metadata contents

```
started	"2018-12-24T05:28:11.832646Z"
finished	"2018-12-24T05:28:12.846469Z"
diskspace_before	3196336
diskspace_after	3196328
retcode	0
```

started:			Datetime object to record when the scripting task started.
finished:			Datetime object to record when the scripting task ended.
diskspace_before:	Integer to display remaining storage in homedir before the activity (bytes)
diskspace_after:	Integer to display remaining storage in homedir after the activity (bytes)
retcode:			Return code of the execution (a value of 0 being successful)


### Using REST API to check the metadata of a scripting task

#### By using primary key
REST API: GET <hostname>:8000/task/view/pk:<number>

Example: GET http://localhost:8000/task/view/pk:1
Response: JSON pretty format
```
id	1
uid	"604a5e38-06f9-11e9-a0e9-0242ac140004"
created	"2018-12-23T21:26:14.356933Z"
script	"touch.sh"
arguments	
	"sample_file.txt"
started	"2018-12-24T05:28:11.832646Z"
finished	"2018-12-24T05:28:12.846469Z"
diskspace_before	3196336
diskspace_after	3196328
retcode	0
```

#### By using uid
REST API: <hostname>:8000/task/view/uid:<number>

Example: GET http://localhost:8000/task/view/uid:c768b028-06fa-11e9-9dbf-0242ac140004
Response: JSON pretty format
```
id	2
uid	"c768b028-06fa-11e9-9dbf-0242ac140004"
created	"2018-12-23T21:36:16.862779Z"
script	"touch.sh"
arguments	
-p	""
	"sample_dir"
started	"2018-12-24T05:36:16.894360Z"
finished	"2018-12-24T05:36:17.912579Z"
diskspace_before	3196308
diskspace_after	3196296
retcode	1
```

### Using REST API to list the tasks in different scenarios

#### Check tasks created today
REST API: <hostname>:8000/task/view/date:today

Example: GET http://localhost:8000/task/view/date:today
Response: JSON Pretty Format

```
0	
id	1
uid	"604a5e38-06f9-11e9-a0e9-0242ac140004"
created	"2018-12-23T21:26:14.356933Z"
script	"touch.sh"
arguments	"{'': 'sample_file.txt'}"
started	"2018-12-24T05:28:11.832646Z"
finished	"2018-12-24T05:28:12.846469Z"
diskspace_before	3196336
diskspace_after	3196328
retcode	0
1	
id	2
uid	"c768b028-06fa-11e9-9dbf-0242ac140004"
created	"2018-12-23T21:36:16.862779Z"
script	"touch.sh"
arguments	"{'-p': '', '': 'sample_dir'}"
started	"2018-12-24T05:36:16.894360Z"
finished	"2018-12-24T05:36:17.912579Z"
diskspace_before	3196308
diskspace_after	3196296
retcode	1
2	
id	3
uid	"6143f61e-06fb-11e9-bec4-0242ac140004"
created	"2018-12-23T21:40:34.991223Z"
script	"mkdir.sh"
arguments	"{'-p': '', '': 'sample_dir'}"
started	"2018-12-24T05:40:35.023554Z"
finished	"2018-12-24T05:40:36.042565Z"
diskspace_before	3196308
diskspace_after	3196296
retcode	0
```

#### Check tasks created at any day in YYYMMDD format
REST API: <hostname>:8000/task/view/date:YYYYMMDD

Example: http://localhost:8000/task/view/date:20181223
Response: JSON Pretty Format

```
0	
id	1
uid	"604a5e38-06f9-11e9-a0e9-0242ac140004"
created	"2018-12-23T21:26:14.356933Z"
script	"touch.sh"
arguments	"{'': 'sample_file.txt'}"
started	"2018-12-24T05:28:11.832646Z"
finished	"2018-12-24T05:28:12.846469Z"
diskspace_before	3196336
diskspace_after	3196328
retcode	0
1	
id	2
uid	"c768b028-06fa-11e9-9dbf-0242ac140004"
created	"2018-12-23T21:36:16.862779Z"
script	"touch.sh"
arguments	"{'-p': '', '': 'sample_dir'}"
started	"2018-12-24T05:36:16.894360Z"
finished	"2018-12-24T05:36:17.912579Z"
diskspace_before	3196308
diskspace_after	3196296
retcode	1
2	
id	3
uid	"6143f61e-06fb-11e9-bec4-0242ac140004"
created	"2018-12-23T21:40:34.991223Z"
script	"mkdir.sh"
arguments	"{'-p': '', '': 'sample_dir'}"
started	"2018-12-24T05:40:35.023554Z"
finished	"2018-12-24T05:40:36.042565Z"
diskspace_before	3196308
diskspace_after	3196296
retcode	0
```

#### Count tasks created at any day in YYYMMDD format
REST API: <hostname>:8000/task/view/date:YYYYMMDD/count

Example: http://localhost:8000/task/view/date:20181223/count
Response: Integer
```
3
```

#### Viewing a chart containing number of tasks submitted per day for the current month
REST API: <hostname>:8000/task/charts/daily

See attached file: task-per-day.png
 
### Using REST API to check disk space usage for the current month
REST API: <hostname>:8000/task/charts/disk

See attached file: disk-space.png

### Connecting to homedir via ftp protocol
To be able to transfer and copy files to the system, ftp server is enabled at port 2121.

How to connect: ftp localhost 2121
Default username: ftp
Default password: ftp

```
arvin@ubuntu:~/remote-executor/logs/worker/tasks$ ftp localhost 2121
Connected to localhost.
220 Hello! Welcome to the remote-executor app.
Name (localhost:arvin): ftp
331 Username ok, send password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> dir
200 Active data connection established.
125 Data connection already open. Transfer starting.
drwxrwxr-x   2 arvin    arvin        4096 Dec 23 21:40 sample_dir
-rw-rw-r--   1 arvin    arvin           0 Dec 23 21:28 sample_file.txt
226 Transfer complete.
ftp>
```

Developers Notes:
-----------------
### Debug mode and Allow Shell mode

Debug Mode: Is a Django capability to allow debug of APIs for easier development and bug tracking. This is achieved
by setting env variable "WEB_DEBUG_MODE" in web component to 1 (default is 1 for the purpose of demonstration)   

Allow Shell Mode: The worker component can allow running of shell commands instead of script files for debug purposes
by setting env variable "WORKER_ALLOW_SHELL" in worker component to 1 (default is 1 for the purpose of demonstration).
This will mean any shell command can be executed by the worker in the homedir even without the shell scripts in place.

Sample JSON structure: { "script": "echo", "arguments" : { "" : "Hello World!" } }

REST API: http://localhost:8000/task/create

Response:

```
{
  "id": 4,
  "uid": "d9aa675a-06fd-11e9-8453-0242ac140004",
  "created": "2018-12-23T21:58:15.982526Z",
  "script": "echo",
  "arguments": {
    "": "Hello World!"
  }
```

Output:

```
arvin@ubuntu:~/remote-executor/logs/worker/tasks$ cat d9aa675a-06fd-11e9-8453-0242ac140004_stdout.log
Hello World!
```

## Home directory

Current home directory is located at $APPDIR/homedir. It can be accessed from the outside using ftp.

### Log files
The following components have log files created at specific locations.

1. web     :   $APPDIR/logs/web
2. db      :   $APPDIR/logs/db
3. mq      :   $APPDIR/logs/mq
4. ftp     :   $APPDIR/logs/ftp
5. worker  :   $APPDIR/logs/worker

Also all task executions logs are recorded and identified via its uid located in $APPDIR/logs/worker/tasks.

Format: 
1. stdout logs: uid_stdout.log
2. stderr logs: uid_stderr.log

### Persistent data for postgresql database

Data persistency can be achieved by mounting the volume to the database container.

Uncomment this part to achieve persistent data:

$APPDIR/docker-compose.yml line 35
```
    #  - $APPDIR/postgresql/data:/var/lib/postgresql/data
```

### Connecting to database
Connection to database is done via docker command:
```
arvin@ubuntu:~/workspaces/remote-executor$ docker exec -it db psql -U postgres
psql (11.1)
Type "help" for help.

postgres=#
```

To connect to database:
```
postgres=# \c taskdb 
You are now connected to database "taskdb" as user "postgres".
```

To view table:
```
taskdb=# table task_task;
 id |                 uid                  |            created            |  script  |        arguments         |            started            |           finished            | diskspace_before | diskspace_after | retcode 
----+--------------------------------------+-------------------------------+----------+--------------------------+-------------------------------+-------------------------------+------------------+-----------------+---------
  1 | 9db2b1d0-0668-11e9-9723-0242ac1b0004 | 2018-12-23 04:10:00.360991+00 | ls.sh    | {'-h': ''}               | 2018-12-23 12:10:00.399485+00 | 2018-12-23 12:10:01.414208+00 |          5632324 |         5632316 |       0
  2 | 36c524c8-0669-11e9-b488-0242ac1b0004 | 2018-12-23 04:14:17.173303+00 | mkdir.sh | {'-p': '', 'sample': ''} | 2018-12-23 12:14:17.209462+00 | 2018-12-23 12:14:17.215578+00 |          5632264 |         5632256 |     126
```

### Do you need to create new migration scripts for new django models? (and not affect existing data in database)

Django supports the migration of new models to old database. 

It can be done using this command inside web component: python3 manage.py makemigrations

To apply changes: python3 manage.py migrate


### Design considerations

Application design is pretty much straightforward.

http request ---> WEB ---> create task ---> MQ ---> consume_task ---> WORKERS --> execute_task ---> homedir <---> FTP

WEB <--- task data ---> DB <--- metadata <--- WORKER   
          

#### Why microservices?

With the emergence of containerization technologies, it is decided to make use of cloud native tools like Docker 
and design the system in such the way the individual components are treated like  microservices.
The following are the considerations made while developing the app.

1. Portability      :       The components are design in such way that every environment are independent to one another. 
                            This will likely increase ability to port to different systems regardless of common and
                            conflicting dependencies. Also, using Alpine Linux distributions make the containers very 
                            lightweight and portable while not losing functionality.
2. Scalability      :       It is anticipated that the more users using this application, the more heavier the workload
                            of highly used components (like the web service and worker nodes). For it to be addressed, the 
                            application is very flexible, allowing spawning of several web servers and worker node instances 
                            as the tasks are queued to an standalone message queue and workloads are shared by different
                            worker nodes.
3. Data Persistency :       An independent relational database is considered allowing management of task related 
                            data for retrieval and analysis of KPIs and different measurements. The database can be set 
                            to become persistent. In external database can also be used and easily plugged to the application.
4. REST API + FTP   :       To be able to maintain separation between user and servers, a webserver and FTP server is exposed 
							so that direct SSH to the servers are avoided and maintain security.


#### Spawning new worker nodes

This can be achieved by adding another [program: worker_num] entry to supervisor. Supervisor will create new process that will
run worker instance.
```
[program:worker_1]
command=python %(ENV_APPDIR)s/worker/worker.py
environment=WORKER_DIRECTORY_PATH="%(ENV_APPDIR)s/homedir/",WORKER_SCRIPT_PATH="%(ENV_APPDIR)s/scripts",WORKER_STDOUT_PATH="%(ENV_APPDIR)s/logs/worker/tasks",WORKER_STDERR_PATH="%(ENV_APPDIR)s/logs/worker/tasks",WORKER_ALLOW_SHELL"=1
autorestart=true
redirect_stderr=true
stdout_logfile=%(ENV_APPDIR)s/logs/worker/worker.log
stderr_logfile=%(ENV_APPDIR)s/logs/worker/err.log
```


### Development installation requirements
Aside from the aforementioned dependencies and installations, there are several installations to be done
for development purposes:

1. Python3.6
2. python3-django
3. requirements.txt for each components (web, ftp, worker)


Environment Variables:
----------------------

### Setting up Environment Variables

web component: These can be set via docker-compose.yml. Default values are:
1. WEB_DEBUG_MODE          1    
2. DATABASE_USER           "postgres"
3. DATABASE_PASSWORD       "postgres"
4. DATABASE_NAME           "taskdb"
5. DATABASE_TABLE_NAME     "task_task"
6. DATABASE_HOSTNAME       "localhost"
7. DATABASE_PORT           "5432"
8. MQ_HOSTNAME             "localhost"

db component: These can be set via docker-compose.yml. Default values are:
1. POSTGRES_PASSWORD: postgres
2. POSTGRES_USER: postgres
3. POSTGRES_DB: taskdb

worker component: These can be set via supervisord.conf. Default values are:
1. WORKER_DIRECTORY_PATH   "/homedir/"
2. WORKER_SCRIPT_PATH      "/logs/worker/scripts"
3. WORKER_STDOUT_PATH      "/logs/worker/tasks"
4. WORKER_STDERR_PATH      "/logs/worker/tasks"
5. WORKER_ALLOW_SHELL      1
6. MQ_HOSTNAME             "localhost"

ftp component: These can be set via supervisord.conf. Default values are:
1. FTP_USER                "ftp"
2. FTP_PASSWORD            "ftp"
3. FTP_HOSTNAME            "localhost"
4. FTP_PORT                2121
5. FTP_DIRECTORY           "/homedir/"


Developer:
----------
Arvin E. Cudanin - DevOps Engineer
email: arvin.cudanin@gmail.com