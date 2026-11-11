Personal notes from building this project: Docker, API testing, and Terraform commands I use.

# Docker

uses the existing image.

```bash
docker compose up
```

While with --build forces it to rebuild the image first

```bash
docker compose up --build
```

just stop and remove the containers and network.

```bash
docker compose down
```

Removes the volumes so it resets the db

```bash
docker compose down -v
```

Run the test created on test/

```bash
docker compose run --rm web env PYTHONPATH=. pytest
```

Runs ruff check

```bash
docker compose run --rm web ruff check .
```

tips for future for yml files like docker-compose.yml add a healthcheck for db or other instance that will run first so that there will be a wait before connecting.

# curl for API (PowerShell / Bash)

if bash use "\"
if powershell then use "`"
remember no https
Get

```bash
curl -X GET "http://localhost:5000/api/books"
```

Add

```bash
curl -X POST "http://localhost:5000/api/books" \
-H "Content-Type: application/json" \
-d '{"Name":"", "Year":"", "Author":""}'
```

Update

```bash
curl -X PUT "http://localhost:5000/api/books/1" \
-H "Content-Type: application/json" \
-d '{"Name":"", "Year":"", "Author":""}'
```

Delete

```bash
curl -X DELETE "http://localhost:5000/api/books/1"
```

# Terraform

Look into infra -> main.tf there is the configuration

```hcl
# Settings and providers
terraform { # tells terraform how to behave and what tools needed to download
    required_providers { # what specific cloud provider
        aws = {
            source = "hashicorp/aws" # dl official aws plugin made by hashicorp
            version = "~> 6.0" # use version ≥ 6.0 and < 7.0
        }
    }
}

provider "aws" { # activates the aws plugin
    region = "ap-southeast-1" # This tells where to build the server
}

# Fetch os
data "aws_ssm_parameter" "al2023" { # aws_ssm_parameter means go look up info that is already there. so dont create anything (SSM) System Manager
    name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64" # official AWS shortcut path for amazon linux 2023 os
}

# Building the server
resource "aws_instance" "web" { # builds a new EC2 virtual server named web
    ami = data.aws_ssm_parameter.al2023.value # uses the AMI ID from the al2023 data block above.
    instance_type = "t3.micro" # use t3.micro. its a small lightweight virtual server

    tags = { # add a name in the server instance in the aws dashboard.
        Name = "WebServer"
    }
}

output "public_ip" { # This will print the specific information directly on terminal screen.
    description = "Public IP address of the web server"
    value = aws_instance.web.public_ip # This grab the ip address of the server built
}
```

to run terraform

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply <- this is when the meter will start running
```

after testing is done

```
terraform destroy <- this is to stop the meter
```

Check the EC2 console (Singapore): no instances Running.

Always remember
data = read existing info
resource = create something
output = print a value after apply
