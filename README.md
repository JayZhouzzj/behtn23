## Overview
This small backend uses flask and SQLite to manage user data. 
It uses flask_sqlalchemy to simplify working with data.

## How to run
```docker compose up```

## How to populate db with mock data
With the docker container running, open another terminal, run  
```docker exec api-new python3 dbinit.py``` to use ```mock_userdata.json```  
or  
```docker exec api-new python3 dbinit.py <your mock data file>``` to use your own mock data

## API
### All Users Endpoint
```GET localhost:3000/users/```  
This endpoint returns a list of all users and their information.
### User Information Endpoint
```GET localhost:3000/users/123``` or  
```GET localhost:3000/users/example@email.com```  
This endpoint returns the user data for a specific user.  
### Updating User Data Endpoint
```PUT localhost:3000/users/123```
```PUT localhost:3000/users/example@email.com```
```
{
  email: new email
  skills: [new skills]
  ...
}
```
This endpoint updates an existing user's data. It supports partial updating.
### Skills Endpoints
```GET localhost:3000/skills/?min_frequency=20&max_frequency=30```  
This endpoint returns a list of skills within the frequency range (frequency = how many user has this skill). The two query parameters are optional.  
(All API responses omits ids to be concise)

## Database Design
![htn-userdb](https://user-images.githubusercontent.com/72354860/220510570-64423589-1378-4f18-9702-cea7b73edaae.png)
The database relationship is relatively simple, as shown in the graph. Some notes:
* The design normalizes data into multiple tables. This relational design can reduce data redundancy, improve data integrity and enable better data analysis.
* User and Skill have a many-to-many relationship. UserSkill is a helper table for this.
* Assume emails are unique because users should use emails as usernames to register. This also allows us to call endpoints with emails to identify users quickly. 
* The implementation uses relationships and backrefs to avoid manually joining tables and writing subqueries. 
* The flask implementation uses [event listeners](https://github.com/JayZhouzzj/behtn23/blob/0b7c679cac84c35e82a91a4c52f03ffe3d7b0c5f/main.py#L67-L76) to update frequency for each skill. This is because there should be much more reads than writes of skill frequency. In testing, with only around 1000 users, if the db re-calculates frequency each time, the endpoint to filter skills by frequency will timeout.

## Testing
pytest should be incorporated in the future. For now, you can test it manually by running the docker container and calling the endpoints.  
You can import ```test/insomnia_env.json``` into [insomnia](https://insomnia.rest/) to get my pre-configured endpoints for testing.  
You can also view data directly using [DB Browser for SQLite](https://sqlitebrowser.org/).
