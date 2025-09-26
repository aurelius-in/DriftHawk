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

deny[msg] {
  input.kind == "Deployment"
  input.spec.template.spec.containers[_].securityContext.privileged == true
  msg := "Privileged containers are not allowed"
}

deny[msg] {
  input.kind == "Service"
  input.spec.type == "NodePort"
  msg := "NodePort services are not allowed"
}

deny[msg] {
  not input.spec.template.spec.containers[_].resources.requests
  msg := "Require resource requests"
}

deny[msg] {
  not input.metadata.namespace
  msg := "Namespace must be set"
}

deny[msg] {
  input.metadata.namespace == "default"
  msg := "Default namespace is not allowed"
}

deny[msg] {
  input.kind == "Deployment"
  not input.spec.template.spec.securityContext.runAsNonRoot
  msg := "Deployment must set runAsNonRoot=true"
}


