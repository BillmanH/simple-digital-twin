# Azure Django Template
Quick templates that deploy python applications for the enterprise. I'm keeping this as a baseline template to streamline deployment to Azure Web Services.

A fork of [Deploy a Python (Django) web app to Azure App Service - Sample Application](https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart)

## What makes this template different? 
* Incorporates AAD form the start, no user/password login. 
* TODO: all secrets come from env vars (for deployment in Azure App Service).
* Data Science / Analytics focused
    * Uses `conda` environments instead of pip invironments.

### Taking components from standard MS Azure Github Pages.
* [Django / Microsoft Identity Platform](https://github.com/Azure-Samples/ms-identity-python-django-tutorial)

If you need an Azure account, you can [create one for free](https://azure.microsoft.com/en-us/free/).

## For local development
Save azure costs by running the application locally to test. Azure deployment to follow TBD, but the origional MSFT repo above has these instructions. 

I'm using Miniconda in my local environment. However it works the same either way. 

Steps to build your local environment in Miniconda (one time setup):
1. `conda create -n azurewebapp` to create the environment.
2. `conda activate azurewebapp`
3. `pip install -r requirements.txt` to install the needed libraries. 
4. `conda env config vars set SECRET_KEY=123abc` to set the default library.
5. `python manage.py makemigrations`
6. `python manage.py migrate`
7. `python manage.py runserver`

# To configure Login with AAD:
* Create your needed app registration and follow the instructions in the _usefull links_ below. That process isn't automated here.

## When you deploy to Azure
For deployment to production, create an app setting, `SECRET_KEY`. Use this command to generate an appropriate value:

```shell
python -c 'import secrets; print(secrets.token_hex())'
```



## Usefull Links: 
* [AAD login in Django](https://learn.microsoft.com/en-us/training/modules/msid-django-web-app-sign-in/) 
* [Code examples of AAD](https://github.com/Azure-Samples/ms-identity-python-django-tutorial/blob/main/1-Authentication/sign-in/Sample/settings.py)