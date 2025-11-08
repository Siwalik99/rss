import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(page_title="Dashboard Financier", layout="wide")

# Titre principal
st.title("📊 Dashboard Financier Global")
st.markdown("---")

# Fonction pour récupérer les données d'un ticker
@st.cache_data(ttl=300)  # Cache pour 5 minutes
def get_ticker_data(ticker, period="1d"):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        info = stock.info
        return data, info
    except Exception as e:
        st.warning(f"Erreur pour {ticker}: {str(e)}")
        return None, None

# Fonction pour récupérer les indices du SMI
@st.cache_data(ttl=300)
def get_smi_stocks():
    # Principales actions du SMI (Swiss Market Index)
    smi_tickers = {
        'NESN.SW': 'Nestlé',
        'NOVN.SW': 'Novartis',
        'ROG.SW': 'Roche',
        'ABBN.SW': 'ABB',
        'UBSG.SW': 'UBS Group',
        'CSGN.SW': 'Credit Suisse',
        'ZURN.SW': 'Zurich Insurance',
        'SREN.SW': 'Swiss Re',
        'GIVN.SW': 'Givaudan',
        'HOLN.SW': 'Holcim',
        'LONN.SW': 'Lonza Group',
        'SLHN.SW': 'Swiss Life',
        'PGHN.SW': 'Partners Group',
        'SIKA.SW': 'Sika',
        'GEBN.SW': 'Geberit',
        'SCMN.SW': 'Swisscom',
        'ADEN.SW': 'Adecco',
        'SGSN.SW': 'SGS',
        'KNIN.SW': 'Kuhne + Nagel',
        'BAER.SW': 'Julius Baer'
    }

    data = []
    for ticker, name in smi_tickers.items():
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="5d")
            if not hist.empty and len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change = ((current_price - prev_price) / prev_price) * 100
                data.append({
                    'Ticker': ticker,
                    'Nom': name,
                    'Prix': f"{current_price:.2f} CHF",
                    'Variation (%)': f"{change:+.2f}%",
                    'change_value': change
                })
        except Exception as e:
            continue

    return pd.DataFrame(data)

# Fonction pour récupérer les indices de l'Eurostoxx 50
@st.cache_data(ttl=300)
def get_eurostoxx50_stocks():
    # Principales actions de l'Eurostoxx 50
    eurostoxx_tickers = {
        'SAN.MC': 'Santander',
        'AIR.PA': 'Airbus',
        'SU.PA': 'Schneider Electric',
        'OR.PA': "L'Oréal",
        'SAP.DE': 'SAP',
        'SIE.DE': 'Siemens',
        'AIR.PA': 'Air Liquide',
        'ASML.AS': 'ASML',
        'MC.PA': 'LVMH',
        'TTE.PA': 'TotalEnergies',
        'DTE.DE': 'Deutsche Telekom',
        'BNP.PA': 'BNP Paribas',
        'BBVA.MC': 'BBVA',
        'IBE.MC': 'Iberdrola',
        'ITX.MC': 'Inditex',
        'MUV2.DE': 'Munich Re',
        'ENEL.MI': 'Enel',
        'BN.PA': 'Danone',
        'DG.PA': 'Vinci',
        'ABI.BR': 'AB InBev'
    }

    data = []
    for ticker, name in eurostoxx_tickers.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            if not hist.empty and len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change = ((current_price - prev_price) / prev_price) * 100
                data.append({
                    'Ticker': ticker,
                    'Nom': name,
                    'Prix': f"{current_price:.2f}",
                    'Variation (%)': f"{change:+.2f}%",
                    'change_value': change
                })
        except Exception as e:
            continue

    return pd.DataFrame(data)

# Fonction pour récupérer le top 20 Nasdaq par volume
@st.cache_data(ttl=300)
def get_nasdaq_top_volume():
    # Liste des principales actions du Nasdaq (approximation basée sur le volume typique)
    nasdaq_tickers = [
        'AAPL', 'MSFT', 'NVDA', 'TSLA', 'GOOGL', 'AMZN', 'META', 'AMD',
        'NFLX', 'INTC', 'CSCO', 'ADBE', 'AVGO', 'QCOM', 'TXN', 'COST',
        'AMGN', 'PEP', 'TMUS', 'CMCSA', 'SBUX', 'PYPL', 'INTU', 'GILD'
    ]

    data = []
    for ticker in nasdaq_tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            info = stock.info
            if not hist.empty and len(hist) >= 1:
                current_price = hist['Close'].iloc[-1]
                volume = hist['Volume'].iloc[-1]

                if len(hist) >= 2:
                    prev_price = hist['Close'].iloc[-2]
                    change = ((current_price - prev_price) / prev_price) * 100
                else:
                    change = 0

                data.append({
                    'Ticker': ticker,
                    'Nom': info.get('shortName', ticker),
                    'Prix': f"${current_price:.2f}",
                    'Volume': volume,
                    'Variation (%)': f"{change:+.2f}%",
                    'change_value': change
                })
        except Exception as e:
            continue

    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values('Volume', ascending=False).head(20)
        df['Volume'] = df['Volume'].apply(lambda x: f"{x:,.0f}")

    return df

