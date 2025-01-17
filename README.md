# Image Classification API

A web api that uses the [CLIP](https://github.com/openai/CLIP) model and a list of categories (see `app/image_service.py`) to classify images.

It runs in a docker container with a volume for the model. This has been tested to run in an Azure Web App for Containers (linux) and performance is decent (500kb images < 0.4sec) on P0v3 (195 ACU/vCPU, 1vCPU, 4GB memory, AUD$73).

## Usage

Requires docker.

### Local development
For local development, you can use DevContainers in VS Code (requires Dev Containers vscode extension).

To run locally without an IDE:
```powershell
docker build --tag imgdet:latest .
docker run --rm -p 8080:80 -v C:/dev/data:/volume imgdet
```

There's a jupyter notebook in the test folder that can be used for testing.

### Azure
For deployment to an Azure Web App for Containers, these az cli commands can help:
Build image and push to container registry
```powershell
az acr build --registry myregistry --image myregistry.azurecr.io/imgdet:latest .
```
Get web app to use latest container. Hacky (to avoid thinking about versions).
```powershell
az webapp config container set --name mywebapp --resource-group myresourcegroup --container-image-name myregistry.azurecr.io/imgdet:0.0.999
az webapp config container set --name mywebapp --resource-group myresourcegroup --container-image-name myregistry.azurecr.io/imgdet:latest
```