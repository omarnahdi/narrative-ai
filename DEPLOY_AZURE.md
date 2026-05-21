# Guide de Déploiement sur Azure Container Apps 🚀

Ce guide vous explique pas-à-pas comment déployer l'application **narrative-ai** sur **Azure Container Apps** en utilisant Azure Developer CLI (`azd`) et GitHub Actions.

---

## Table des matières

1. [Prérequis](#1-prérequis)
2. [Architecture déployée](#2-architecture-déployée)
3. [Déploiement manuel avec `azd`](#3-déploiement-manuel-avec-azd)
4. [Configurer les secrets GitHub](#4-configurer-les-secrets-github)
5. [CI/CD automatique avec GitHub Actions](#5-cicd-automatique-avec-github-actions)
6. [Vérifier le déploiement](#6-vérifier-le-déploiement)
7. [Variables d'environnement](#7-variables-denvironnement)
8. [Résolution de problèmes](#8-résolution-de-problèmes)

---

## 1. Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :

### Outils requis

| Outil | Version minimale | Installation |
|-------|-----------------|--------------|
| [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) | 2.50+ | `winget install Microsoft.AzureCLI` |
| [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) | 1.5+ | `winget install Microsoft.Azd` |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | 24+ | [Télécharger ici](https://www.docker.com/products/docker-desktop/) |
| [Git](https://git-scm.com/) | 2.40+ | `winget install Git.Git` |

> **💡 Conseil** : Sur macOS, vous pouvez utiliser `brew` à la place de `winget`.
> ```sh
> brew install azure-cli azd
> ```

### Compte Azure requis

- Un **abonnement Azure actif** (vous pouvez créer un [compte gratuit](https://azure.microsoft.com/free/))
- Les **clés API** pour l'application :
  - `GOOGLE_API_KEY` — Clé API Google Gemini ([obtenir ici](https://aistudio.google.com/))
  - `BRAVE_API_KEY` — Clé API Brave Search ([obtenir ici](https://brave.com/search/api/))

---

## 2. Architecture déployée

Le déploiement crée les ressources Azure suivantes :

```
Groupe de ressources Azure
├── 🗄️  Azure Container Registry (ACR)   — Stocke l'image Docker
├── 🌍  Container Apps Environment        — Environnement partagé
└── 📦  Azure Container App              — Votre application (port 7777)
```

---

## 3. Déploiement manuel avec `azd`

### Étape 1 : Cloner le dépôt

```bash
git clone https://github.com/rajputshamshed-ux/narrative-ai.git
cd narrative-ai
```

### Étape 2 : Se connecter à Azure

```bash
# S'authentifier avec Azure CLI
az login

# S'authentifier avec Azure Developer CLI
azd auth login
```

> **💡 Note** : Ces deux commandes ouvriront un navigateur pour vous connecter à votre compte Azure.

### Étape 3 : Initialiser l'environnement azd

```bash
azd env new narrative-ai-prod
```

Cette commande vous demandera de choisir :
- **Abonnement Azure** : Sélectionnez votre abonnement dans la liste
- **Région Azure** : Par exemple `westeurope` (Europe de l'Ouest) ou `eastus` (États-Unis Est)

### Étape 4 : Configurer les variables d'environnement

```bash
# Clés API obligatoires
azd env set GOOGLE_API_KEY "votre-clé-google-api"
azd env set BRAVE_API_KEY "votre-clé-brave-api"

# Optionnel : NeonDB
azd env set USE_NEONDB "True"
azd env set NEON_DB "votre-connection-string-neon"

# Optionnel : Supabase
azd env set USE_SUPABASE "True"
azd env set SUPABASE_PROJECT "votre-projet-supabase"
azd env set SUPABASE_PASSWORD "votre-mot-de-passe-supabase"
```

### Étape 5 : Déployer l'application

```bash
azd up
```

Cette commande effectue automatiquement :
1. ✅ Création du groupe de ressources Azure
2. ✅ Provisionnement de l'infrastructure (ACR, Container Apps Environment, Container App)
3. ✅ Build de l'image Docker avec `Dockerfile.azure`
4. ✅ Push de l'image vers ACR
5. ✅ Déploiement sur Azure Container Apps

> **⏱️ Durée estimée** : 5 à 10 minutes lors du premier déploiement.

### Étape 6 : Accéder à l'application

Une fois le déploiement terminé, `azd` affiche l'URL de votre application :
```
Outputs:
  appUrl: https://app-narrativeai-dev.XXX.westeurope.azurecontainerapps.io
```

---

## 4. Configurer les secrets GitHub

Pour que le CI/CD automatique fonctionne, vous devez configurer des **secrets GitHub**.

### Étape 1 : Créer un service principal Azure

Un service principal permet à GitHub Actions de se connecter à Azure de manière sécurisée.

```bash
# Remplacez <votre-subscription-id> par votre ID d'abonnement Azure
az ad sp create-for-rbac \
  --name "narrative-ai-github-actions" \
  --role contributor \
  --scopes /subscriptions/<votre-subscription-id> \
  --sdk-auth
```

Cette commande génère un JSON ressemblant à ceci :
```json
{
  "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "subscriptionId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

> **🔒 Important** : Copiez ce JSON complet, vous en aurez besoin à l'étape suivante.

### Étape 2 : Ajouter les secrets dans GitHub

1. Allez sur votre dépôt GitHub : `https://github.com/rajputshamshed-ux/narrative-ai`
2. Cliquez sur **Settings** (⚙️)
3. Dans le menu de gauche, cliquez sur **Secrets and variables** → **Actions**
4. Cliquez sur **New repository secret**

Ajoutez les secrets suivants un par un :

| Nom du secret | Valeur |
|--------------|--------|
| `AZURE_CREDENTIALS` | Le JSON complet généré à l'étape précédente |
| `AZURE_SUBSCRIPTION_ID` | Votre ID d'abonnement Azure |
| `AZURE_RESOURCE_GROUP` | Le nom de votre groupe de ressources (ex: `rg-narrative-ai`) |
| `AZURE_CONTAINER_REGISTRY` | Le nom de votre ACR (ex: `acrnarrativeaidev`) |
| `GOOGLE_API_KEY` | Votre clé API Google Gemini |
| `BRAVE_API_KEY` | Votre clé API Brave Search |

---

## 5. CI/CD automatique avec GitHub Actions

### Comment ça fonctionne ?

Le fichier `.github/workflows/azure-deploy.yml` définit le pipeline automatique :

```
Push sur 'main'
      │
      ▼
┌─────────────────────────────────────────────────────┐
│              GitHub Actions Pipeline                 │
│                                                     │
│  1. 📥 Checkout du code                             │
│  2. 🔑 Connexion à Azure                            │
│  3. 🔑 Connexion au registre ACR                    │
│  4. 🐳 Build de l'image Docker (Dockerfile.azure)   │
│  5. 📤 Push de l'image vers ACR                     │
│  6. 🚀 Déploiement sur Azure Container Apps         │
│  7. 🔗 Affichage de l'URL de l'application          │
└─────────────────────────────────────────────────────┘
```

### Déclencher manuellement

Vous pouvez aussi déclencher le déploiement manuellement :
1. Allez sur **Actions** dans votre dépôt GitHub
2. Sélectionnez le workflow **"Deploy to Azure Container Apps"**
3. Cliquez sur **"Run workflow"**

---

## 6. Vérifier le déploiement

### Via Azure CLI

```bash
# Lister les Container Apps dans votre groupe de ressources
az containerapp list \
  --resource-group <votre-resource-group> \
  --output table

# Obtenir l'URL de l'application
az containerapp show \
  --name app-narrativeai-dev \
  --resource-group <votre-resource-group> \
  --query "properties.configuration.ingress.fqdn" \
  --output tsv

# Voir les logs de l'application
az containerapp logs show \
  --name app-narrativeai-dev \
  --resource-group <votre-resource-group> \
  --follow
```

### Via le Portail Azure

1. Allez sur [portal.azure.com](https://portal.azure.com)
2. Recherchez **"Container Apps"** dans la barre de recherche
3. Sélectionnez votre application `app-narrativeai-dev`
4. L'URL est visible dans **"Overview"** → **"Application URL"**

---

## 7. Variables d'environnement

| Variable | Obligatoire | Description |
|----------|------------|-------------|
| `GOOGLE_API_KEY` | ✅ Oui | Clé API Google Gemini pour l'IA |
| `BRAVE_API_KEY` | ✅ Oui | Clé API Brave Search pour la recherche web |
| `USE_NEONDB` | ❌ Non | Mettre `True` pour utiliser NeonDB |
| `NEON_DB` | ❌ Non | Chaîne de connexion NeonDB |
| `USE_SUPABASE` | ❌ Non | Mettre `True` pour utiliser Supabase |
| `SUPABASE_PROJECT` | ❌ Non | Identifiant du projet Supabase |
| `SUPABASE_PASSWORD` | ❌ Non | Mot de passe Supabase |

---

## 8. Résolution de problèmes

### ❌ Erreur : "az: command not found"
**Solution** : Installez Azure CLI depuis [ce lien](https://learn.microsoft.com/cli/azure/install-azure-cli).

### ❌ Erreur : "You do not have permission to perform this action"
**Solution** : Vérifiez que votre compte Azure a le rôle **Contributor** sur l'abonnement.

### ❌ Erreur : "Image pull failed" dans la Container App
**Solution** : Vérifiez que l'ACR est correctement configuré et que les credentials sont valides :
```bash
az acr check-health --name <votre-acr-name>
```

### ❌ L'application ne répond pas
**Solution** : Vérifiez les logs :
```bash
az containerapp logs show \
  --name app-narrativeai-dev \
  --resource-group <votre-resource-group>
```

### ❌ Erreur dans GitHub Actions : "AZURE_CREDENTIALS secret not found"
**Solution** : Vérifiez que vous avez bien ajouté tous les secrets dans GitHub Settings → Secrets and variables → Actions.

---

## Commandes utiles

```bash
# Voir l'état de l'environnement azd
azd env list

# Mettre à jour l'application (après un changement de code)
azd deploy

# Supprimer toutes les ressources Azure (éviter les coûts inutiles)
azd down

# Voir les logs en temps réel
az containerapp logs show \
  --name app-narrativeai-dev \
  --resource-group <votre-resource-group> \
  --follow
```

---

*Pour toute question, ouvrez une issue sur le dépôt GitHub.*
