
# YoutubeAPI-to-DynamoDB
[![Test&Deploy](https://github.com/creil94/ytapi-dynamodb/actions/workflows/deployment.yml/badge.svg?branch=main)](https://github.com/creil94/ytapi-dynamodb/actions/workflows/deployment.yml)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

Small example implementation which regularly retrieves data from the youtube-api and stores them in AWS DynamoDB through a combination of AWS-SQS and AWS-Lambda.

## Architecture
The core idea of this architecture is to create a scalable solution to retrieve data from the youtube-api for a high number of videos. Therefore, a distributed architecture has been created with a "producer" which adds all the relevant video_ids to a queue. All these video_ids are batched (e.g. batches of 5 video_ids) and processed by the "statistics crawler function". This component can run in parallel. Furthermore, through the SQS-queue there is an automatic retry and eventually failed records will end up in a deadletter queue to investigate the errors.

![architecture diagram](assets/architecture_diagram.jpg)

## Features
- highly scalable pipeline to extract information from yt-api
- validation of data flow with pydantic
- automatic retry and deadletter queue for failed crawling runs
- single-table dynamodb design
- Infrastructure as Code with terraform
- automated testing and deployment with github actions
- high test coverage
- dependabot integration to receive notification for package updates and automatically open PRs

