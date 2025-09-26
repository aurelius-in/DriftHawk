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

deny[msg] {
  input.kind == "Deployment"
  input.spec.template.spec.volumes[_].hostPath
  msg := "hostPath volumes are not allowed"
}

deny[msg] {
  input.kind == "Deployment"
  input.spec.template.spec.hostNetwork == true
  msg := "hostNetwork is not allowed"
}

# Containers must not allow privilege escalation
deny[msg] {
  input.kind == "Deployment"
  input.spec.template.spec.containers[_].securityContext.allowPrivilegeEscalation == true
  msg := "allowPrivilegeEscalation must be false"
}

# Containers must use readOnlyRootFilesystem
deny[msg] {
  input.kind == "Deployment"
  not input.spec.template.spec.containers[_].securityContext.readOnlyRootFilesystem
  msg := "readOnlyRootFilesystem must be set to true"
}

# Pod must set seccompProfile
deny[msg] {
  input.kind == "Deployment"
  not input.spec.template.spec.securityContext.seccompProfile
  msg := "Pod securityContext.seccompProfile must be set"
}

# Must not use default service account
deny[msg] {
  input.kind == "Deployment"
  input.spec.template.spec.serviceAccountName == "default"
  msg := "Default service account is not allowed"
}

# ServiceAccount token should not be automounted at pod level
deny[msg] {
  input.kind == "Deployment"
  not input.spec.template.spec.automountServiceAccountToken
  msg := "automountServiceAccountToken must be false"
}


