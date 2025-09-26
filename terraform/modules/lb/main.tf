terraform { required_version = ">=1.6.0" }

resource "null_resource" "lb" {
  triggers = { provisioned = timestamp() }
}

output "lb_id" { value = "mock-lb" }


