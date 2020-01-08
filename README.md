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

## Testing
### Unit Tests
    export FLASK_APP=run.py
    export FLASK_DEBUG=1
    flask test

### Code Coverage
Code coverage tools measure how much of the application is excercised by unit tests. (Grinberg. M, 2018, Flask Web Development, O'REILLY)

    flask test --coverage