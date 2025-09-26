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

deny[msg] {
  input.kind == "Deployment"
  input.spec.template.spec.hostPID == true
  msg := "hostPID is not allowed"
}

deny[msg] {
  input.kind == "Deployment"
  input.spec.template.spec.hostIPC == true
  msg := "hostIPC is not allowed"
}

# Only allow images from ghcr.io
deny[msg] {
  input.kind == "Deployment"
  some i
  not re_match("^ghcr\\.io/", input.spec.template.spec.containers[i].image)
  msg := "Images must come from ghcr.io"
}

# Require imagePullPolicy IfNotPresent
deny[msg] {
  input.kind == "Deployment"
  some i
  input.spec.template.spec.containers[i].imagePullPolicy != "IfNotPresent"
  msg := "imagePullPolicy must be IfNotPresent"
}

deny[msg] {
  input.kind == "Deployment"
  some i
  not input.spec.template.spec.containers[i].livenessProbe
  msg := "livenessProbe is required"
}

deny[msg] {
  input.kind == "Deployment"
  some i
  not input.spec.template.spec.containers[i].readinessProbe
  msg := "readinessProbe is required"
}

deny[msg] {
  input.kind == "Deployment"
  not input.spec.template.spec.securityContext.runAsUser
  msg := "runAsUser must be set"
}

deny[msg] {
  input.kind == "Deployment"
  input.spec.template.spec.securityContext.runAsUser < 10000
  msg := "runAsUser must be >= 10000"
}

# Drop all capabilities
deny[msg] {
  input.kind == "Deployment"
  some i
  not input.spec.template.spec.containers[i].securityContext.capabilities
  msg := "Container must drop all capabilities"
}

deny[msg] {
  input.kind == "Deployment"
  some i
  input.spec.template.spec.containers[i].securityContext.capabilities.drop[_] != "ALL"
  msg := "Capabilities drop must include ALL"
}

# Require minimum terminationGracePeriodSeconds
deny[msg] {
  input.kind == "Deployment"
  input.spec.template.spec.terminationGracePeriodSeconds < 10
  msg := "terminationGracePeriodSeconds must be >= 10"
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


