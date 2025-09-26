package policy.k8s

deny[msg] {
  input.kind == "Deployment"
  re_match(":latest$", input.spec.template.spec.containers[_].image)
  msg := "Disallow :latest tags"
}

deny[msg] {
  not input.metadata.annotations["cosign.sigstore.dev/verified"]
  msg := "Image must be cosign-verified"
}

deny[msg] {
  not input.spec.template.spec.containers[_].resources.limits
  msg := "Require resource limits"
}


