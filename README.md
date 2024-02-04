# Simple Digital Twin application framework
A simple, easy to deploy, easy to manage digital twin rendering and reporting platform. 
* runs off of your data platform in Azure without copying
* preference on easy access and use, as opposed to high quality visualization and cosmetics
* designed for the enterprise
* free and open source
* built to be easy, scalable, and focus on solving business problems

## Demo Link
Currently:
* [Flat file rendered in 3d, with current-state telemetry](https://app-simple-digital-twin.azurewebsites.net/simple_twin_2d/3d/twin/?boundary_id=boundary17529430240082)
* [Flat file rendered in 3d, with current-state telemetry](https://app-simple-digital-twin.azurewebsites.net/simple_twin_2d/2d/twin/?boundary_id=boundary17529430240082)

Comming Soon:
* AI Chat With Data
* 3d Model View
* More variety and extensibility of shapes and rendering


# Business Case
Most digital twin platforms are built one at a time. You load a cad model into a virtual machine and then one at a time attach each part of your data into that model. Then repeat for the next use case. This is ideal for MVPs and POCs, but it is not an ideal workflow for the enterprise. 

![Alt text](/docs/images/reasoning.png?raw=true "business case")

## What makes this application different? 
The goal of this application is that you would set it up once, configure it, and then it would be able to operate over all the data objects in your tenant via connectors and queries. Generally, applications of this nature tend to be silos. You create a virtual environment, you load one asset, you load some data and do all of that within that one application. Your next application requires the same amount of work. This makes factory of the future applications costly to develop. Instead, our application connects to your data platform, where you are storing all of this data, and managing the workflow within your existing data platform. 
![Alt text](/docs/images/dataflow.png?raw=true "data flow")


This application is the control and reporting plane for your digital twin data graph. You don't load data into it. You point connectors to your data graph, and your asset blobs. The application queries the graph to get the assets and data that it needs for real time rendering. 

This assumes that you already have an ontology of your enterprise data, or are workign on one.  
![Alt text](/docs/images/ontology_example.png?raw=true "business case")

That ontolgoy will need to have:
* a serchable hierarchy of objects
* `asset`, `anchor`, and `boundary` nodes with relationships to your hierarchy.

# Two ways of connecting your assets to your data


# Application contents
Bassic application features:
* Django MCV framework
* Incorporates AAD form the start, no user/password login. 
 




### Taking components from standard MS Azure Github Pages.
* [Django / Microsoft Identity Platform](https://github.com/Azure-Samples/ms-identity-python-django-tutorial)


# For the Demo
This is made to be an enterprise ready tool, not a POC or sales tool. However in order to validate the applications fitness I've created an example model for engineers to review. You can access this in `infra/demo`. 


## For local development
Save azure costs by running the application locally to test. Azure deployment to follow TBD, but the original MSFT repo above has these instructions. 


Steps to build your local environment in Miniconda (one time setup):
1. `conda create -n azurewebapp python=3.8` to create the environment.
2. `conda activate azurewebapp`
3. `pip install -r requirements.txt` to install the needed libraries. 
4. Set the environment variables see section below.
5. `python manage.py makemigrations`
6. `python manage.py migrate`
7. `python manage.py runserver`

### Setting environment variables (locally)
You need to set the conda environment variables.
`conda env config vars set SECRET_KEY=123abc` to set the env vars
Here are the list of vars the system will need:
* SECRET_KEY
* DEBUG
* AAD_CLIENT_ID
* AAD_CLIENT_CREDENTIAL
* AAD_TENANT_ID
* AZURE_ACCOUNT_NAME
* AZURE_STORAGE_KEY

For the connectors, see the [connectors readme doc](./connectors/connectors.md)


Confirm you have the correct variables with `conda env config vars list`

* Remove your env with `conda remove --name azurewebapp --all`

## To configure Login with AAD:
* Create your needed app registration and follow the instructions in the _useful links_ below. That process isn't automated here.

# Testing: 
`http://localhost:8000/simple_twin_2d/3d/twin/?scene_id=pnid1`


## Useful Links: 
* [AAD login in Django](https://learn.microsoft.com/en-us/training/modules/msid-django-web-app-sign-in/) 
* [Code examples of AAD](https://github.com/Azure-Samples/ms-identity-python-django-tutorial/blob/main/1-Authentication/sign-in/Sample/settings.py)