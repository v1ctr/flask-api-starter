# Flask API Starter with Authentication
This Flask API Starter helps creating new flask api projects fast.
Basic features like authentication, unit testing and more are already setup and ready to use.
## Install
    pip install -r requirements.txt

## Database Migration with Flask-Migrate

### Create a Migration Script
    flask db migrate -m "migration message"
    
### Upgrading the Database
    flask db upgrade
    
## Flask Python Shell

### Start Flask Shell
    export FLASK_APP=run.py
    export FLASK_DEBUG=1
    flask shell

### Exit Flask Shell
    exit()
    
### Creating/Removing tables
Use with caution. All data in database will be lost.

    db.create_all()
    db.drop_all()
    
### Creating Users
    user = User("test@gmail.com")
    db.session.add(user)
    db.session.commit()

### Querying Users
Get all users

    User.query.all()

Get specific user

    User.query.filter_by(email="test@gmail.com").first()

Get native SQL query that SQLAlchemy generates
    
    str(User.query.filter_by(email="test@gmail.com"))
    
## Sending Emails

### Start Flask Shell 
    export FLASK_APP=run.py
    export FLASK_DEBUG=1
    export MAIL_USERNAME=<Gmail username>
    export MAIL_PASSWORD=<Gmail password>
    export MAIL_DEFAULT_SENDER=<Gmail mail adress>
    flask shell
    
To display the name as the sender you can set ```MAIL_DEFAULT_USER='User <user@example.com>'```

### Sending Email
    from app.email import send_email
    send_email('you@example.com', 'Subject', 'email')
    
## Testing
### Unit Tests
    export FLASK_APP=run.py
    export FLASK_DEBUG=1
    flask test

### Code Coverage
Code coverage tools measure how much of the application is excercised by unit tests. (Grinberg. M, 2018, Flask Web Development, O'REILLY)

    flask test --coverage
    
## Deployment

### Running a production web server
    gunicorn run:app
    
### Heroku
Testing with Heroku Local
    
    heroku local:run flask deploy
    heroku local

Deploying
    
    git push heroku master
    heroku run flask deploy
    heroku restart

Upgrading

    heroku maintenance:on
    git push heroku master
    heroku run flask deploy
    heroku restart
    heroku maintenance:off    

Logs

    heroku logs
    heroku logs -t
    
### Docker
Building the Container Image

    docker build -t flask-api-starter:latest .

Running the Conatiner

    docker run --name flask-api-starter -d -p 8000:5000 \
    -e SECRET_KEY=<secret_key>
    
If you get a permission denied error for ```boot.sh``` than change permissions:

    chmod +x boot.sh

## Docker Compose
    docker-compose up -d --build

## References
* The Flask API Starter Project is inspired by Miguel Grinbergs Book _Flask Web Development, 2nd Edition_