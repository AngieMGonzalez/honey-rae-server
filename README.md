# honey-rae-server

## ERD
- https://dbdiagram.io/d/644c1e2cdca9fb07c439ccb2
- https://github.com/nashville-software-school/bangazon-llc/blob/cohort-62/book-3-levelup/chapters/HR_MODELS.md

## Migration of models 
- `python3 manage.py makemigrations repairsapi`
- `python3 manage.py migrate` creates tables in DB

## Resources
- https://docs.djangoproject.com/en/4.2/topics/db/models/
- Django Models - Overview of Django Models
- Extending the User Model - Explanation for how to add fields to the Django user
- Model Field Types - All the options for data types in a model
- One to Many Relationships - How to add a foreign key to a model
- Many to Many Relationships - How to set up - a Many-Many Relationship
- check what version of python `python manage.py version` 
- I'm running 4.2 right now

- packages are imported and defining routes

# CREATE POST reminder
- Now that you have a model, a view, a serializer, and the URL defining the route for 
[resource], the final step is to create a [resource] or two and then get them.

# Fixtures
- JSON files that contain some data for your database. Useful for initial creation of a development database, or for testing.
- set up your project with some fixtures so that you can provide some *initial, or seed, data* for your database, without the need to write any INSERT INTO statements in a SQL file
- https://docs.djangoproject.com/en/4.2/howto/initial-data/
- we are adding fixtures in JSON
- add info on `seed_database.sh` file
- https://github.com/nashville-software-school/bangazon-llc/blob/cohort-62/book-3-levelup/chapters/HR_SEED_DB.md
- `chmod u+x ./seed_database.sh` to make executable script
- https://linuxhandbook.com/make-file-executable/
- then run `./seed_database.sh` to install fixtures

## getting all customers from api 
- Adding the URL
So far we’ve set up the view and serializer but not which URL to use for the view. We need to add /customers to be supported by the API.

## React App
- https://github.com/nashville-software-school/honey-rae-react18

# Serialization cont
- https://watch.screencastify.com/v/CJPF5fiVlqsZH8nxo892 

# Notes
- migrate the models 
