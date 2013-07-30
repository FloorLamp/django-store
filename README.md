# django-store

  Simple store application using Django and Bootstrap. Each store is a subdomain with its own database and admin page.

## Installation

    $ pip install -r requirements.txt    

## Adding a store

    $ python djangostore/add_store.py store_name
    $ ./manage.py syncdb --database=store_name
    $ ./manage.py migrate --database=store_name
    
  Now you can just visit store_name.yourstore.com.

## Testing
    
    $ ./manage.py test shoppingcart