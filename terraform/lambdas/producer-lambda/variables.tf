variable "name" {
  description = "unique name that identifies the queue provisioner"
  type = string
}

variable "image_uri" {
  description = "image-uri for the lambda function"
  type = string
}

variable "container_entry_point" {
  description = "entry point for the container of the lambda function"
  type = string
}

variable "table" {
  description = "information about the table from which the queue is filled"
  type = object({
    arn: string
    name: string
    index_arn: string
  })
}

variable "queue" {
  description = "information about the queue that is filled by the provisioner"
  type = object({
    arn: string
    url: string
  })
}

variable "schedule_expression" {
  description = "expression how often the provisioner is triggered"
  type = string
}