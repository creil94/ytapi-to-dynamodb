module "comments-crawler-queue-provisioner" {
  source                = "./lambdas/producer-lambda"
  container_entry_point = "producer/statistics.lambda_handler"
  image_uri = "${aws_ecr_repository.lambda-functions-ecr.repository_url}@${docker_registry_image.lambda-image-remote.sha256_digest}"
  name                  = "video-crawler"
  queue = {
    arn : aws_sqs_queue.video-statistics-queue.arn
    url : aws_sqs_queue.video-statistics-queue.url
  }
  schedule_expression = "cron(*/10 * * * ? *)"
  table = {
    arn : aws_dynamodb_table.videos-dynamodb-table.arn
    name : aws_dynamodb_table.videos-dynamodb-table.name
    index_arn : "${aws_dynamodb_table.videos-dynamodb-table.arn}/index/entity-type-identifier"
  }
  environment_vars = {
    VIDEO_TABLE = aws_dynamodb_table.videos-dynamodb-table.name
    QUEUE_URL = aws_sqs_queue.video-statistics-queue.url
  }
}