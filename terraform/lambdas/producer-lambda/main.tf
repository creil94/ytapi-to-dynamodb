terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.7.0"
    }
  }
}

resource "aws_iam_role" "queue-provisioner-lambda-role" {
  name                = "${var.name}-queue-provisioner-lambda-role"
  assume_role_policy  = <<EOF
  {
   "Version": "2012-10-17",
   "Statement": [
     {
       "Action": "sts:AssumeRole",
       "Principal": {
         "Service": "lambda.amazonaws.com"
       },
       "Effect": "Allow",
       "Sid": ""
     }
   ]
  }
EOF
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "${var.name}-queue-provisioner-lambda-dynamodb"
    policy = data.aws_iam_policy_document.queue-provisioner-lambda-dynamodb.json
  }
  inline_policy {
    name   = "${var.name}-queue-provisioner-lambda-sqs"
    policy = data.aws_iam_policy_document.queue-provisioner-lambda-sqs.json
  }
  inline_policy {
    name   = "${var.name}-queue-provisioner-x-ray"
    policy = data.aws_iam_policy_document.queue-provisioner-x-ray.json
  }
}


resource "aws_lambda_function" "queue-provisioner-lambda" {
  function_name = "qp-${var.name}"
  role          = aws_iam_role.queue-provisioner-lambda-role.arn
  timeout       = 30
  memory_size   = 128
  image_uri     = var.image_uri
  architectures = ["arm64"]
  image_config {
    command = [var.container_entry_point]
  }
  package_type = "Image"
  environment {
    variables = var.environment_vars
  }
  tracing_config {
    mode = "Active"
  }
}

data "aws_iam_policy_document" "queue-provisioner-lambda-dynamodb" {
  statement {
    actions = [
      "dynamodb:Query"
    ]
    resources = [
      var.table.arn,
      var.table.index_arn
    ]
  }
}

data "aws_iam_policy_document" "queue-provisioner-lambda-sqs" {
  statement {
    actions = [
      "sqs:SendMessage"
    ]
    resources = [var.queue.arn]
  }
}

data "aws_iam_policy_document" "queue-provisioner-x-ray" {
  statement {
    actions = [
      "xray:PutTraceSegments",
      "xray:PutTelemetryRecords"
    ]
    resources = ["*"]
  }
}


resource "aws_cloudwatch_event_rule" "schedule-expression" {
  name                = "${var.name}-schedule-exp"
  schedule_expression = var.schedule_expression
}

resource "aws_cloudwatch_event_target" "event-target" {
  rule      = aws_cloudwatch_event_rule.schedule-expression.name
  target_id = "check_foo"
  arn       = aws_lambda_function.queue-provisioner-lambda.arn
}

resource "aws_lambda_permission" "allow-cloudwatch-to-call-provisioner-lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.queue-provisioner-lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule-expression.arn
}