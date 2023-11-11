terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.7.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "eu-central-1"
}

data "aws_caller_identity" "current" {}

provider "docker" {
  registry_auth {
    address     = "${data.aws_caller_identity.current.account_id}.dkr.ecr.eu-central-1.amazonaws.com"
    config_file = "./config.json"
  }
}