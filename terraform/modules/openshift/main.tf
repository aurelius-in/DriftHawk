terraform { required_version = ">=1.6.0" }

resource "null_resource" "openshift" {
  triggers = { provisioned = timestamp() }
}

output "cluster_id" { value = "mock-ocp" }


