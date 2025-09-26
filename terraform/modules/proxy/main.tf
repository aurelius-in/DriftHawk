terraform { required_version = ">=1.6.0" }

resource "null_resource" "proxy" {
  triggers = { provisioned = timestamp() }
}

output "proxy_id" { value = "mock-proxy" }