# Fonction pour récupérer les indices majeurs
@st.cache_data(ttl=300)
def get_major_indices():
    indices = {
        '^GSPC': 'S&P 500',
        '^DJI': 'Dow Jones',
        '^IXIC': 'Nasdaq',
        '^FTSE': 'FTSE 100',
        '^GDAXI': 'DAX',
        '^FCHI': 'CAC 40',
        '^N225': 'Nikkei 225',
        '^HSI': 'Hang Seng',
        '000001.SS': 'Shanghai Composite',
        '^STOXX50E': 'EURO STOXX 50',
        '^SSMI': 'SMI'
    }

    data = []
    for ticker, name in indices.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            if not hist.empty and len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change = ((current_price - prev_price) / prev_price) * 100

                # Performance YTD
                ytd_start = datetime(datetime.now().year, 1, 1)
                ytd_data = stock.history(start=ytd_start)
                if not ytd_data.empty:
                    ytd_change = ((current_price - ytd_data['Close'].iloc[0]) / ytd_data['Close'].iloc[0]) * 100
                else:
                    ytd_change = 0

                data.append({
                    'Indice': name,
                    'Valeur': f"{current_price:,.2f}",
                    'Var. 1J (%)': f"{change:+.2f}%",
                    'Var. YTD (%)': f"{ytd_change:+.2f}%",
                    'change_1d': change,
                    'change_ytd': ytd_change
                })
        except Exception as e:
            continue

    return pd.DataFrame(data)

# Fonction pour récupérer les taux de change FX
@st.cache_data(ttl=300)
def get_fx_rates():
    fx_pairs = {
        'EURCHF=X': 'EUR/CHF',
        'USDCHF=X': 'USD/CHF',
        'GBPCHF=X': 'GBP/CHF',
        'JPYCHF=X': 'JPY/CHF'
    }

    data = []
    for ticker, pair in fx_pairs.items():
        try:
            fx = yf.Ticker(ticker)
            hist = fx.history(period="5d")
            if not hist.empty and len(hist) >= 2:
                current_rate = hist['Close'].iloc[-1]
                prev_rate = hist['Close'].iloc[-2]
                change = ((current_rate - prev_rate) / prev_rate) * 100

                # Performance sur 1 mois
                hist_1m = fx.history(period="1mo")
                if not hist_1m.empty:
                    change_1m = ((current_rate - hist_1m['Close'].iloc[0]) / hist_1m['Close'].iloc[0]) * 100
                else:
                    change_1m = 0

                data.append({
                    'Paire': pair,
                    'Taux': f"{current_rate:.4f}",
                    'Var. 1J (%)': f"{change:+.2f}%",
                    'Var. 1M (%)': f"{change_1m:+.2f}%",
                    'change_value': change
                })
        except Exception as e:
            continue

    return pd.DataFrame(data)

# Fonction pour récupérer les principales cryptos
@st.cache_data(ttl=300)
def get_crypto_prices():
    cryptos = {
        'BTC-USD': 'Bitcoin',
        'ETH-USD': 'Ethereum',
        'BNB-USD': 'Binance Coin',
        'XRP-USD': 'Ripple',
        'ADA-USD': 'Cardano',
        'DOGE-USD': 'Dogecoin',
        'SOL-USD': 'Solana',
        'MATIC-USD': 'Polygon',
        'DOT-USD': 'Polkadot',
        'AVAX-USD': 'Avalanche',
        'UNI-USD': 'Uniswap',
        'LINK-USD': 'Chainlink'
    }

    data = []
    for ticker, name in cryptos.items():
        try:
            crypto = yf.Ticker(ticker)
            hist = crypto.history(period="5d")
            if not hist.empty and len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change_1d = ((current_price - prev_price) / prev_price) * 100

                # Performance sur 7 jours
                if len(hist) >= 7:
                    week_ago_price = hist['Close'].iloc[-7]
                    change_7d = ((current_price - week_ago_price) / week_ago_price) * 100
                else:
                    change_7d = 0

                # Formater le prix selon sa valeur
                if current_price >= 1:
                    price_str = f"${current_price:,.2f}"
                else:
                    price_str = f"${current_price:.6f}"

                data.append({
                    'Crypto': name,
                    'Ticker': ticker,
                    'Prix (USD)': price_str,
                    'Var. 24h (%)': f"{change_1d:+.2f}%",
                    'Var. 7J (%)': f"{change_7d:+.2f}%",
                    'change_1d': change_1d,
                    'change_7d': change_7d
                })
        except Exception as e:
            continue

    return pd.DataFrame(data)

