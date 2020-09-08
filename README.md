## Scrapping service

### Requirements
* Python 3.6.1

### 1. Clone our repository
    git clone https://github.com/ivanauchynnikau/scrapper-service.git
    cd scrapper-service

### 2. Set up a python environment
We highly recommend installing [pyenv](https://github.com/pyenv/pyenv). 
This tool helps you to install different versions of python and set up 
virtual environments easily. Follow those instructions https://github.com/pyenv/pyenv-installer 
to install `pyenv`. After installing, run this:

    pyenv install 3.6.1
    pyenv virtualenv 3.6.1 scrapping-service-3.6.1
    pyenv local scrapping-service-3.6.1
    
### 3. Activate virtual environment
    source /home/ivan/.pyenv/versions/scrapping-service-3.6.1/bin/activate
    
    
### 4. Install requirements
    pip install -r requirements.txt
    
### 5. Setup config data
go to `scrapper-service/src/scrappingservice` and create `.env` file (config for development) 
with next content

    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT = 587
    EMAIL_HOST_USER=[YOUR_EMAIL]
    EMAIL_HOST_PASSWORD=[YOUR_EMAIL_PASSWORD]
    
    DEBUG=True    
    
### 6. Apply migrations    
go to `scrapper-service/src/`

    python manage.py migrate
    
### 7. Create admin account
    python manage.py createsuperuser    
    
### 8. Run server    
    python manage.py runserver 0:8080

*Enjoy!*


    
     





