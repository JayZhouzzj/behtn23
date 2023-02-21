## How to run
```docker compose up```

## How to populate db with mock data
With the docker container running, open another terminal, run  
```docker exec api-new python3 dbinit.py``` to use ```mock_userdata.json```  
or  
```docker exec api-new python3 dbinit.py <your mock data file>``` to use your own mock data
