// modules/acr.bicep — Azure Container Registry
// Ce module crée un registre de conteneurs Azure pour stocker
// l'image Docker de l'application narrative-ai.

@description('Nom du registre de conteneurs Azure (doit être unique globalement)')
param acrName string

@description('Emplacement Azure')
param location string

// Registre de conteneurs Azure
resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: acrName
  location: location
  sku: {
    // Basic : suffisant pour un usage standard, le moins coûteux
    name: 'Basic'
  }
  properties: {
    // Activer l'accès par clé d'administration (nécessaire pour le push depuis GitHub Actions)
    adminUserEnabled: true
  }
}

// ---------------------------------------------------------------------------
// Sorties
// ---------------------------------------------------------------------------

@description('Serveur de connexion ACR (ex: myacr.azurecr.io)')
output acrLoginServer string = acr.properties.loginServer

@description('Nom du registre ACR')
output acrName string = acr.name
