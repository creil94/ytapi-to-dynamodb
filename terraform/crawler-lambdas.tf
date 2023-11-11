module "product-price-crawler" {
  source                = "./lambdas/crawler-lambda"
  container_entry_point = "crawler/statistics.lambda_handler"
  environment_vars = {
    TABLE = aws_dynamodb_table.videos-dynamodb-table.name
  }
  image_uri = "${aws_ecr_repository.lambda-functions-ecr.repository_url}:latest"
  inline_policies = [{
    name : "videos-dynamodb-access"
    actions : ["dynamodb:PutItem"]
    resources : [aws_dynamodb_table.videos-dynamodb-table.arn]
    }, {
    name : "sqs-trigger"
    actions : [
      "sqs:ReceiveMessage",
      "sqs:GetQueueAttributes",
      "sqs:DeleteMessage"
    ]
    resources : [aws_sqs_queue.video-statistics-queue.arn]
    }
  ]
  name      = "video-statistics-crawler"
  queue_arn = aws_sqs_queue.video-statistics-queue.arn
}