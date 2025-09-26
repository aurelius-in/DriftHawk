Param(
  [string]$Env = "dev"
)

Push-Location "terraform/envs/$Env"
terraform init -input=false -upgrade | Out-Null
terraform graph | dot -Tpng > "../../../artifacts/$Env-graph.png"
Write-Output "wrote artifacts/$Env-graph.png"
Pop-Location


