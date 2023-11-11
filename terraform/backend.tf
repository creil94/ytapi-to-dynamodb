terraform {
  backend "s3" {
    bucket = "ytapi-dynamodb-tf-state"
    key    = "global/terraform.tfstate"
    region = "eu-central-1"
  }
}