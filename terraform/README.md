# Terraform
In this folder the infrastructure in AWS is created and the docker image for the lambda function is built via terraform.
## Usage
1. (optional) setup backend.tf as follows:
```hcl
terraform {
  backend "s3" {
    bucket = "[YOUR-BUCKET]"
    key    = "[YOUR-KEY]/terraform.tfstate"
    region = "eu-central-1"
  }
}
```
2. To use the functionality of pushing the lambda image directly to ECR you need to install the [amazon-ecr-credentials-helper](https://github.com/awslabs/amazon-ecr-credential-helper).
3. Run `terraform init`

4. Run `terraform plan`
5. Run `terraform apply`
* You will be prompted for your YT_API_KEY. Either always fill it in or store the key in the env variable `TF_VAR_YT_APi_KEY`.
