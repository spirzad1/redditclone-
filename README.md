# Flask Reddit Clone

This is for a Coursera course teaching Flask.

## Step-by-step Documentation

The 60-page [documentation](https://docs.google.com/document/d/16XEdoqeY2XH0ROYiVefino9cJgOta3oB52O1BvuoY_4/edit?usp=sharing) goes through each step of the development process of this Reddit clone, from building the "hello, world!" routes to the database models, all the routes, the front end, authentication nuances, and more.

No knowledge is assumed - the documentation is designed for inexperienced developers using the Cloud 9 IDE.

## Setup

After going into the directory, these are the steps to get the app up and running locally:

#### Step 1. Create a Virtual Environment and Install Dependencies

Create a new Virtual Environment for the project and source it.  If you don't have Virtual Environment yet, you can find installation [instructions here](https://virtualenv.readthedocs.org/en/latest/).

```
$ virtualenv venv
$ source venv/bin/activate
```

Next we need to install the project dependencies, which are listed in `pip.req`. If you have issues, try install MySQL python dev libs.

```
(venv) $ pip install -r pip.req
```

#### Step 2. Set up the Database

Enter the MySQL shell and create a Flask app user and database running locally. If you don't have MySQL yet, you can find installation [instructions here](http://dev.mysql.com/doc/refman/5.7/en/installing.html).

```
mysql> create database reddit;
mysql> create user 'reddit'@'localhost' identified by 'reddit';
mysql> grant all privileges on reddit.* to 'reddit'@'localhost';
```

Now apply the models defined in the flask app as such:

```
(venv) $ ./migrate.py db init
(venv) $ ./migrate.py db migrate
(venv) $ ./migrate.py db upgrade
```

For most table changes, edit reddit/models.py, and run the above migrate and upgrade commands again.

If you happen to change a foreign key, or delete the migrations folder, run the above init, migrate and upgrade commands again.

#### Step 3. Run the Server

Now we're ready to start our server which is as simple as:

```
(venv) $ ./run.py
```

Optional: If we want to expose this to a public facing URL, we can use [ngrok](https://ngrok.com/):

```
(venv) $ ./ngrok http 5000
```

## Credit

Built by Sakib Jalal, Jamie Liao, and Mihai Andrei at Rutgers University, kept under the MIT License.
