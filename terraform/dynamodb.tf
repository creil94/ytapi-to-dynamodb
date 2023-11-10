resource "aws_dynamodb_table" "videos-dynamodb-table" {
  name           = "Videos"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "video_id"
  range_key      = "identifier"

  attribute {
    name = "video_id"
    type = "S"
  }

  attribute {
    name = "identifier"
    type = "S"
  }

  attribute {
    name = "entity_type"
    type = "S"
  }

  global_secondary_index {
    name            = "entity-type-identifier"
    hash_key        = "entity_type"
    range_key       = "identifier"
    write_capacity  = 5
    read_capacity   = 5
    projection_type = "ALL"
  }

  deletion_protection_enabled = true
}