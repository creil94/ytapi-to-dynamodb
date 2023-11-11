
# Youtube-API-DynamoDB
[![Test&Deploy](https://github.com/creil94/ytapi-dynamodb/actions/workflows/deployment.yml/badge.svg?branch=main)](https://github.com/creil94/ytapi-dynamodb/actions/workflows/deployment.yml)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

Small example implementation which regularly retrieves data from the youtube-api and stores them in AWS DynamoDB through a combination of AWS-SQS and AWS-Lambda.

## Architecture
![architecture diagram](assets/architecture_diagram.jpg)

## Features
- highly scalable pipeline to extract information from yt-api
- validation of data flow with pydantic
- Infrastructure as Code with terraform
- automated testing and deployment with github actions
- high test coverage

