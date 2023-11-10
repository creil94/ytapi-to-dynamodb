resource "aws_sqs_queue" "video-statistics-queue" {
  name                      = "video-statistics-queue"
  message_retention_seconds = 120
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.video-statistics-deadletter-queue.arn
    maxReceiveCount     = 2
  })
}

resource "aws_sqs_queue" "video-statistics-deadletter-queue" {
  name = "video-statistics-deadletter-queue"
}