auth2_python_django
===================

Auth2 sample project for python and django is provided in the hope that it'll be useful to create your own code.

Here is the demo of the sample on youtube-

<a href='http://www.youtube.com/watch?v=0x4n5egwLXk'>Auth2 Sample Demo</a>

Before you can use the code please visit <a href='http://auth2.com'>http://auth2.com</a> and create an account and then from developer page create an application. Then you can use the application key/secret pair with this sample.

<h3>Running the sample</h3>
Download the code and change following 4 lines of code with appropriate values. You can remove the error raising part. It is just to remind you about the required change.

<code>
AUTH2_API_KEY = "your api key here"

AUTH2_API_SECRET = "your api secret here"


if AUTH2_API_KEY == "your api key here":
    raise ValueError("You forgot to set your API Key")
    
</code>

Then sync the db from the project directory (manage.py syncdb) nad run the server and test your site.

<b>Please note that you need two phones around to test the sample. The phone you use for your application can not be used to call the API. This is becasue the application phone will be sent as caller ID who is receiving. You can not call yourself.</b>

