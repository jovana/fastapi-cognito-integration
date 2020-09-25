// create the Cognito User Pool

resource "aws_cognito_user_pool" "this" {
  name                = "${var.application_name}-${var.stage}-user-pool"
  username_attributes = ["email"]
  username_configuration {
    case_sensitive = false
  }
  password_policy {
    minimum_length                   = 8
    require_lowercase                = true
    require_numbers                  = true
    require_symbols                  = false
    require_uppercase                = true
    temporary_password_validity_days = 1
  }
  admin_create_user_config {
    allow_admin_create_user_only = true
  }
}

resource "aws_cognito_user_pool" "this-rc" {
  name                = "${var.application_name}-rc-user-pool"
  username_attributes = ["email"]
  username_configuration {
    case_sensitive = false
  }
  password_policy {
    minimum_length                   = 8
    require_lowercase                = true
    require_numbers                  = true
    require_symbols                  = false
    require_uppercase                = true
    temporary_password_validity_days = 1
  }
  admin_create_user_config {
    allow_admin_create_user_only = true
  }
}

resource "aws_cognito_user_pool_client" "this" {
  name                         = "${var.application_name}-${var.stage}-app-clients"
  user_pool_id                 = aws_cognito_user_pool.this.id
  supported_identity_providers = ["COGNITO"]
  generate_secret              = true // using javascripts SDK, please disabled
  explicit_auth_flows          = ["ADMIN_NO_SRP_AUTH"]
  refresh_token_validity       = 1

  // using javascript SDK, below lines need to enable
  # allowed_oauth_flows_user_pool_client = true
  # allowed_oauth_flows = ["client_credentials"]
  # allowed_oauth_scopes = aws_cognito_resource_server.this.scope_identifiers
}


resource "aws_cognito_identity_pool" "this" {
  identity_pool_name               = "${var.application_name} ${var.stage} identity pool"
  allow_unauthenticated_identities = false
  cognito_identity_providers {
    client_id               = aws_cognito_user_pool_client.this.id
    provider_name           = aws_cognito_user_pool.this.endpoint
    server_side_token_check = false
  }
}

output "aws_cognito_user_pool" {
  sensitive = false
  value = {
    arn : aws_cognito_user_pool.this.arn,
    endpoint : aws_cognito_user_pool.this.endpoint,
    id : aws_cognito_user_pool.this.id
  }
}


output "aws_cognito_app_client_id" {
  value = aws_cognito_user_pool_client.this.id
}
