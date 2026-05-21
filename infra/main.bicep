// main.bicep — Point d'entrée principal de l'infrastructure Azure
// Ce fichier orchestre le déploiement de toutes les ressources Azure nécessaires
// pour héberger l'application narrative-ai sur Azure Container Apps.
//
// Ressources déployées :
//   1. Azure Container Registry (ACR)  — stockage de l'image Docker
//   2. Azure Container Apps Environment — environnement d'exécution partagé
//   3. Azure Container App             — l'application elle-même

targetScope = 'resourceGroup'

// ---------------------------------------------------------------------------
// Paramètres
// ---------------------------------------------------------------------------

@description('Emplacement Azure pour toutes les ressources (ex: westeurope, eastus)')
param location string = resourceGroup().location

@description('Nom court de l\'environnement (ex: dev, prod)')
@maxLength(10)
param environmentName string = 'dev'

@description('Clé API Google Gemini')
@secure()
param googleApiKey string

@description('Clé API Brave Search')
@secure()
param braveApiKey string

@description('Activer NeonDB comme base de données (True/False)')
param useNeonDb string = 'False'

@description('Chaîne de connexion NeonDB (optionnel)')
@secure()
param neonDb string = ''

@description('Activer Supabase comme base de données (True/False)')
param useSupabase string = 'False'

@description('Identifiant du projet Supabase (optionnel)')
param supabaseProject string = ''

@description('Mot de passe Supabase (optionnel)')
@secure()
param supabasePassword string = ''

// ---------------------------------------------------------------------------
// Variables
// ---------------------------------------------------------------------------

var resourcePrefix = 'narrativeai-${environmentName}'
var acrName = replace('acr${resourcePrefix}', '-', '')
var containerAppEnvName = 'env-${resourcePrefix}'
var containerAppName = 'app-${resourcePrefix}'
var imageName = 'narrative-ai:latest'

// ---------------------------------------------------------------------------
// Module : Azure Container Registry
// ---------------------------------------------------------------------------

module acr 'modules/acr.bicep' = {
  name: 'deploy-acr'
  params: {
    acrName: acrName
    location: location
  }
}

// ---------------------------------------------------------------------------
// Module : Azure Container Apps Environment
// ---------------------------------------------------------------------------

module containerAppEnv 'modules/container-app-env.bicep' = {
  name: 'deploy-container-app-env'
  params: {
    containerAppEnvName: containerAppEnvName
    location: location
  }
}

// ---------------------------------------------------------------------------
// Module : Azure Container App
// ---------------------------------------------------------------------------

module containerApp 'modules/container-app.bicep' = {
  name: 'deploy-container-app'
  params: {
    containerAppName: containerAppName
    location: location
    containerAppEnvId: containerAppEnv.outputs.containerAppEnvId
    acrLoginServer: acr.outputs.acrLoginServer
    acrName: acr.outputs.acrName
    imageName: imageName
    googleApiKey: googleApiKey
    braveApiKey: braveApiKey
    useNeonDb: useNeonDb
    neonDb: neonDb
    useSupabase: useSupabase
    supabaseProject: supabaseProject
    supabasePassword: supabasePassword
  }
  dependsOn: [
    acr
    containerAppEnv
  ]
}

// ---------------------------------------------------------------------------
// Sorties
// ---------------------------------------------------------------------------

@description('URL publique de l\'application déployée')
output appUrl string = containerApp.outputs.appUrl

@description('Serveur de connexion ACR')
output acrLoginServer string = acr.outputs.acrLoginServer
