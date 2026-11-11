# Settings and providers
terraform { # This tells terraform how to behave and what tools needed to download
    required_providers { # tells that were going to work with a specific cloud provider
        aws = { 
            source = "hashicorp/aws" # dl official aws plugin made by hashicorp 
            version = "~> 6.0" # use version ≥ 6.0 and < 7.0
        }
    }
}

provider "aws" { # this activates the aws plugin that is configured up there
    region = "ap-southeast-1" # This tells where to build the server
}

# Fetch os 
data "aws_ssm_parameter" "al2023" { # aws_ssm_parameter means go look up info that is already there. so dont create anything (SSM) System Manager
    name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64" # official AWS shortcut path for amazon linux 2023 os
}

# Building the server 
resource "aws_instance" "web" { # means build something new so like aws build EC2 virtual server instance with name of web
    ami = data.aws_ssm_parameter.al2023.value # plugs in the os iD fetch on line 15. So like use the value found from that data
    instance_type = "t3.micro" # this will be the size of the computer. So t3.micro is a small lightweight virtual server 

    tags = { # then add a name in thhe server instance in the aws dashboard.
        Name = "WebServer"
    }
}

output "public_ip" { # when terra finishes building the server. This will print the specific information directly on terminal screen.
    description = "Public IP address of the web server"
    value = aws_instance.web.public_ip # This grab the ip address of the server built 
}