#Welcome to my bashboard.fyi website repo!

Currently the site is minimal with only a landing page and a raw nfl dashboard, however I have big plans for the website to eventually host a number of my personal projects.

The current version of the website is an application written in python, using the Flask framework. It then is packaged into a Docker container and run using google cloud run and hosted by google firebase.

#To run the app locally:
$ python /server/app.py

## Full deployment to website:

#To build the container:
$ docker build -t bashboard-image .

#To submit the build to gcloud:
$ gcloud builds submit --tag gcr.io/bashboard-40f7b/bashboard-image

#To deploy container to gcloud:
$ gcloud run deploy --image gcr.io/bashboard-40f7b/bashboard-image

#To deploy the hosting (dont think this is needed):
$ firebase deploy --only hosting

#TODO:
- Clean up the landing/index page
- Clean up the dashboard page
- - Add titles to the graphs, clean up the labels
- - Get some kind of layout properly organised
- Create a diagram showing the flow of the app
- Add the rest of the backend operations (i.e. data, data models, aggregation etc.)
- Add an error handler route
