# Setup the provider and the region: AWS eu-west-1 in this case
provider "aws" {
  region = var.region
}

# For the remote state, setup the remote S3 bucket.
terraform {
  backend "s3" {
    bucket = "<S3-BUCKET-NAME>"
    key    = "terraform-states/<FOLDER_NAME>/terraform.tfstate"
    region = var.region
  }
}
