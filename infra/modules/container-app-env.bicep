// modules/container-app-env.bicep — Azure Container Apps Environment
// Ce module crée l'environnement partagé pour les Container Apps.
// Un environnement regroupe plusieurs Container Apps et gère
// la mise en réseau, la journalisation et l'évolutivité.

@description('Nom de l\'environnement Container Apps')
param containerAppEnvName string

@description('Emplacement Azure')
param location string

// Espace de travail Log Analytics pour la journalisation
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'log-${containerAppEnvName}'
  location: location
  properties: {
    sku: {
      // PerGB2018 : facturation à la consommation (le moins coûteux)
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// Environnement Azure Container Apps
resource containerAppEnv 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: containerAppEnvName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Sorties
// ---------------------------------------------------------------------------

@description('Identifiant de ressource de l\'environnement Container Apps')
output containerAppEnvId string = containerAppEnv.id
