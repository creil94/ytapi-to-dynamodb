resource "aws_ecr_repository" "lambda-functions-ecr" {
  name = "lambda-functions"
}


resource "aws_ecr_lifecycle_policy" "expire-lifecycle-policy" {
  repository = aws_ecr_repository.lambda-functions-ecr.name

  policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Expire images older than 1 days",
            "selection": {
                "tagStatus": "untagged",
                "countType": "sinceImagePushed",
                "countUnit": "days",
                "countNumber": 1
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}