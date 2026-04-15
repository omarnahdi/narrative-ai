// modules/container-app.bicep — Azure Container App
// Ce module crée la Container App qui héberge l'application narrative-ai.
// Il configure le conteneur, les variables d'environnement (secrets inclus),
// et l'accès public via HTTPS sur le port 7777.

@description('Nom de la Container App')
param containerAppName string

@description('Emplacement Azure')
param location string

@description('Identifiant de l\'environnement Container Apps')
param containerAppEnvId string

@description('Serveur de connexion ACR (ex: myacr.azurecr.io)')
param acrLoginServer string

@description('Nom du registre ACR')
param acrName string

@description('Nom complet de l\'image Docker (ex: narrative-ai:latest)')
param imageName string

// Variables d'environnement — clés API (sensibles)
@secure()
param googleApiKey string

@secure()
param braveApiKey string

// Variables d'environnement — base de données (optionnelles)
param useNeonDb string = 'False'

@secure()
param neonDb string = ''

param useSupabase string = 'False'
param supabaseProject string = ''

@secure()
param supabasePassword string = ''

// Référence au registre ACR pour récupérer les credentials
resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' existing = {
  name: acrName
}

// Azure Container App
resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: containerAppName
  location: location
  properties: {
    environmentId: containerAppEnvId
    configuration: {
      // Activer l'accès externe (HTTPS public)
      ingress: {
        external: true
        // Port cible de l'application (playground server FastAPI)
        targetPort: 7777
        transport: 'auto'
      }
      // Authentification auprès du registre ACR
      registries: [
        {
          server: acrLoginServer
          username: acr.listCredentials().username
          passwordSecretRef: 'acr-password'
        }
      ]
      // Secrets — stockés de manière sécurisée dans Azure
      secrets: [
        {
          name: 'acr-password'
          value: acr.listCredentials().passwords[0].value
        }
        {
          name: 'google-api-key'
          value: googleApiKey
        }
        {
          name: 'brave-api-key'
          value: braveApiKey
        }
        {
          name: 'neon-db'
          value: neonDb
        }
        {
          name: 'supabase-password'
          value: supabasePassword
        }
      ]
    }
    template: {
      containers: [
        {
          // Image Docker depuis ACR
          image: '${acrLoginServer}/${imageName}'
          name: 'narrative-ai'
          resources: {
            // Ressources minimales pour réduire les coûts
            cpu: json('0.5')
            memory: '1Gi'
          }
          // Variables d'environnement injectées dans le conteneur
          env: [
            {
              name: 'GOOGLE_API_KEY'
              secretRef: 'google-api-key'
            }
            {
              name: 'BRAVE_API_KEY'
              secretRef: 'brave-api-key'
            }
            {
              name: 'USE_NEONDB'
              value: useNeonDb
            }
            {
              name: 'NEON_DB'
              secretRef: 'neon-db'
            }
            {
              name: 'USE_SUPABASE'
              value: useSupabase
            }
            {
              name: 'SUPABASE_PROJECT'
              value: supabaseProject
            }
            {
              name: 'SUPABASE_PASSWORD'
              secretRef: 'supabase-password'
            }
          ]
        }
      ]
      // Mise à l'échelle : minimum 1 réplique, maximum 3
      scale: {
        minReplicas: 1
        maxReplicas: 3
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Sorties
// ---------------------------------------------------------------------------

@description('URL publique HTTPS de la Container App')
output appUrl string = 'https://${containerApp.properties.configuration.ingress.fqdn}'
