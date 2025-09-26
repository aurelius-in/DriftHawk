terraform {
  required_version = ">=1.6.0"
  required_providers {
    null = { source = "hashicorp/null" }
  }
}

module "ipam" {
  source     = "../../modules/ipam"
  cidr_block = "10.20.0.0/16"
}

module "lb" {
  source     = "../../modules/lb"
  depends_on = [module.ipam]
}

module "proxy" {
  source     = "../../modules/proxy"
  depends_on = [module.lb]
}

module "openshift" {
  source     = "../../modules/openshift"
  depends_on = [module.proxy]
}


