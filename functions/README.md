# Functions
This folder contains the code of the lambda functions and their respective connectors to third party services and models to validate the data flow.
## Content
In the following section the content of this folder is shortly explained.
### connectors
This folder mainly contains helper functionalities to wrap connections to third party-services like dynamodb, sqs and the youtube api-
```
├── connectors
│   ├── dynamodb.py
│   ├── sqs.py
│   ├── yp_api.py
```
### crawler
This folder contains the code for the crawler function
```
├── crawler
│   ├── statistics.py
```
### models
This folder contains pydantic models which are used to cast the input to types and also validate the data.
```
├── models
│   ├── dynamodb.py
│   ├── video_event.py
```
### producer
This folder contains the code for the producer function
```
├── producer
│   ├── statistics.py
```
