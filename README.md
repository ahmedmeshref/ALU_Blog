# ALU_Blog
__Version 1.0.0__

The African Leadership University is growing with two communities, one in Rwanda and another in Mauritius. 
From an institutional level, both campuses might be well linked and growing together under one institution. 
But, from the students' perspective, each community is separated and there doesn’t exist one platform that 
brings both communities together to facilitate and encourage the process of communication between members, 
opportunities and experience sharing between students, … etc. ALU Blog platform is meant to be a joint to 
link both communities together under one platform with all staff and students from both campuses together
 to share and discuss news, opportunities, issues, … etc.

## Installation
**Be sure to use the same version of the code as the version of the docs you're reading.** 
You probably want the latest tagged version, but the default Git version is the master branch. ::

```bash
# clone the repository
$ git clone https://github.com/ahmedmeshref/ALU_Blog.git 
# navigate to the directory of the downloaded folder
$ cd ALU_Blog
```

**Setup your database**

Open SQL shell
```bash
# create a new database from sql shell
$ CREATE DATABASE ALU_Blog;
```

 

**Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all required libraries.**

```bash
# install all required packages from the requirements file
$ pip install -r requirements.txt
```
**Edit Configuration file**

Edit the following attributes from the config file

- SECRET_KEY = 'Use any random 16 characters'
- SQLALCHEMY_DATABASE_URI = "postgresql://UserName:Password@localhost:5432/ALU_Blog"
- MAIL_USERNAME = "Your Gmail username"
- MAIL_PASSWORD = "Your Gmail password"


**Run**
```bash
$ python run.py
```
Open http://127.0.0.1:5000 in a browser.


## Instructions
- If you use the register page, then the system will create an end 
user account
- For super admin, register and then change your account to a super admin
using sql 
- To add admins, you need to be register as a super admin.

## Deployment ``Heroku``

> To deploy the website on Heroku 

__Install guinicorn locally__
```
pip install gunicorn
```
__Install Heroku CLI__

https://devcenter.heroku.com/articles/heroku-cli

__Login via CLI__
```
heroku login
```

__Create app__
```
heroku create alublog
```

__Create database__
```
heroku addons:create heroku-postgresql:hobby-dev --app alublog
```

__Get URI__
```
heroku config --app alublog

# set the BADATBASE_URI to the output 
```

__Deploy with Git__
```
git add . 
git commit -m 'Intial Deploy'
heroku git:remote -a appname
git push heroku master
```

__Add table to remote database__
```
heroku run python
>>> from blog import db
>>> db.create_all()
>>>exit()
```

__Visit app__
```
# command will direct you to the website
heroku open
```

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [Postgresql](https://www.postgresql.org/) - Database management system
* [JavaScript](https://devdocs.io/javascript/) - Used for async communication between the front-end and back-end
* [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) - Used for creating templates 
* [Bootstrap](https://getbootstrap.com/) - Used for styling the html 


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors
* **Ahmed Meshref** - *Initial work* - [AhmedMeshref](https://github.com/ahmedmeshref)

## License
[MIT](https://choosealicense.com/licenses/mit/)