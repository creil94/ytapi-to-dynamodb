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

variable "queue_arn" {
  description = "information about the queue that is filled by the provisioner"
  type = string
  default = null
}

variable "event_rule_arn" {
  description = "information about the event_rule that is filled by the provisioner"
  type = string
  default = null
}

variable "inline_policies" {
  type = list(object({
    name: string
    actions: list(string)
    resources: list(string)
  }))
}

variable "environment_vars" {
  type = map(string)
}