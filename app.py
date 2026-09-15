import streamlit as st
import pandas as pd
from datetime import datetime

# ============================================================
# OMEGA AGENTIC SUPER AI
# app.py
# ============================================================

st.set_page_config(
    page_title="OMEGA AGENTIC SUPER AI",
    page_icon="🇲🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
# OMEGA AGENTIC SUPER AI

Tu es OMEGA AGENTIC SUPER AI, superviseur intelligent spécialisé
dans le sourcing B2B multidomaine au Maroc.

MISSION:
- Recherche
- Sourcing
- Vérification
- Contradiction
- Analyse marché
- Analyse économique
- Logistique
- Gestion des risques
- Décision

DOMAINES:
- Ferraille lourde
- Fer massif
- Fer à béton
- HMS 1 / HMS 2
- Rails
- Tracteurs
- Véhicules réformés
- Aluminium
- Cuivre rouge
- Cuivre jaune / laiton
- Métaux industriels
- Machines industrielles
- Matériel de chantier
- Déstockage
- Import / Export
- Immobilier B2B

RÈGLE ABSOLUE:
Ne jamais présenter une information non vérifiée comme un fait.

STATUTS:
VERIFIED
PROBABLE
HYPOTHESIS
UNVERIFIED
STALE
REJECTED

SCORE OMEGA:
Identité fournisseur /20
Existence stock /20
Quantité /15
Récence /15
Prix /10
Qualité /10
Logistique /5
Cohérence sources /5

TOTAL /100.
"""

# ============================================================
# DATA
# ============================================================

REGIONS = [
    "Toutes les régions",
    "Casablanca-Settat",
    "Marrakech-Safi",
    "Rabat-Salé-Kénitra",
    "Fès-Meknès",
    "Tanger-Tétouan-Al Hoceïma",
    "Souss-Massa",
    "Béni Mellal-Khénifra",
    "Drâa-Tafilalet",
    "Oriental",
    "Guelmim-Oued Noun",
    "Laâyoune-Sakia El Hamra",
    "Dakhla-Oued Ed-Dahab"
]

DOMAINS = {
    "Ferraille & métaux ferreux": [
        "Ferraille lourde",
        "Fer massif",
        "Fer à béton",
        "HMS 1",
        "HMS 2",
        "Rails",
        "Structures métalliques"
    ],
    "Métaux non-ferreux": [
        "Aluminium",
        "Cuivre rouge",
        "Cuivre jaune / Laiton",
        "Métaux industriels"
    ],
    "Agriculture": [
        "Tracteurs réformés",
        "Matériel agricole",
        "Machines agricoles",
        "Équipements d'irrigation"
    ],
    "Automobile": [
        "Véhicules réformés",
        "Véhicules accidentés",
        "Pièces automobiles",
        "Flottes à renouveler"
    ],
    "Industrie": [
        "Machines industrielles",
        "Matériel de chantier",
        "Équipements industriels",
        "Stocks industriels",
        "Déstockage"
    ],
    "Import / Export": [
        "Ferraille",
        "Métaux",
        "Machines",
        "Matériel industriel",
        "Produits B2B"
    ],
    "Immobilier B2B": [
        "Terrain industriel",
        "Local commercial",
        "Entrepôt",
        "Hangar",
        "Terrain agricole"
    ]
}

# ============================================================
# SESSION STATE
# ============================================================

if "opportunities" not in st.session_state:
    st.session_state.opportunities = []

if "search_history" not in st.session_state:
    st.session_state.search_history = []

# ============================================================
# FUNCTIONS
# ============================================================

def omega_score(
    identity,
    stock,
    quantity,
    recency,
    price,
    quality,
    logistics,
    coherence
):
    return (
        identity
        + stock
        + quantity
        + recency
        + price
        + quality
        + logistics
        + coherence
    )


def score_status(score):
    if score >= 85:
        return "🟢 PRIORITÉ CRITIQUE"
    elif score >= 70:
        return "🟢 TRÈS INTÉRESSANT"
    elif score >= 55:
        return "🟠 À QUALIFIER"
    elif score >= 35:
        return "🟠 FAIBLE"
    return "🔴 REJET / NON FIABLE"


def confidence(score):
    if score >= 85:
        return "Très élevée"
    elif score >= 70:
        return "Élevée"
    elif score >= 55:
        return "Moyenne"
    elif score >= 35:
        return "Faible"
    return "Très faible"


def create_demo_opportunities(product, region):
    """
    Données de démonstration uniquement.
    Elles ne représentent PAS des fournisseurs réels.
    """

    return [
        {
            "Fournisseur": "Prospect démonstration A",
            "Produit": product,
            "Région": region,
            "Ville": "À vérifier",
            "Quantité (t)": 2000,
            "Prix": "À vérifier",
            "Statut": "UNVERIFIED",
            "Score": 72,
            "Confiance": "Élevée",
            "Source": "Démonstration",
            "Preuve stock": "À vérifier",
            "Contradictions": "Aucune donnée suffisante",
            "Prochaine action": "Vérifier directement fournisseur + stock"
        },
        {
            "Fournisseur": "Prospect démonstration B",
            "Produit": product,
            "Région": region,
            "Ville": "À vérifier",
            "Quantité (t)": 850,
            "Prix": "À vérifier",
            "Statut": "PROBABLE",
            "Score": 61,
            "Confiance": "Moyenne",
            "Source": "Démonstration",
            "Preuve stock": "Non confirmée",
            "Contradictions": "Quantité à confirmer",
            "Prochaine action": "Demander preuve de stock récente"
        },
        {
            "Fournisseur": "Prospect démonstration C",
            "Produit": product,
            "Région": region,
            "Ville": "À vérifier",
            "Quantité (t)": 3000,
            "Prix": "À vérifier",
            "Statut": "UNVERIFIED",
            "Score": 42,
            "Confiance": "Faible",
            "Source": "Démonstration",
            "Preuve stock": "Non disponible",
            "Contradictions": "Informations insuffisantes",
            "Prochaine action": "Ne pas valider avant vérification"
        }
    ]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🇲🇦 OMEGA")

    st.caption("AGENTIC SUPER AI")
    st.divider()

    menu = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🔎 Nouvelle recherche",
            "📦 Opportunités",
            "🔍 Vérification",
            "📊 Market Intelligence",
            "⚠️ Risk Center",
            "🧠 Mémoire",
            "⚙️ Configuration"
        ]
    )

    st.divider()

    st.info(
        "OMEGA privilégie les opportunités "
        "réelles, récentes et vérifiables."
    )

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <h1 style='text-align:center;'>
    🇲🇦 OMEGA AGENTIC SUPER AI
    </h1>
    <p style='text-align:center;'>
    B2B SOURCING • RESEARCH • VERIFICATION • ANALYSIS • DECISION
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# DASHBOARD
# ============================================================

if menu == "🏠 Dashboard":

    st.subheader("📊 OMEGA Dashboard")

    opportunities = st.session_state.opportunities

    total = len(opportunities)

    if total > 0:
        df = pd.DataFrame(opportunities)

        high = len(df[df["Score"] >= 70])
        medium = len(df[(df["Score"] >= 55) & (df["Score"] < 70)])
        low = len(df[df["Score"] < 55])

        tonnes = (
            pd.to_numeric(
                df["Quantité (t)"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )
    else:
        high = 0
        medium = 0
        low = 0
        tonnes = 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📦 Opportunités",
        total
    )

    c2.metric(
        "🟢 Score ≥70",
        high
    )

    c3.metric(
        "🟠 À qualifier",
        medium
    )

    c4.metric(
        "⚖️ Tonnes identifiées",
        f"{tonnes:,.0f}"
    )

    st.divider()

    st.subheader("🎯 Philosophie OMEGA")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(
            "### VERIFIED\n"
            "Informations confirmées."
        )

    with col2:
        st.warning(
            "### PROBABLE\n"
            "Informations nécessitant confirmation."
        )

    with col3:
        st.error(
            "### UNVERIFIED\n"
            "Ne pas considérer comme opportunité validée."
        )

# ============================================================
# NEW SEARCH
# ============================================================

elif menu == "🔎 Nouvelle recherche":

    st.subheader("🔎 Nouvelle recherche OMEGA")

    col1, col2 = st.columns(2)

    with col1:

        domain = st.selectbox(
            "Domaine",
            list(DOMAINS.keys())
        )

        product = st.selectbox(
            "Produit",
            DOMAINS[domain]
        )

        quantity = st.number_input(
            "Quantité minimale (tonnes)",
            min_value=1,
            value=100,
            step=100
        )

    with col2:

        region = st.selectbox(
            "Région",
            REGIONS
        )

        mode = st.selectbox(
            "Mode de recherche",
            [
                "Normal",
                "Deep Research",
                "Enterprise Sourcing"
            ]
        )

        destination = st.text_input(
            "Destination",
            placeholder="Ex: Marrakech"
        )

    keywords = st.text_area(
        "Instructions supplémentaires",
        placeholder=(
            "Ex: Fournisseur direct, stock récent, "
            "prix départ parc, priorité aux gros volumes..."
        )
    )

    st.divider()

    if st.button(
        "🚀 LANCER OMEGA",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "OMEGA analyse la demande..."
        ):

            results = create_demo_opportunities(
                product,
                region
            )

            st.session_state.opportunities.extend(
                results
            )

            st.session_state.search_history.append(
                {
                    "Date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    ),
                    "Domaine": domain,
                    "Produit": product,
                    "Région": region,
                    "Quantité": quantity,
                    "Mode": mode
                }
            )

        st.success(
            "Recherche OMEGA terminée."
        )

        st.info(
            "⚠️ Les résultats affichés ici sont "
            "des données de démonstration. "
            "Connecte ensuite le moteur de recherche "
            "réel pour obtenir des prospects Internet."
        )

# ============================================================
# OPPORTUNITIES
# ============================================================

elif menu == "📦 Opportunités":

    st.subheader("📦 Opportunités détectées")

    if not st.session_state.opportunities:

        st.info(
            "Aucune opportunité. "
            "Lance une nouvelle recherche."
        )

    else:

        df = pd.DataFrame(
            st.session_state.opportunities
        )

        min_score = st.slider(
            "Score minimum",
            0,
            100,
            0
        )

        filtered = df[
            df["Score"] >= min_score
        ]

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        for index, row in filtered.iterrows():

            with st.expander(
                f"{row['Fournisseur']} — "
                f"{row['Score']}/100"
            ):

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Score OMEGA",
                    f"{row['Score']}/100"
                )

                c2.metric(
                    "Quantité",
                    f"{row['Quantité (t)']} t"
                )

                c3.write(
                    f"**Statut:** {row['Statut']}"
                )

                st.write(
                    f"**Produit:** {row['Produit']}"
                )

                st.write(
                    f"**Région:** {row['Région']}"
                )

                st.write(
                    f"**Source:** {row['Source']}"
                )

                st.write(
                    f"**Preuve de stock:** "
                    f"{row['Preuve stock']}"
                )

                st.write(
                    f"**Contradictions:** "
                    f"{row['Contradictions']}"
                )

                st.info(
                    f"👉 Prochaine action : "
                    f"{row['Prochaine action']}"
                )

# ============================================================
# VERIFICATION
# ============================================================

elif menu == "🔍 Vérification":

    st.subheader("🔍 Verification Center")

    if not st.session_state.opportunities:

        st.info(
            "Aucun prospect à vérifier."
        )

    else:

        df = pd.DataFrame(
            st.session_state.opportunities
        )

        selected = st.selectbox(
            "Sélectionner un prospect",
            df["Fournisseur"].tolist()
        )

        prospect = df[
            df["Fournisseur"] == selected
        ].iloc[0]

        st.markdown(
            f"## {prospect['Fournisseur']}"
        )

        checks = {
            "Identité fournisseur": "À vérifier",
            "Existence du stock": prospect["Preuve stock"],
            "Quantité": "À confirmer",
            "Prix": prospect["Prix"],
            "Localisation": prospect["Région"],
            "Récence": "À vérifier",
            "Qualité": "À vérifier",
            "Logistique": "À vérifier"
        }

        for name, status in checks.items():

            col1, col2 = st.columns([3, 1])

            col1.write(name)
            col2.write(status)

        st.warning(
            "Une opportunité ne doit être VALIDATED "
            "qu'après confirmation suffisante du stock "
            "et du fournisseur."
        )

# ============================================================
# MARKET
# ============================================================

elif menu == "📊 Market Intelligence":

    st.subheader("📊 Market Intelligence")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Prix achat",
            "À déterminer"
        )

    with col2:

        st.metric(
            "Prix revente",
            "À déterminer"
        )

    st.divider()

    st.write(
        "Le module Market Intelligence est prêt "
        "à recevoir les données provenant du moteur "
        "de recherche et des sources de marché."
    )

# ============================================================
# RISK CENTER
# ============================================================

elif menu == "⚠️ Risk Center":

    st.subheader("⚠️ Risk Center")

    risks = [
        "Annonce ancienne",
        "Stock non confirmé",
        "Quantité non documentée",
        "Prix anormal",
        "Fournisseur non vérifié",
        "Adresse incohérente",
        "Doublon potentiel",
        "Photos non vérifiées",
        "Contradiction entre sources",
        "Logistique non confirmée"
    ]

    for risk in risks:

        st.checkbox(
            risk,
            value=False,
            key=f"risk_{risk}"
        )

# ============================================================
# MEMORY
# ============================================================

elif menu == "🧠 Mémoire":

    st.subheader("🧠 Mémoire OMEGA")

    if st.session_state.search_history:

        history = pd.DataFrame(
            st.session_state.search_history
        )

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Aucune recherche enregistrée."
        )

    st.divider()

    st.write(
        "La mémoire persistante PostgreSQL/SQLite "
        "pourra être connectée dans la prochaine couche."
    )

# ============================================================
# CONFIGURATION
# ============================================================

elif menu == "⚙️ Configuration":

    st.subheader("⚙️ Configuration OMEGA")

    st.text_input(
        "Nom du système",
        value="OMEGA AGENTIC SUPER AI"
    )

    st.selectbox(
        "Langue",
        [
            "Français",
            "العربية",
            "English"
        ]
    )

    st.selectbox(
        "Niveau de recherche",
        [
            "Normal",
            "Deep Research",
            "Enterprise"
        ]
    )

    st.divider()

    st.subheader("🧠 System Prompt")

    st.code(
        SYSTEM_PROMPT,
        language="text"
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "OMEGA AGENTIC SUPER AI 🇲🇦 | "
    "B2B Research • Sourcing • Verification • Analysis"
)
