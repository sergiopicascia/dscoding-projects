# How to use Reddit Rest API

## Register on teh Reddit Website

You firstly need to register on this [website](https://www.reddit.com) if you do not have an account. Login and Password are necessary to use API.

## Create Application

On this [web page](https://www.reddit.com/prefs/apps) you can create your API. Firstly, sign in to your account. There you are to see the section called "create application. It looks like that:

![ ](../Streamlit/Pictures/API%20page.png)

I've already created mine, but you can do the same for your purposes. Choose a name for it, choose 'script', add description. After that you will get your CLIENT_ID and CLIENT_SECRET that you can pass into the `Reddit_API_Wrapper`.  I use my own data which is confidential, so you will see there just import of variables from a file that I have added to .gitignore.  In "user_agent" you can write pretty much everyting you need, maybe just a version of your application. 

I use `praw`, which is a Reddit API Wrapper for python. Consult with the documentation [here](https://praw.readthedocs.io/en/stable/#getting-started).

## Consult with the documentation

Everything related to the usage of Reddit API is described on the dedicated [web page](https://www.reddit.com/dev/api/).