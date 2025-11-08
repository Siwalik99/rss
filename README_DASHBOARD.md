# Dashboard Financier Global

Application de tableau de bord financier développée en Python avec Streamlit pour afficher en temps réel les informations financières des marchés mondiaux.

## Fonctionnalités

Cette application affiche sur une seule page :

### 🇨🇭 Actions du SMI (Swiss Market Index)
- Les principales actions du marché suisse
- Prix actuel en CHF
- Variation en pourcentage

### 🇪🇺 Actions de l'Eurostoxx 50
- Les principales actions européennes
- Prix actuel
- Variation en pourcentage

### 📈 Top 20 Nasdaq par Volume
- Les 20 titres avec le plus de volume sur le Nasdaq
- Prix actuel en USD
- Volume d'échange
- Variation en pourcentage

### 🌍 Performance des Indices Majeurs
- S&P 500, Dow Jones, Nasdaq
- FTSE 100, DAX, CAC 40
- Nikkei 225, Hang Seng, Shanghai Composite
- Euro Stoxx 50, SMI
- Variation journalière et YTD (Year-to-Date)

### 💱 Taux de Change (FX) - CHF
- EUR/CHF
- USD/CHF
- GBP/CHF
- JPY/CHF
- Variation sur 1 jour et 1 mois

### ₿ Principales Cryptomonnaies
- Bitcoin, Ethereum, Binance Coin, Ripple
- Cardano, Dogecoin, Solana, Polygon
- Polkadot, Avalanche, Uniswap, Chainlink
- Prix en USD
- Variation sur 24h et 7 jours

## Installation

Les dépendances sont déjà listées dans `requirements.txt` :

```bash
pip install -r requirements.txt
```

## Utilisation

Pour lancer l'application :

```bash
streamlit run financial_dashboard.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut à l'adresse `http://localhost:8501`

## Fonctionnalités Techniques

- **Cache des données** : Les données sont mises en cache pendant 5 minutes pour optimiser les performances
- **Coloration automatique** : Les variations positives apparaissent en vert, les négatives en rouge
- **Bouton de rafraîchissement** : Permet de forcer la mise à jour des données
- **Source des données** : Toutes les données proviennent de Yahoo Finance via la bibliothèque `yfinance`

## Notes

- Les données sont mises à jour toutes les 5 minutes automatiquement grâce au système de cache
- Certaines actions peuvent ne pas apparaître si les données ne sont pas disponibles sur Yahoo Finance
- L'application nécessite une connexion internet pour récupérer les données

## Auteur

Développé avec Python, Streamlit et yfinance
