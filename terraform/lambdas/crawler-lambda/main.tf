resource "aws_iam_role" "crawler-lambda-role" {
  name                = "${var.name}-crawler-lambda-role"
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
}

resource "aws_iam_role_policy" "test_policy" {
  for_each = {
    for index, inline_policy in var.inline_policies:
    inline_policy.name => inline_policy
  }
  name = each.value.name
  role = aws_iam_role.crawler-lambda-role.id

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = each.value.actions
        Effect   = "Allow"
        Resource = each.value.resources
      },
    ]
  })
}

resource "aws_iam_role_policy" "x-ray-policy" {
  name = "x-ray-policy"
  role = aws_iam_role.crawler-lambda-role.id

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "xray:PutTraceSegments",
          "xray:PutTelemetryRecords"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_lambda_function" "crawler-lambda" {
  function_name = "cl-${var.name}"
  role          = aws_iam_role.crawler-lambda-role.arn
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

resource "aws_lambda_event_source_mapping" "sqs-trigger-crawler" {
  count = var.queue_arn == null ? 0 : 1
  event_source_arn                   = var.queue_arn
  function_name                      = aws_lambda_function.crawler-lambda.arn
  batch_size                         = 10
  maximum_batching_window_in_seconds = 5
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  count = var.event_rule_arn == null ? 0 : 1
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.crawler-lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = var.event_rule_arn
}