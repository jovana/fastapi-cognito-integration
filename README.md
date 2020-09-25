# Cognito Integration for FastAPI
Using the AWS Cognito authentication in FastAPI.
- FastAPI: https://fastapi.tiangolo.com/
- Terraform: https://www.terraform.io/
- AWS Cognito: https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html

# DISCLAIMER
This project is only to help you understand and give you a possible authentication integration to learn what is possible. This is created with my own vision on how to achieve a backend authentication using AWS Cognito.

You can use this code if you like, but before using it review the code carefully. Do not going to use this in production without validating all aspects of this code.


## Features in the integration
Features:
- Integrate your FastAPI project on Cognito Authentication for using JWK-tokens.
- Manage sending mail notifications yourself (instead of letting Cognito sending mail).
- Manage users in your own database, but let the authentication manage by Cognito.
- Save the cognito userid into your own database toghter with the user information.

### Setup Cognito
In the folder ```terraform``` are basic scripts to deploy basic Cognito setup.
Run the following commands (make sure you have installed Terraform https://learn.hashicorp.com/collections/terraform/aws-get-started)


Enter into the directory:
```cd terraform```

Initialization terraform:
```terraform init```

Check the settings and if there are any mistakes:
```terraform plan```

Apply the settings to AWS:
```terraform apply``` (confirm by enter Yes)
After terraform is finised you got some output in green details. This information you need to take over into your .env file

### Setup authentication in Fast-API
Adding .env file in the root of your project (rename the example.env to .env).
Enter the correct values retrived from Cognito (Or terraform scripts).

### Running this example code
```
pip install -r requirements.txt
python main.py
```

Open your browser to http://locahost:8080/docs to start.
