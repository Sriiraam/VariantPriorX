import html
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# CONFIG
# ============================================================

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "variantpriorx.db"

st.set_page_config(
    page_title="VariantPriorX",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PREMIUM THEME
# ============================================================

st.html("""
<style>

/* =========================================================
   MAIN APP
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 5% 4%,
            rgba(147, 211, 177, 0.48),
            transparent 31%
        ),
        radial-gradient(
            circle at 94% 7%,
            rgba(190, 165, 228, 0.44),
            transparent 32%
        ),
        radial-gradient(
            circle at 75% 78%,
            rgba(164, 215, 194, 0.26),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #E4F5EA 0%,
            #EFE7F8 48%,
            #E1F2E8 100%
        );

    color: #183328;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* =========================================================
   TYPOGRAPHY
   ========================================================= */

html,
body,
[class*="css"] {
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

h1,
h2,
h3,
h4 {
    color: #173C2E;
    letter-spacing: -0.025em;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            rgba(218, 241, 228, 0.98),
            rgba(232, 221, 247, 0.98)
        );

    border-right: 1px solid rgba(92, 130, 108, 0.18);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #1F4938;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    position: relative;
    overflow: hidden;

    padding: 2.6rem 2.7rem;

    border-radius: 26px;

    margin-bottom: 1.8rem;

    background:
        linear-gradient(
            115deg,
            rgba(178, 226, 200, 0.98) 0%,
            rgba(205, 231, 215, 0.98) 42%,
            rgba(214, 194, 239, 0.98) 100%
        );

    border:
        1px solid rgba(76, 121, 96, 0.22);

    box-shadow:
        0 18px 45px rgba(36, 76, 57, 0.13);
}

.hero::before {
    content: "";

    position: absolute;

    width: 330px;
    height: 330px;

    right: -90px;
    top: -170px;

    border-radius: 50%;

    background:
        rgba(255,255,255,0.25);
}

.hero::after {
    content: "";

    position: absolute;

    width: 220px;
    height: 220px;

    left: -90px;
    bottom: -140px;

    border-radius: 50%;

    background:
        rgba(255,255,255,0.18);
}

.hero-badge {
    position: relative;
    z-index: 2;

    display: inline-block;

    padding:
        0.46rem 0.88rem;

    border-radius: 999px;

    background:
        rgba(255,255,255,0.72);

    border:
        1px solid rgba(45,91,71,0.15);

    color: #315D4B;

    font-size: 0.78rem;

    font-weight: 800;

    letter-spacing: 0.09em;

    margin-bottom: 0.95rem;
}

.hero-title {
    position: relative;
    z-index: 2;

    color: #153B2C;

    font-size: 3.2rem;

    line-height: 1.03;

    font-weight: 850;

    letter-spacing: -0.04em;
}

.hero-sub {
    position: relative;
    z-index: 2;

    max-width: 940px;

    margin-top: 0.82rem;

    color: #435F52;

    font-size: 1.08rem;

    font-weight: 470;

    line-height: 1.65;
}


/* =========================================================
   KPI CARDS
   ========================================================= */

.kpi {
    min-height: 140px;

    padding: 1.35rem;

    border-radius: 19px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.95),
            rgba(246,251,248,0.90)
        );

    border:
        1px solid rgba(116, 151, 132, 0.20);

    box-shadow:
        0 9px 27px rgba(40,72,56,0.085);

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}

.kpi:hover {
    transform: translateY(-4px);

    box-shadow:
        0 15px 35px rgba(40,72,56,0.14);
}

.kpi-icon {
    font-size: 1.38rem;

    color: #76549E;

    margin-bottom: 0.55rem;
}

.kpi-value {
    color: #163C2D;

    font-size: 2.12rem;

    font-weight: 850;

    line-height: 1;
}

.kpi-label {
    color: #63766C;

    font-size: 0.86rem;

    font-weight: 650;

    margin-top: 0.52rem;
}


/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-wrap {
    margin-top: 2.4rem;
    margin-bottom: 0.85rem;
}

.section-kicker {
    color: #705093;

    font-size: 0.75rem;

    font-weight: 850;

    letter-spacing: 0.115em;

    text-transform: uppercase;
}

.section-title {
    color: #153C2D;

    font-size: 1.62rem;

    font-weight: 850;

    letter-spacing: -0.025em;

    margin-top: 0.12rem;
}

.section-desc {
    color: #5F7469;

    font-size: 0.94rem;

    line-height: 1.55;

    margin-top: 0.25rem;
}


/* =========================================================
   SELECTED VARIANT CARD
   ========================================================= */

.variant-card {
    padding: 1.35rem 1.45rem;

    margin-bottom: 1rem;

    border-radius: 19px;

    background:
        linear-gradient(
            120deg,
            rgba(255,255,255,0.94),
            rgba(236,247,241,0.93),
            rgba(241,234,249,0.92)
        );

    border:
        1px solid rgba(106,145,124,0.20);

    box-shadow:
        0 9px 27px rgba(38,70,54,0.075);
}

.variant-small {
    color: #725794;

    font-size: 0.76rem;

    font-weight: 850;

    letter-spacing: 0.09em;
}

.variant-title {
    color: #173D2E;

    margin-top: 0.35rem;

    font-size: 1.55rem;

    font-weight: 850;
}

.variant-id {
    color: #536C60;

    margin-top: 0.45rem;

    font-size: 0.90rem;

    line-height: 1.55;

    word-break: break-all;
}


/* =========================================================
   STREAMLIT METRIC CARDS
   ========================================================= */

[data-testid="stMetric"] {
    padding: 1.05rem;

    border-radius: 16px;

    background:
        rgba(255,255,255,0.91);

    border:
        1px solid rgba(109,145,126,0.19);

    box-shadow:
        0 7px 20px rgba(37,69,53,0.06);
}

[data-testid="stMetricLabel"] {
    font-size: 0.89rem;

    font-weight: 650;
}

[data-testid="stMetricValue"] {
    color: #173D2E;

    font-weight: 800;
}


/* =========================================================
   TABLES
   ========================================================= */

[data-testid="stDataFrame"] {
    overflow: hidden;

    border-radius: 17px;

    background:
        rgba(255,255,255,0.95);

    border:
        1px solid rgba(106,143,123,0.18);

    box-shadow:
        0 7px 22px rgba(35,68,52,0.055);
}


/* =========================================================
   FORM ELEMENTS
   ========================================================= */

[data-baseweb="input"] {
    border-radius: 11px;
}

[data-baseweb="select"] > div {
    border-radius: 11px;
}

.stDownloadButton button {
    border-radius: 11px;

    font-weight: 700;

    border:
        1px solid #AFCDBE;
}


/* =========================================================
   DISCLAIMER
   ========================================================= */

.disclaimer {
    margin-top: 2.3rem;

    padding: 1.2rem 1.35rem;

    border-radius: 15px;

    color: #66583F;

    font-size: 0.90rem;

    line-height: 1.65;

    background:
        linear-gradient(
            90deg,
            #FFF8DD,
            #FFF1E2
        );

    border:
        1px solid #E9D5AA;

    border-left:
        5px solid #D39B3C;
}


/* =========================================================
   STREAMLIT CHROME
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""")


# ============================================================
# HELPERS
# ============================================================

def section_header(kicker, title, description):

    st.html(
        f"""
        <div class="section-wrap">
            <div class="section-kicker">{html.escape(kicker)}</div>
            <div class="section-title">{html.escape(title)}</div>
            <div class="section-desc">{html.escape(description)}</div>
        </div>
        """
    )


@st.cache_data
def load_data():

    conn = sqlite3.connect(DB_PATH)

    data = pd.read_sql_query(
        "SELECT * FROM variants ORDER BY rank",
        conn,
    )

    conn.close()

    return data


# ============================================================
# DATABASE CHECK
# ============================================================

if not DB_PATH.exists():

    st.error(
        "VariantPriorX database not found. "
        "Run the VariantPriorX pipeline first."
    )

    st.stop()


df = load_data()


df["population_af"] = pd.to_numeric(
    df["population_af"],
    errors="coerce",
)


df["variantpriorx_score"] = pd.to_numeric(
    df["variantpriorx_score"],
    errors="coerce",
)


for column in [
    "impact_score",
    "clinvar_score",
    "frequency_score",
]:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🧬 VariantPriorX")

    st.caption(
        "Clinical genomics · Variant interpretation"
    )

    st.divider()

    st.markdown("### Explore variants")


    impact_options = sorted(
        df["max_impact"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    selected_impacts = st.multiselect(
        "Functional impact",
        impact_options,
        default=impact_options,
    )


    frequency_options = sorted(
        df["frequency_class"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    selected_freq = st.multiselect(
        "Population frequency",
        frequency_options,
        default=frequency_options,
    )


    genes = sorted(
        df["gene_symbol"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


    selected_gene = st.selectbox(
        "Gene",
        ["All genes"] + genes,
    )


    score_min = int(
        df["variantpriorx_score"].min()
    )


    score_max = int(
        df["variantpriorx_score"].max()
    )


    score_range = st.slider(
        "VariantPriorX score",
        min_value=score_min,
        max_value=score_max,
        value=(score_min, score_max),
    )


    clinvar_only = st.toggle(
        "ClinVar records only",
        value=False,
    )


    st.divider()

    st.markdown("#### Data sources")

    st.caption(
        "GIAB HG002 · GRCh38\n\n"
        "Ensembl VEP\n\n"
        "ClinVar\n\n"
        "gnomAD"
    )


# ============================================================
# FILTER DATA
# ============================================================

filtered = df[
    df["max_impact"].astype(str).isin(
        selected_impacts
    )
    &
    df["frequency_class"].astype(str).isin(
        selected_freq
    )
    &
    df["variantpriorx_score"].between(
        score_range[0],
        score_range[1],
    )
].copy()


if selected_gene != "All genes":

    filtered = filtered[
        filtered["gene_symbol"].astype(str)
        == selected_gene
    ]


if clinvar_only:

    filtered = filtered[
        filtered["clinvar_id"].notna()
        &
        (
            filtered["clinvar_id"]
            .astype(str)
            != "."
        )
    ]


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero">
    <div class="hero-badge">CLINICAL GENOMICS • VARIANT INTERPRETATION</div>
    <div class="hero-title">VariantPriorX</div>
    <div class="hero-sub">
        Evidence-driven germline variant prioritization integrating
        functional consequence, ClinVar clinical evidence and gnomAD
        population frequency across the GIAB HG002 benchmark genome.
    </div>
</div>
""")


# ============================================================
# KPI VALUES
# ============================================================

total = len(df)

high = int(
    (df["max_impact"] == "HIGH").sum()
)

moderate = int(
    (df["max_impact"] == "MODERATE").sum()
)

clinvar_records = int(
    (
        df["clinvar_id"].notna()
        &
        (
            df["clinvar_id"]
            .astype(str)
            != "."
        )
    ).sum()
)

gnomad_found = int(
    (df["status"] == "FOUND").sum()
)

highest_score = int(
    df["variantpriorx_score"].max()
)


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4, k5, k6 = st.columns(6)


kpis = [
    (k1, "◈", total, "Prioritized variants"),
    (k2, "▲", high, "High impact"),
    (k3, "●", moderate, "Moderate impact"),
    (k4, "✦", clinvar_records, "ClinVar records"),
    (k5, "◎", gnomad_found, "gnomAD matched"),
    (k6, "◆", highest_score, "Highest score"),
]


for col, icon, value, label in kpis:

    with col:

        st.html(
            f"""
            <div class="kpi">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-value">{value:,}</div>
                <div class="kpi-label">{html.escape(label)}</div>
            </div>
            """
        )


# ============================================================
# EVIDENCE LANDSCAPE
# ============================================================

section_header(
    "Portfolio overview",
    "Evidence landscape",
    "Functional severity, population evidence and prioritization behaviour across the candidate set.",
)


chart1, chart2 = st.columns(
    [1.15, 0.85]
)


# ============================================================
# SCORE DISTRIBUTION
# ============================================================

with chart1:

    score_counts = (
        df["variantpriorx_score"]
        .value_counts()
        .sort_index()
        .reset_index()
    )


    score_counts.columns = [
        "VariantPriorX score",
        "Variants",
    ]


    fig_score = px.bar(
        score_counts,
        x="VariantPriorX score",
        y="Variants",
        color="VariantPriorX score",
        color_continuous_scale=[
            "#D75C61",
            "#E5A64E",
            "#6BB394",
            "#7256A0",
        ],
        title="Prioritization score distribution",
    )


    fig_score.update_layout(
        height=400,

        coloraxis_showscale=False,

        plot_bgcolor=
            "rgba(255,255,255,0.40)",

        paper_bgcolor=
            "rgba(0,0,0,0)",

        title_font=dict(
            size=19,
            color="#24493A",
        ),

        font=dict(
            size=13,
            color="#40584D",
        ),

        xaxis=dict(
            gridcolor=
                "rgba(85,110,97,0.10)",
            dtick=1,
        ),

        yaxis=dict(
            gridcolor=
                "rgba(85,110,97,0.13)",
        ),

        margin=dict(
            l=25,
            r=20,
            t=60,
            b=30,
        ),
    )


    st.plotly_chart(
        fig_score,
        use_container_width=True,
    )


# ============================================================
# IMPACT DONUT
# ============================================================

with chart2:

    impact_counts = (
        df["max_impact"]
        .fillna("UNKNOWN")
        .value_counts()
        .reset_index()
    )


    impact_counts.columns = [
        "Impact",
        "Variants",
    ]


    fig_impact = px.pie(
        impact_counts,
        names="Impact",
        values="Variants",
        hole=0.60,
        title="Functional impact composition",
        color="Impact",
        color_discrete_map={
            "HIGH": "#D95858",
            "MODERATE": "#E1A53F",
            "LOW": "#46A18C",
            "MODIFIER": "#735AA0",
            "UNKNOWN": "#9DAAA4",
        },
    )


    fig_impact.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(
            line=dict(
                color="white",
                width=2,
            )
        ),
    )


    fig_impact.update_layout(
        height=400,

        paper_bgcolor=
            "rgba(0,0,0,0)",

        title_font=dict(
            size=19,
            color="#24493A",
        ),

        font=dict(
            size=13,
            color="#40584D",
        ),

        legend_title_text="",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )


    st.plotly_chart(
        fig_impact,
        use_container_width=True,
    )


# ============================================================
# FREQUENCY + CLINVAR
# ============================================================

chart3, chart4 = st.columns(2)


with chart3:

    frequency_order = [
        "VERY_RARE",
        "RARE",
        "LOW_FREQUENCY",
        "UNCOMMON",
        "COMMON",
        "NOT_FOUND",
        "UNRESOLVED",
        "UNKNOWN",
    ]


    frequency_counts = (
        df["frequency_class"]
        .fillna("UNKNOWN")
        .value_counts()
        .reindex(frequency_order)
        .dropna()
        .reset_index()
    )


    frequency_counts.columns = [
        "Frequency class",
        "Variants",
    ]


    fig_frequency = px.bar(
        frequency_counts,
        y="Frequency class",
        x="Variants",
        orientation="h",
        color="Frequency class",
        color_discrete_map={
            "VERY_RARE": "#248D72",
            "RARE": "#48AA88",
            "LOW_FREQUENCY": "#79C29D",
            "UNCOMMON": "#E2AA3E",
            "COMMON": "#D76558",
            "NOT_FOUND": "#70549C",
            "UNRESOLVED": "#A17ABE",
            "UNKNOWN": "#9AA8A1",
        },
        title="Population frequency evidence",
    )


    fig_frequency.update_layout(
        height=430,

        showlegend=False,

        plot_bgcolor=
            "rgba(255,255,255,0.40)",

        paper_bgcolor=
            "rgba(0,0,0,0)",

        title_font=dict(
            size=19,
            color="#24493A",
        ),

        font=dict(
            size=13,
            color="#40584D",
        ),

        xaxis=dict(
            gridcolor=
                "rgba(85,110,97,0.13)",
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=25,
        ),
    )


    st.plotly_chart(
        fig_frequency,
        use_container_width=True,
    )


with chart4:

    clinvar_counts = (
        df["clnsig"]
        .replace(".", pd.NA)
        .fillna("No classification")
        .value_counts()
        .head(8)
        .reset_index()
    )


    clinvar_counts.columns = [
        "Classification",
        "Variants",
    ]


    fig_clinvar = px.bar(
        clinvar_counts.sort_values(
            "Variants"
        ),
        y="Classification",
        x="Variants",
        orientation="h",
        color="Variants",
        color_continuous_scale=[
            "#D7ECDD",
            "#57A88B",
            "#76549D",
        ],
        title="ClinVar evidence profile",
    )


    fig_clinvar.update_layout(
        height=430,

        coloraxis_showscale=False,

        plot_bgcolor=
            "rgba(255,255,255,0.40)",

        paper_bgcolor=
            "rgba(0,0,0,0)",

        title_font=dict(
            size=19,
            color="#24493A",
        ),

        font=dict(
            size=12,
            color="#40584D",
        ),

        xaxis=dict(
            gridcolor=
                "rgba(85,110,97,0.13)",
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=25,
        ),
    )


    st.plotly_chart(
        fig_clinvar,
        use_container_width=True,
    )


# ============================================================
# POPULATION FREQUENCY RELATIONSHIP
# ============================================================

section_header(
    "Evidence relationship",
    "Priority versus population frequency",
    "Relationship between gnomAD allele frequency and the VariantPriorX prioritization score for successfully matched variants.",
)


scatter_df = df[
    (df["status"] == "FOUND")
    &
    df["population_af"].notna()
].copy()


scatter_df["AF for plot"] = (
    scatter_df["population_af"]
    .clip(lower=1e-8)
)


fig_scatter = px.scatter(
    scatter_df,

    x="AF for plot",

    y="variantpriorx_score",

    color="max_impact",

    hover_name="gene_symbol",

    hover_data={
        "variant_id": True,
        "population_af": ":.3e",
        "AF for plot": False,
        "most_severe_consequence": True,
        "frequency_class": True,
    },

    log_x=True,

    color_discrete_map={
        "HIGH": "#D65252",
        "MODERATE": "#DDA33E",
        "LOW": "#3C9A87",
        "MODIFIER": "#71569D",
    },

    labels={
        "AF for plot":
            "gnomAD joint allele frequency",

        "variantpriorx_score":
            "VariantPriorX score",

        "max_impact":
            "Functional impact",
    },
)


fig_scatter.update_traces(
    marker=dict(
        size=9,

        opacity=0.82,

        line=dict(
            width=0.6,
            color="white",
        ),
    )
)


fig_scatter.update_layout(
    height=490,

    plot_bgcolor=
        "rgba(255,255,255,0.44)",

    paper_bgcolor=
        "rgba(0,0,0,0)",

    legend_title_text="Impact",

    font=dict(
        size=13,
        color="#40584D",
    ),

    xaxis=dict(
        gridcolor=
            "rgba(85,110,97,0.13)",
    ),

    yaxis=dict(
        gridcolor=
            "rgba(85,110,97,0.13)",

        dtick=1,
    ),

    margin=dict(
        l=25,
        r=20,
        t=30,
        b=35,
    ),
)


st.plotly_chart(
    fig_scatter,
    use_container_width=True,
)


# ============================================================
# TOP VARIANTS
# ============================================================

section_header(
    "Prioritization",
    "Top-ranked variants",
    "Highest-ranking variants based on integrated functional, clinical and population evidence.",
)


top = (
    df.sort_values(
        [
            "variantpriorx_score",
            "rank",
        ],
        ascending=[
            False,
            True,
        ],
    )
    .head(12)
    .copy()
)


top["label"] = (
    top["gene_symbol"]
    .fillna("Unknown")
    .astype(str)
    +
    " • #"
    +
    top["rank"]
    .astype(int)
    .astype(str)
)


fig_top = px.bar(
    top.sort_values(
        [
            "variantpriorx_score",
            "rank",
        ],
        ascending=[
            True,
            False,
        ],
    ),

    x="variantpriorx_score",

    y="label",

    orientation="h",

    color="max_impact",

    color_discrete_map={
        "HIGH": "#CF5450",
        "MODERATE": "#DCA13C",
        "LOW": "#43978A",
        "MODIFIER": "#71559C",
    },

    hover_data=[
        "variant_id",
        "most_severe_consequence",
        "frequency_class",
        "population_af",
    ],

    labels={
        "variantpriorx_score":
            "Prioritization score",

        "label":
            "",

        "max_impact":
            "Impact",
    },
)


fig_top.update_layout(
    height=510,

    plot_bgcolor=
        "rgba(255,255,255,0.40)",

    paper_bgcolor=
        "rgba(0,0,0,0)",

    legend_title_text="Impact",

    font=dict(
        size=13,
        color="#40584D",
    ),

    xaxis=dict(
        gridcolor=
            "rgba(85,110,97,0.13)",

        dtick=1,
    ),

    margin=dict(
        l=10,
        r=20,
        t=25,
        b=35,
    ),
)


st.plotly_chart(
    fig_top,
    use_container_width=True,
)


# ============================================================
# VARIANT EXPLORER
# ============================================================

section_header(
    "Interactive exploration",
    "Variant explorer",
    "Search, filter and inspect the complete prioritized variant set.",
)


search_term = st.text_input(
    "Search variant, gene or consequence",
    placeholder=
        "Example: CLCN7, RHCE, missense...",
)


if search_term:

    query = (
        search_term
        .strip()
        .lower()
    )


    searchable = (
        filtered[
            [
                "variant_id",
                "gene_symbol",
                "most_severe_consequence",
            ]
        ]
        .fillna("")
        .astype(str)
    )


    search_mask = searchable.apply(
        lambda row:
        row.str.lower()
        .str.contains(
            query,
            regex=False,
        )
        .any(),

        axis=1,
    )


    filtered = filtered[
        search_mask
    ].copy()


st.markdown(
    f"**{len(filtered):,} variants** match the current filters."
)


table_columns = [
    "rank",
    "gene_symbol",
    "variant_id",
    "most_severe_consequence",
    "max_impact",
    "clnsig",
    "population_af",
    "frequency_class",
    "variantpriorx_score",
]


st.dataframe(
    filtered[
        table_columns
    ],

    use_container_width=True,

    hide_index=True,

    height=470,

    column_config={
        "rank":
            st.column_config.NumberColumn(
                "Rank",
                format="%d",
            ),

        "gene_symbol":
            "Gene",

        "variant_id":
            "Variant",

        "most_severe_consequence":
            "Consequence",

        "max_impact":
            "Impact",

        "clnsig":
            "ClinVar",

        "population_af":
            st.column_config.NumberColumn(
                "gnomAD AF",
                format="%.3e",
            ),

        "frequency_class":
            "Frequency",

        "variantpriorx_score":
            st.column_config.NumberColumn(
                "Score",
                format="%d",
            ),
    },
)


download_data = filtered.to_csv(
    index=False,
    sep="\t",
).encode("utf-8")


st.download_button(
    "⬇ Download filtered variants",

    data=download_data,

    file_name=
        "variantpriorx_filtered.tsv",

    mime=
        "text/tab-separated-values",
)


# ============================================================
# VARIANT DETAILS
# ============================================================

section_header(
    "Evidence inspection",
    "Variant detail",
    "Inspect functional annotation, clinical evidence, population frequency and scoring components.",
)


if len(filtered) > 0:

    selected_variant = st.selectbox(
        "Select a variant",
        filtered[
            "variant_id"
        ].tolist(),
    )


    row = filtered[
        filtered["variant_id"]
        == selected_variant
    ].iloc[0]


    gene_name = (
        str(row["gene_symbol"])
        if pd.notna(
            row["gene_symbol"]
        )
        else "Unknown gene"
    )


    safe_gene = html.escape(
        gene_name
    )


    safe_variant = html.escape(
        str(
            row["variant_id"]
        )
    )


    st.html(
        f"""
        <div class="variant-card">
            <div class="variant-small">SELECTED VARIANT</div>
            <div class="variant-title">{safe_gene} &nbsp; • &nbsp; Rank #{int(row["rank"])}</div>
            <div class="variant-id">{safe_variant}</div>
        </div>
        """
    )


    d1, d2, d3, d4 = st.columns(4)


    d1.metric(
        "VariantPriorX score",
        int(
            row["variantpriorx_score"]
        ),
    )


    d2.metric(
        "Functional impact",
        str(
            row["max_impact"]
        ),
    )


    d3.metric(
        "Frequency class",
        str(
            row["frequency_class"]
        ),
    )


    af_text = (
        "Not available"
        if pd.isna(
            row["population_af"]
        )
        else
        f"{row['population_af']:.3e}"
    )


    d4.metric(
        "gnomAD joint AF",
        af_text,
    )


    left, right = st.columns(2)


    # ========================================================
    # FUNCTIONAL ANNOTATION
    # ========================================================

    with left:

        st.markdown(
            "#### Functional annotation"
        )


        functional_table = pd.DataFrame(
            {
                "Field": [
                    "Gene",
                    "Consequence",
                    "Variant class",
                    "Transcript",
                    "MANE Select",
                    "Canonical",
                    "HGVS c.",
                    "HGVS p.",
                ],

                "Value": [
                    row.get(
                        "gene_symbol"
                    ),

                    row.get(
                        "most_severe_consequence"
                    ),

                    row.get(
                        "variant_class"
                    ),

                    row.get(
                        "transcript_id"
                    ),

                    row.get(
                        "mane_select"
                    ),

                    row.get(
                        "canonical"
                    ),

                    row.get(
                        "hgvsc"
                    ),

                    row.get(
                        "hgvsp"
                    ),
                ],
            }
        )


        functional_table["Value"] = (
            functional_table["Value"]
            .fillna("Not available")
            .replace(
                ".",
                "Not available",
            )
        )


        st.dataframe(
            functional_table,

            use_container_width=True,

            hide_index=True,

            height=320,
        )


    # ========================================================
    # CLINICAL / POPULATION EVIDENCE
    # ========================================================

    with right:

        st.markdown(
            "#### Clinical & population evidence"
        )


        clinvar_id = row.get(
            "clinvar_id"
        )


        if (
            pd.isna(
                clinvar_id
            )
            or
            str(
                clinvar_id
            ) == "."
        ):

            clinvar_id = (
                "No matching ClinVar record"
            )


        clinical_table = pd.DataFrame(
            {
                "Field": [
                    "ClinVar ID",
                    "Clinical significance",
                    "Review status",
                    "Condition",
                    "gnomAD status",
                    "Frequency class",
                ],

                "Value": [
                    clinvar_id,

                    row.get(
                        "clnsig"
                    ),

                    row.get(
                        "clnrevstat"
                    ),

                    row.get(
                        "clndn"
                    ),

                    row.get(
                        "status"
                    ),

                    row.get(
                        "frequency_class"
                    ),
                ],
            }
        )


        clinical_table["Value"] = (
            clinical_table["Value"]
            .fillna(
                "Not available"
            )
            .replace(
                ".",
                "Not available",
            )
        )


        st.dataframe(
            clinical_table,

            use_container_width=True,

            hide_index=True,

            height=320,
        )


    # ========================================================
    # SCORE CONTRIBUTION
    # ========================================================

    st.markdown(
        "#### Evidence contribution"
    )


    impact_component = (
        row.get(
            "impact_score",
            0,
        )
    )


    clinvar_component = (
        row.get(
            "clinvar_score",
            0,
        )
    )


    frequency_component = (
        row.get(
            "frequency_score",
            0,
        )
    )


    components = pd.DataFrame(
        {
            "Evidence": [
                "Functional consequence",
                "ClinVar evidence",
                "Population frequency",
            ],

            "Score": [
                0
                if pd.isna(
                    impact_component
                )
                else impact_component,

                0
                if pd.isna(
                    clinvar_component
                )
                else clinvar_component,

                0
                if pd.isna(
                    frequency_component
                )
                else frequency_component,
            ],
        }
    )


    fig_components = go.Figure()


    fig_components.add_trace(
        go.Bar(
            x=
                components[
                    "Evidence"
                ],

            y=
                components[
                    "Score"
                ],

            marker_color=[
                "#319270",
                "#7752A0",
                "#E1A33C",
            ],

            text=
                components[
                    "Score"
                ],

            textposition=
                "outside",
        )
    )


    component_min = min(
        components[
            "Score"
        ].min(),
        0,
    )


    component_max = max(
        components[
            "Score"
        ].max(),
        0,
    )


    fig_components.update_layout(
        height=350,

        yaxis_title=
            "Score contribution",

        xaxis_title="",

        plot_bgcolor=
            "rgba(255,255,255,0.40)",

        paper_bgcolor=
            "rgba(0,0,0,0)",

        showlegend=False,

        font=dict(
            size=13,
            color="#40584D",
        ),

        yaxis=dict(
            gridcolor=
                "rgba(85,110,97,0.13)",

            range=[
                component_min - 1,
                component_max + 1,
            ],

            dtick=1,
        ),

        margin=dict(
            l=25,
            r=20,
            t=30,
            b=35,
        ),
    )


    fig_components.add_hline(
        y=0,

        line_width=1,

        line_color=
            "rgba(70,90,80,0.35)",
    )


    st.plotly_chart(
        fig_components,

        use_container_width=True,
    )


else:

    st.info(
        "No variants match the current filters."
    )


# ============================================================
# DISCLAIMER
# ============================================================

st.html("""
<div class="disclaimer">
    <strong>Research-use disclaimer</strong><br>
    VariantPriorX is an educational and research workflow built using the
    GIAB HG002 benchmark genome. The VariantPriorX score is a transparent
    evidence-prioritization score and is <strong>not</strong> an ACMG/AMP
    classification, medical diagnosis or clinical recommendation.
    gnomAD NOT_FOUND and unresolved records are treated as missing
    population evidence rather than allele frequency zero.
</div>
""")

