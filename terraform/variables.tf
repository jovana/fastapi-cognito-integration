variable "application_name" {
  description = "The name of your application"
  type        = string
}

variable "stage" {
  description = "Applicaiton environment (dev, rc, prod)"
  type        = string
  default     = "dev"
}

variable "region" {
  description = "Set the region"
  type        = string
  default     = "eu-west-1"
}
