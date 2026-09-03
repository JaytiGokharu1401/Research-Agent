"""
Level 3: Industry Analysis.

Analyzes how a given technology applies across a fixed set of target
industries (Healthcare, Finance, Manufacturing, Insurance, Retail),
producing use cases, adoption opportunities, and investment trends for
each. This is the third and final stage of the ResearchEngine pipeline
and answers "where and how should this technology be applied?".

Like the other levels, this module supports any technology: industries
outside the curated knowledge base combination still receive a complete,
generically-templated analysis rather than being skipped.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Data models
# --------------------------------------------------------------------------

@dataclass
class IndustryOpportunity:
    """A single adoption opportunity within an industry."""

    title: str
    description: str
    impact: str  # one of: high, medium, low


@dataclass
class InvestmentTrend:
    """A qualitative investment-trend signal for an industry."""

    trend: str
    rationale: str


@dataclass
class IndustryProfile:
    """The full Level 3 result for a single industry."""

    industry: str
    use_cases: List[str] = field(default_factory=list)
    opportunities: List[IndustryOpportunity] = field(default_factory=list)
    investment_trends: List[InvestmentTrend] = field(default_factory=list)
    regulatory_considerations: List[str] = field(default_factory=list)


@dataclass
class IndustryAnalysisFindings:
    """The full Level 3 result across all target industries."""

    technology: str
    industries: List[IndustryProfile] = field(default_factory=list)
    generated_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# --------------------------------------------------------------------------
# Fixed target industries
# --------------------------------------------------------------------------

TARGET_INDUSTRIES: List[str] = [
    "Healthcare",
    "Finance",
    "Manufacturing",
    "Insurance",
    "Retail",
]


# --------------------------------------------------------------------------
# Knowledge base
# --------------------------------------------------------------------------
# Keyed by (technology_domain, industry). Technology domains reuse the same
# normalization as level1/level2 (rpa, ai, kubernetes, blockchain, generic).

_TECHNOLOGY_ALIASES: Dict[str, str] = {
    "rpa": "rpa",
    "robotic process automation": "rpa",
    "automation": "rpa",
    "ai": "ai",
    "artificial intelligence": "ai",
    "machine learning": "ai",
    "ml": "ai",
    "generative ai": "ai",
    "genai": "ai",
    "kubernetes": "kubernetes",
    "k8s": "kubernetes",
    "container orchestration": "kubernetes",
    "blockchain": "blockchain",
    "distributed ledger": "blockchain",
    "web3": "blockchain",
}

_INDUSTRY_KB: Dict[str, Dict[str, Dict[str, Any]]] = {
    "rpa": {
        "Healthcare": {
            "use_cases": ["Patient intake and eligibility verification", "Claims pre-processing", "Appointment scheduling automation"],
            "opportunities": [("Back-office cost reduction", "Automating high-volume administrative tasks frees clinical staff capacity.", "high")],
            "investment_trends": [("Steady adoption growth", "Health systems are prioritizing administrative automation to offset staffing shortages.")],
            "regulatory_considerations": ["HIPAA compliance for any bot handling PHI"],
        },
        "Finance": {
            "use_cases": ["Reconciliation and reporting", "KYC/AML document processing", "Loan application processing"],
            "opportunities": [("Compliance-driven automation", "Regulatory reporting volume makes automation a high-ROI target.", "high")],
            "investment_trends": [("Mature, budget-line spend", "RPA is an established line item in most large financial institutions' automation budgets.")],
            "regulatory_considerations": ["SOX and financial audit trail requirements"],
        },
        "Manufacturing": {
            "use_cases": ["Supply chain order processing", "Inventory reconciliation", "Quality report generation"],
            "opportunities": [("ERP-adjacent automation", "Bridging gaps between legacy ERP systems without custom integration work.", "medium")],
            "investment_trends": [("Growing interest via hyperautomation", "Manufacturers are pairing RPA with IoT sensor data for broader automation.")],
            "regulatory_considerations": ["Traceability requirements in regulated sub-sectors (e.g. aerospace, pharma)"],
        },
        "Insurance": {
            "use_cases": ["Claims intake and triage", "Policy issuance", "Underwriting data collection"],
            "opportunities": [("Claims cycle time reduction", "Automating first-notice-of-loss steps materially shortens claims cycles.", "high")],
            "investment_trends": [("High and sustained investment", "Claims automation remains one of the highest-ROI RPA use cases in the industry.")],
            "regulatory_considerations": ["State/national insurance regulatory reporting requirements"],
        },
        "Retail": {
            "use_cases": ["Order processing and returns", "Inventory synchronization across channels", "Price/catalog updates"],
            "opportunities": [("Omnichannel back-office consistency", "Automation keeps inventory and pricing consistent across online/in-store channels.", "medium")],
            "investment_trends": [("Seasonal-spike driven investment", "Retailers invest ahead of peak seasons to absorb order-volume spikes without added headcount.")],
            "regulatory_considerations": ["Consumer data handling regulations for order/returns automation"],
        },
    },
    "ai": {
        "Healthcare": {
            "use_cases": ["Clinical documentation assistance", "Medical imaging analysis", "Patient triage chatbots"],
            "opportunities": [("Clinician time savings", "Ambient documentation tools reduce administrative burden on clinicians.", "high")],
            "investment_trends": [("Rapidly increasing investment", "Health systems are piloting generative AI for documentation and diagnostics support.")],
            "regulatory_considerations": ["FDA oversight for clinical decision-support tools", "HIPAA for any patient data processing"],
        },
        "Finance": {
            "use_cases": ["Fraud detection", "Algorithmic research/summarization", "Customer service copilots"],
            "opportunities": [("Real-time fraud detection", "ML models materially outperform rules-based fraud detection at scale.", "high")],
            "investment_trends": [("High investment, cautious deployment", "Institutions are investing heavily but deploying carefully due to model-risk requirements.")],
            "regulatory_considerations": ["Model risk management requirements", "Explainability requirements for credit decisions"],
        },
        "Manufacturing": {
            "use_cases": ["Predictive maintenance", "Defect detection via computer vision", "Demand forecasting"],
            "opportunities": [("Downtime reduction", "Predictive maintenance models reduce unplanned equipment downtime.", "high")],
            "investment_trends": [("Growing, ROI-driven investment", "Investment is concentrated where AI has clear, measurable operational impact.")],
            "regulatory_considerations": ["Safety certification requirements for AI-assisted quality control"],
        },
        "Insurance": {
            "use_cases": ["Underwriting risk scoring", "Claims fraud detection", "Automated damage assessment from images"],
            "opportunities": [("Underwriting speed and accuracy", "AI risk models speed up underwriting while improving pricing accuracy.", "high")],
            "investment_trends": [("Strong investment in claims AI", "Image-based damage assessment is a fast-growing investment area.")],
            "regulatory_considerations": ["Anti-discrimination requirements in AI-driven underwriting/pricing"],
        },
        "Retail": {
            "use_cases": ["Personalized recommendations", "Demand forecasting", "AI-powered customer service"],
            "opportunities": [("Conversion rate improvement", "Personalization engines directly increase conversion and basket size.", "high")],
            "investment_trends": [("Sustained, competitive investment", "Retailers view AI-driven personalization as a competitive necessity.")],
            "regulatory_considerations": ["Consumer data privacy regulations for personalization"],
        },
    },
    "kubernetes": {
        "Healthcare": {
            "use_cases": ["Scalable hosting for patient-facing portals", "Interoperability (FHIR) service hosting"],
            "opportunities": [("Modernizing legacy health IT", "Containerization supports modernization of aging health IT systems.", "medium")],
            "investment_trends": [("Gradual, modernization-driven investment", "Adoption tracks broader digital health modernization initiatives.")],
            "regulatory_considerations": ["HIPAA-compliant hosting/network segmentation requirements"],
        },
        "Finance": {
            "use_cases": ["Scalable trading/risk platforms", "Microservices hosting for digital banking"],
            "opportunities": [("Resilience and scalability", "Kubernetes supports the high-availability requirements of financial platforms.", "high")],
            "investment_trends": [("Established, ongoing investment", "Kubernetes is a standard part of financial services' cloud-native strategy.")],
            "regulatory_considerations": ["Data residency and audit requirements for regulated workloads"],
        },
        "Manufacturing": {
            "use_cases": ["Edge computing for factory-floor systems", "Hosting IoT data pipelines"],
            "opportunities": [("Edge-to-cloud consistency", "Kubernetes provides a consistent operating model from edge to cloud.", "medium")],
            "investment_trends": [("Emerging investment via edge/IoT", "Adoption is growing alongside industrial IoT initiatives.")],
            "regulatory_considerations": ["Operational technology (OT) network isolation requirements"],
        },
        "Insurance": {
            "use_cases": ["Scalable claims processing platforms", "Digital policy portal hosting"],
            "opportunities": [("Digital channel scalability", "Supports scaling digital self-service channels during demand spikes.", "medium")],
            "investment_trends": [("Steady modernization investment", "Investment tracks broader core-system modernization efforts.")],
            "regulatory_considerations": ["Data residency requirements for policyholder data"],
        },
        "Retail": {
            "use_cases": ["E-commerce platform scaling", "Point-of-sale/inventory microservices"],
            "opportunities": [("Peak-season scalability", "Autoscaling handles seasonal traffic spikes without over-provisioning.", "high")],
            "investment_trends": [("High investment ahead of peak seasons", "Retailers invest in cloud-native scalability ahead of major shopping events.")],
            "regulatory_considerations": ["PCI-DSS considerations for payment-handling services"],
        },
    },
    "blockchain": {
        "Healthcare": {
            "use_cases": ["Supply chain provenance for pharmaceuticals", "Patient consent/record audit trails"],
            "opportunities": [("Drug supply chain integrity", "Blockchain-based provenance reduces counterfeit drug risk.", "medium")],
            "investment_trends": [("Selective, pilot-stage investment", "Adoption remains limited to targeted supply-chain pilots.")],
            "regulatory_considerations": ["HIPAA implications for any patient data anchored on-chain"],
        },
        "Finance": {
            "use_cases": ["Cross-border settlement", "Tokenized assets/securities", "Trade finance documentation"],
            "opportunities": [("Settlement cost/time reduction", "Tokenization and stablecoin rails reduce settlement times from days to minutes.", "high")],
            "investment_trends": [("Growing investment in tokenization", "Real-world asset tokenization is the fastest-growing enterprise blockchain use case.")],
            "regulatory_considerations": ["Securities regulation for tokenized assets", "AML/KYC requirements for on-chain transactions"],
        },
        "Manufacturing": {
            "use_cases": ["Supply chain provenance and traceability", "Multi-party logistics coordination"],
            "opportunities": [("Provenance verification", "Shared ledgers reduce disputes across multi-party supply chains.", "medium")],
            "investment_trends": [("Limited, targeted investment", "Adoption is concentrated in high-value, traceability-critical supply chains.")],
            "regulatory_considerations": ["Cross-border trade compliance for shared ledger data"],
        },
        "Insurance": {
            "use_cases": ["Parametric insurance smart contracts", "Reinsurance settlement automation"],
            "opportunities": [("Parametric claims automation", "Smart contracts can auto-trigger payouts based on verified external data.", "medium")],
            "investment_trends": [("Niche but growing", "Parametric insurance is a small but expanding blockchain use case.")],
            "regulatory_considerations": ["Insurance regulatory approval for automated payout mechanisms"],
        },
        "Retail": {
            "use_cases": ["Product authenticity/anti-counterfeiting", "Loyalty program tokenization"],
            "opportunities": [("Authenticity verification", "Blockchain provenance helps combat counterfeit goods in luxury/high-value retail.", "medium")],
            "investment_trends": [("Niche investment", "Adoption is concentrated among luxury and high-value goods retailers.")],
            "regulatory_considerations": ["Consumer protection rules for loyalty-token programs"],
        },
    },
}


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------

def _normalize_technology(technology: str) -> str:
    """Map a free-text technology name to a normalized domain key."""
    text = (technology or "").strip().lower()
    if not text:
        return "generic"
    if text in _TECHNOLOGY_ALIASES:
        return _TECHNOLOGY_ALIASES[text]
    matches = [alias for alias in _TECHNOLOGY_ALIASES if alias in text]
    if matches:
        best = max(matches, key=len)
        return _TECHNOLOGY_ALIASES[best]
    return "generic"


def _generic_industry_profile(technology: str, industry: str) -> IndustryProfile:
    """Build a template-based industry profile for a technology/industry
    pairing that isn't in the curated knowledge base."""
    name = technology.strip() or "the selected technology"
    return IndustryProfile(
        industry=industry,
        use_cases=[
            f"Process automation opportunities for {name} in {industry}",
            f"Data-driven decision support using {name} in {industry}",
        ],
        opportunities=[
            IndustryOpportunity(
                title=f"Early-mover advantage in {industry}",
                description=(
                    f"Specific {name} use cases for {industry} are not yet "
                    f"catalogued in this engine's knowledge base; further "
                    f"domain-specific research is recommended."
                ),
                impact="medium",
            )
        ],
        investment_trends=[
            InvestmentTrend(
                trend="Investment trend not yet catalogued",
                rationale=(
                    f"No curated investment data exists for {name} in "
                    f"{industry}; validate with live market sources."
                ),
            )
        ],
        regulatory_considerations=[
            f"Review industry-specific regulations applicable to {industry} "
            f"before deploying {name} solutions."
        ],
    )


