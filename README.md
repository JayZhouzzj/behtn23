## How to run
```docker compose up```

## How to populate db with mock data
With the docker container running, open another terminal, run  
```docker exec api-new python3 dbinit.py``` to use ```mock_userdata.json```  
or  
```docker exec api-new python3 dbinit.py <your mock data file>``` to use your own mock data
![htn-userdb drawio(1)](https://user-images.githubusercontent.com/72354860/220491256-731ffcc2-ee29-4fe1-b911-95e9afc98465.png)
