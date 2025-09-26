terraform { required_version = ">=1.6.0" }

variable "cidr_block" { type = string }

resource "null_resource" "ipam" {
  triggers = { cidr = var.cidr_block }
}

output "cidr" { value = var.cidr_block }