def analyze_industries(technology: str) -> Dict[str, Any]:
    """Run Level 3 industry analysis across the fixed target industries.

    Args:
        technology: The technology or category being researched (e.g. "RPA").

    Returns:
        A JSON-compatible dict with one profile per entry in
        `TARGET_INDUSTRIES` (Healthcare, Finance, Manufacturing, Insurance,
        Retail). Never raises: any internal error is captured and returned
        as a degraded-but-valid result so the overall research pipeline can
        continue.
    """
    try:
        domain = _normalize_technology(technology)
        domain_kb = _INDUSTRY_KB.get(domain, {})

        profiles: List[IndustryProfile] = []
        for industry in TARGET_INDUSTRIES:
            entry = domain_kb.get(industry)
            if entry is None:
                profiles.append(_generic_industry_profile(technology, industry))
                continue

            profiles.append(
                IndustryProfile(
                    industry=industry,
                    use_cases=list(entry["use_cases"]),
                    opportunities=[
                        IndustryOpportunity(title=t, description=d, impact=i)
                        for (t, d, i) in entry["opportunities"]
                    ],
                    investment_trends=[
                        InvestmentTrend(trend=t, rationale=r)
                        for (t, r) in entry["investment_trends"]
                    ],
                    regulatory_considerations=list(entry["regulatory_considerations"]),
                )
            )

        findings = IndustryAnalysisFindings(
            technology=technology,
            industries=profiles,
            generated_at=datetime.now().isoformat(),
        )
        return findings.to_dict()

    except Exception as exc:  # pragma: no cover - defensive fallback
        logger.exception("Level 3 industry analysis failed for technology=%r", technology)
        return {
            "technology": technology,
            "industries": [],
            "generated_at": datetime.now().isoformat(),
            "error": str(exc),
        }
