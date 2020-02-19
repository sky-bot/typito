Stack Used:
1) FrontEnd: React, BootStrap 
2) BackEnd: Python Flask (I would have preferred Django, but it was Restricted)
3) Image Storage: Amazon S3
4) Data Storage: SQLite(with ORM SQLAlchemy)

APIs:
1) Upload API
2) Search API
3) Amazon Rekognition API( for getting tags )

Challenges Faced:
1) Permissions for all Amazon related things like (S3 Storage, Rekognition API).
2) Working for first time in React(due to which assignment gets delayed)
3) Dealing with different aspect ratio.

Db Schema Design:
1) logid ( primary key )
2) Url ( Unique constraints )
3) Day ( date )
4) Month ( Month )
5) Year ( Year )
6) Date (date time object)
7) Description

Flow of Upload APIs:
1) Getting the file from request
2) Storing the images in S3 and getting the urls
3) Calling the Amazon Rekognition APIs and get the tags
4) Storing in the Db

Flow of Search APIs:
1) Get the search key and get whatever constraints given in search( date, from, to, tags, desc)
2) Forming the SQL query based on certain conditions
3) Send the result

Thought of using but not implemented:
1) Presigned Url(giving image Permissions for some period of time).
2) Amazon RDS for data Storage for Scaling.
3) Refresing page when Upload image takes place.
3) Reduce the size of image before uploading.
4) Zipping of request-response of getting faster response 
4) Full text search shoul be implemented
5) Recent 30 images can be stored in Redis

What I Learn:
Learn a lot about React
How to use SQLAlchemy.
IAM Roles(AWS)
How to use Amazon S3 bucket, Rekognition API
How to deploy React App with Amazon S3
Presigned Url.


About Assignment:
Modifications I made
1) Instead of creating button for loading more I have created infinite scrolling( on scroll
   it will call API to load more)
2) Instead of giving option for user to add tags, I am calling Amazon Rekognition API,
   to give me tags. Amazon Rekognition API do object detection and gives object names with
   confidence value, so I am taking the top 3 confidence value's tags.
3) If user select multiple images, than same description is applied for all the images.

Vulnerabilities:
1) Form validation not done.
2) Many if conditions in search APIs(not recommended) but can't think of better solution
   to satisfy the search api constraints.
3) On upload you have to refresh the app to see the change reflected (not recommended)
4) Aspect ratio not handled.
5) Seach Api only works if search query is as per the assignment doc.
P.S: for date query My API won't work for these two types 
            - date:03-2016
            - date:2016`
    you should provide all three it can be *-12-*, *-*-2020