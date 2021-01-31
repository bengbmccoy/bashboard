#Welcome to my bashboard.fyi website repo!

Currently the site is minimal with only a landing page and a raw nfl dashboard, however I have big plans for the website to eventually host a number of my personal projects.

The current version of the website is an application written in python, using the Flask framework. It then is packaged into a Docker container and run using google cloud run and hosted by google firebase.

#To build the container:
$ docker build -t bashboard-image .

#To submit the build to gcloud:
$ gcloud builds submit --tag gcr.io/bashboard-40f7b/bashboard-image

#To deploy container to gcloud:
$ gcloud run deploy --image gcr.io/bashboard-40f7b/bashboard-image

#To deploy the hosting:
$ firebase deploy --only hosting