# Fonction pour colorer les variations
def color_negative_red(val):
    if isinstance(val, str) and '%' in val:
        try:
            num = float(val.replace('%', '').replace('+', ''))
            color = 'red' if num < 0 else 'green'
            return f'color: {color}'
        except:
            return ''
    return ''

# Affichage du tableau de bord
st.markdown("### 🇨🇭 Actions du SMI (Swiss Market Index)")
with st.spinner('Chargement des données SMI...'):
    smi_df = get_smi_stocks()
    if not smi_df.empty:
        display_df = smi_df[['Ticker', 'Nom', 'Prix', 'Variation (%)']].copy()
        st.dataframe(
            display_df.style.applymap(color_negative_red, subset=['Variation (%)']),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("Impossible de charger les données SMI")

st.markdown("---")

# Eurostoxx 50
st.markdown("### 🇪🇺 Actions de l'Eurostoxx 50")
with st.spinner('Chargement des données Eurostoxx 50...'):
    eurostoxx_df = get_eurostoxx50_stocks()
    if not eurostoxx_df.empty:
        display_df = eurostoxx_df[['Ticker', 'Nom', 'Prix', 'Variation (%)']].copy()
        st.dataframe(
            display_df.style.applymap(color_negative_red, subset=['Variation (%)']),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("Impossible de charger les données Eurostoxx 50")

st.markdown("---")

# Top 20 Nasdaq par volume
st.markdown("### 📈 Top 20 Nasdaq par Volume")
with st.spinner('Chargement des données Nasdaq...'):
    nasdaq_df = get_nasdaq_top_volume()
    if not nasdaq_df.empty:
        display_df = nasdaq_df[['Ticker', 'Nom', 'Prix', 'Volume', 'Variation (%)']].copy()
        st.dataframe(
            display_df.style.applymap(color_negative_red, subset=['Variation (%)']),
            use_container_width=True,
            height=500
        )
    else:
        st.warning("Impossible de charger les données Nasdaq")

st.markdown("---")

# Indices majeurs
st.markdown("### 🌍 Performance des Indices Majeurs")
with st.spinner('Chargement des indices majeurs...'):
    indices_df = get_major_indices()
    if not indices_df.empty:
        display_df = indices_df[['Indice', 'Valeur', 'Var. 1J (%)', 'Var. YTD (%)']].copy()
        st.dataframe(
            display_df.style.applymap(color_negative_red, subset=['Var. 1J (%)', 'Var. YTD (%)']),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("Impossible de charger les données des indices")

st.markdown("---")

# Taux de change FX
st.markdown("### 💱 Taux de Change (FX) - CHF")
with st.spinner('Chargement des taux de change...'):
    fx_df = get_fx_rates()
    if not fx_df.empty:
        display_df = fx_df[['Paire', 'Taux', 'Var. 1J (%)', 'Var. 1M (%)']].copy()
        st.dataframe(
            display_df.style.applymap(color_negative_red, subset=['Var. 1J (%)', 'Var. 1M (%)']),
            use_container_width=True,
            height=200
        )
    else:
        st.warning("Impossible de charger les taux de change")

st.markdown("---")

# Cryptos
st.markdown("### ₿ Principales Cryptomonnaies (USD)")
with st.spinner('Chargement des données crypto...'):
    crypto_df = get_crypto_prices()
    if not crypto_df.empty:
        display_df = crypto_df[['Crypto', 'Ticker', 'Prix (USD)', 'Var. 24h (%)', 'Var. 7J (%)']].copy()
        st.dataframe(
            display_df.style.applymap(color_negative_red, subset=['Var. 24h (%)', 'Var. 7J (%)']),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("Impossible de charger les données crypto")

# Pied de page
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Données fournies par Yahoo Finance | Mise à jour toutes les 5 minutes</p>
        <p><small>Dernière mise à jour: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</small></p>
    </div>
    """,
    unsafe_allow_html=True
)

# Bouton de rafraîchissement
if st.button("🔄 Rafraîchir les données", use_container_width=True):
    st.cache_data.clear()
    st.rerun()
