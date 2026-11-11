terraform {
    required_providers { 
        aws = { 
            source = "hashicorp/aws"
            version = "~> 6.0"
        }
    }
}

provider "aws" {
    region = "ap-southeast-1"
}

data "aws_ssm_parameter" "al2023" {
    name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

resource "aws_instance" "web" {
    ami = data.aws_ssm_parameter.al2023.value 
    instance_type = "t3.micro" 

    tags = {
        Name = "WebServer"
    }
}

output "public_ip" {
    description = "Public IP address of the web server"
    value = aws_instance.web.public_ip
}