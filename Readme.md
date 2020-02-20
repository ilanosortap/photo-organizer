upload image and search api

-> Tools used : Flask in the backend, bootstrap in frontend and Mongodb as the database

To begin with, I researched different ways of implementing this API. I finally settled on using the Python flask framework due to my familiarity with python and a good learning 
curve that comes with it. I used mongo db as my database as it can handle unstructured data and can queries can be done using simple json string.

I made only one page for the UI instead of 2 separate pages for upload and search each, since I thought its better for the UX part, as a user myself I wouldnt like to navigate between 
different pages to just upload something.

I could'nt however implement the description part of the search api as I wasn't able to find a good external library to do it, and the or query for tags as mongodb doesnt have 
a surefire way of doing it in the backend (in retrospect, I should have used a MySQL db to make my life easier, but I was too far down the road before I realised this. From next time
on, I should probably research a bit more before deciding and sticking to a database)

For the upload part, I fetched the image using POST request and compressed and stored them using the Pillow library, I know I was supposed to do 2 sizes of each image but I am using 
a free hosting platform and they usually have a cap on storage so didnt want to take a chance on failure during deployment.

I added a little exception handling as well so that the page would notify the user if they haven't selected any image for uploading, or their search query is not in the right format.

This was good learning experience, and even if this doesnt move forward I am glad i tried out something new.