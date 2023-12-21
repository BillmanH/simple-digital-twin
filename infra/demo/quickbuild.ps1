$resourceGroupName = "simple_digital_twin"
az login --tenant <your tenant>

az deployment group create --resource-group $resourceGroupName --template-file "infra/demo/template.json" --parameters "infra/demo/parameters.json"
