# Simple Digital Twin
A fast and easy application to render your digital twin data. 

A fork of [Deploy a Python (Django) web app to Azure App Service - Sample Application](https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart)

### Taking components from standard MS Azure Github Pages.
* [Django / Microsoft Identity Platform](https://github.com/Azure-Samples/ms-identity-python-django-tutorial)

If you need an Azure account, you can [create one for free](https://azure.microsoft.com/en-us/free/).

## For local development
Save azure costs by running the application locally to test. Azure deployment to follow TBD, but the origional MSFT repo above has these instructions. 

I'm using Miniconda in my local environment. However it works the same either way. 

Steps to build your local environment in Miniconda (one time setup):
1. `conda create -n digitaltwin` to create the environment.
2. `pip install -r requirements.txt` to install the needed libraries. 
3. `conda env config vars set SECRET_KEY=123abc` to set the default library.
4. `python manage.py makemigrations`
5. `python manage.py migrate`
6. `python manage.py runserver`

# To configure Login with GH:
1. `pip install git+https://github.com/azure-samples/ms-identity-python-utilities@main`
2. Create your needed app registration and follow the instructions in the _usefull links_ below.

## When you deploy to Azure

For deployment to production, create an app setting, `SECRET_KEY`. Use this command to generate an appropriate value:

```shell
python -c 'import secrets; print(secrets.token_hex())'
```



## Usefull Links: 
* [AAD login in Django](https://learn.microsoft.com/en-us/training/modules/msid-django-web-app-sign-in/) 
* [Code examples of AAD](https://github.com/Azure-Samples/ms-identity-python-django-tutorial/blob/main/1-Authentication/sign-in/Sample/settings.py)