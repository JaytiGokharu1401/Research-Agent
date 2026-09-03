"""
Level 1: Market Research.

Produces high-level market intelligence for a given technology: adoption
trends, the vendor/competitive landscape, and demand indicators. This is
the first stage of the three-level ResearchEngine pipeline and is meant
to answer "is this technology worth paying attention to, and why?".

The module ships with a curated knowledge base for well-known technology
domains (RPA, AI, Kubernetes, Blockchain, and a few adjacent domains).
Any technology that does not match a known domain still produces a full,
well-structured result via a generic template so that arbitrary/unknown
technologies are supported.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Data models
# --------------------------------------------------------------------------

@dataclass
class MarketTrend:
    """A single observable trend in the technology's market."""

    title: str
    description: str
    momentum: str  # one of: accelerating, steady, emerging, declining


@dataclass
class VendorProfile:
    """A market participant and its competitive standing."""

    name: str
    market_position: str  # one of: leader, challenger, niche, emerging
    strengths: List[str] = field(default_factory=list)


@dataclass
class DemandIndicators:
    """Qualitative signals of market demand for the technology."""

    overall_demand: str  # one of: high, moderate, emerging, niche
    growth_outlook: str
    key_drivers: List[str] = field(default_factory=list)
    audience_relevance: str = ""


@dataclass
class MarketResearchFindings:
    """The full Level 1 result for a single technology."""

    technology: str
    domain: str
    summary: str
    trends: List[MarketTrend] = field(default_factory=list)
    vendors: List[VendorProfile] = field(default_factory=list)
    demand: Optional[DemandIndicators] = None
    generated_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Return a fully JSON-compatible representation."""
        return asdict(self)


# --------------------------------------------------------------------------
# Knowledge base
# --------------------------------------------------------------------------

# Maps free-text technology names/synonyms to a normalized domain key used
# to look up curated market data below.
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
    "llm": "ai",
    "kubernetes": "kubernetes",
    "k8s": "kubernetes",
    "container orchestration": "kubernetes",
    "containers": "kubernetes",
    "blockchain": "blockchain",
    "distributed ledger": "blockchain",
    "web3": "blockchain",
    "crypto": "blockchain",
    "cloud": "cloud",
    "cloud computing": "cloud",
    "cybersecurity": "cybersecurity",
    "security": "cybersecurity",
    "data analytics": "data_analytics",
    "big data": "data_analytics",
    "iot": "iot",
    "internet of things": "iot",
}

_MARKET_KB: Dict[str, Dict[str, Any]] = {
    "rpa": {
        "summary": (
            "Robotic Process Automation is a mature but still-expanding market, "
            "shifting from standalone task automation toward broader "
            "hyperautomation and agentic platforms that combine RPA with AI."
        ),
        "trends": [
            MarketTrend(
                "Convergence with AI/agentic systems",
                "RPA vendors are embedding LLM-based decisioning and document "
                "understanding directly into bots, blurring the line between "
                "RPA and AI orchestration.",
                "accelerating",
            ),
            MarketTrend(
                "Shift to citizen development",
                "Low-code/no-code bot builders are lowering the barrier to "
                "entry, pushing automation ownership out of IT and into "
                "business units.",
                "steady",
            ),
            MarketTrend(
                "Consolidation among vendors",
                "Market consolidation (acquisitions, platform bundling) is "
                "reducing the number of independent RPA-only vendors.",
                "steady",
            ),
            MarketTrend(
                "Governance and center-of-excellence maturity",
                "Enterprises increasingly require centralized bot governance, "
                "security review, and ROI tracking before scaling automation.",
                "emerging",
            ),
        ],
        "vendors": [
            VendorProfile("UiPath", "leader", ["Broad platform", "Strong ecosystem", "Enterprise adoption"]),
            VendorProfile("Automation Anywhere", "leader", ["Cloud-native architecture", "AI integration"]),
            VendorProfile("Microsoft Power Automate", "challenger", ["Bundled with Microsoft 365", "Low entry cost"]),
            VendorProfile("Blue Prism (SS&C)", "niche", ["Security-focused", "Strong governance model"]),
        ],
        "demand": DemandIndicators(
            overall_demand="high",
            growth_outlook="Steady double-digit growth, increasingly framed as part of hyperautomation budgets rather than standalone RPA spend.",
            key_drivers=["Labor cost pressure", "Back-office efficiency mandates", "Compliance and audit trail needs"],
        ),
    },
    "ai": {
        "summary": (
            "Artificial intelligence, and generative AI specifically, is the "
            "fastest-growing enterprise technology category, with adoption "
            "moving rapidly from experimentation to production deployment."
        ),
        "trends": [
            MarketTrend(
                "Enterprise move from pilots to production",
                "Organizations are shifting budget from proof-of-concept AI "
                "projects to production deployments with measurable ROI.",
                "accelerating",
            ),
            MarketTrend(
                "Rise of agentic AI",
                "Multi-step, tool-using AI agents are emerging as the next "
                "capability tier beyond single-turn chat assistants.",
                "accelerating",
            ),
            MarketTrend(
                "Model commoditization at the low end",
                "Smaller, cheaper, open-weight models are closing the gap on "
                "many tasks, pushing differentiation toward tooling and data.",
                "steady",
            ),
            MarketTrend(
                "Regulatory scrutiny increasing",
                "Governments are introducing AI-specific regulation (e.g. the "
                "EU AI Act), raising compliance requirements for deployers.",
                "emerging",
            ),
        ],
        "vendors": [
            VendorProfile("OpenAI", "leader", ["Frontier model performance", "Broad developer ecosystem"]),
            VendorProfile("Anthropic", "leader", ["Safety-focused positioning", "Strong coding/agentic performance"]),
            VendorProfile("Google DeepMind", "leader", ["Deep research bench", "Integrated cloud/data stack"]),
            VendorProfile("Microsoft Azure AI", "challenger", ["Enterprise distribution via Azure/Copilot"]),
        ],
        "demand": DemandIndicators(
            overall_demand="high",
            growth_outlook="Very high growth; AI spend is increasingly treated as a strategic priority rather than a discretionary IT line item.",
            key_drivers=["Productivity gains", "Competitive pressure", "New product capabilities unlocked by generative models"],
        ),
    },
    "kubernetes": {
        "summary": (
            "Kubernetes has become the de facto standard for container "
            "orchestration, with the market now centered on managed "
            "distributions, platform engineering, and multi-cluster operations."
        ),
        "trends": [
            MarketTrend(
                "Platform engineering adoption",
                "Organizations are building internal developer platforms on "
                "top of Kubernetes to abstract its operational complexity.",
                "accelerating",
            ),
            MarketTrend(
                "Multi-cluster and multi-cloud management",
                "Tooling for fleet management across clusters and clouds is "
                "maturing as a distinct product category.",
                "steady",
            ),
            MarketTrend(
                "AI/ML workload scheduling",
                "GPU-aware scheduling and MLOps integration are becoming "
                "core Kubernetes capabilities as AI workloads move on-cluster.",
                "accelerating",
            ),
            MarketTrend(
                "FinOps and cost optimization",
                "Cost visibility and autoscaling tooling are in high demand "
                "as Kubernetes footprints and cloud bills grow.",
                "steady",
            ),
        ],
        "vendors": [
            VendorProfile("Amazon EKS", "leader", ["Deep AWS integration", "Broad managed service reach"]),
            VendorProfile("Google GKE", "leader", ["Origin of Kubernetes", "Strong autopilot/serverless mode"]),
            VendorProfile("Microsoft AKS", "leader", ["Tight Azure/enterprise integration"]),
            VendorProfile("Red Hat OpenShift", "challenger", ["Enterprise support", "Hybrid/on-prem strength"]),
        ],
        "demand": DemandIndicators(
            overall_demand="high",
            growth_outlook="Mature but still growing as remaining monolithic workloads migrate and AI workloads add new demand.",
            key_drivers=["Cloud-native migration", "Scalability requirements", "Multi-cloud portability"],
        ),
    },
    "blockchain": {
        "summary": (
            "Enterprise blockchain has moved past its early hype cycle into "
            "a smaller set of durable use cases, chiefly around asset "
            "tokenization, supply chain provenance, and settlement."
        ),
        "trends": [
            MarketTrend(
                "Real-world asset tokenization",
                "Tokenization of traditional assets (bonds, funds, real "
                "estate) is the fastest-growing enterprise blockchain use case.",
                "accelerating",
            ),
            MarketTrend(
                "Retreat from generic 'blockchain for X' pilots",
                "Many exploratory pilots from 2018-2021 have been shelved in "
                "favor of narrower, ROI-justified deployments.",
                "declining",
            ),
            MarketTrend(
                "Stablecoins entering payments infrastructure",
                "Regulated stablecoins are increasingly used for cross-border "
                "settlement and treasury operations.",
                "accelerating",
            ),
            MarketTrend(
                "Regulatory clarity improving",
                "Clearer regulatory frameworks in major markets are reducing "
                "legal uncertainty for enterprise adoption.",
                "steady",
            ),
        ],
        "vendors": [
            VendorProfile("Ethereum (and L2s)", "leader", ["Largest developer ecosystem", "Deep liquidity"]),
            VendorProfile("Hyperledger Fabric", "niche", ["Permissioned/enterprise focus", "Consortium governance"]),
            VendorProfile("R3 Corda", "niche", ["Financial services focus", "Privacy-preserving design"]),
            VendorProfile("Solana", "challenger", ["High throughput", "Growing payments/consumer use cases"]),
        ],
        "demand": DemandIndicators(
            overall_demand="moderate",
            growth_outlook="Selective growth concentrated in financial services and supply chain, rather than broad horizontal demand.",
            key_drivers=["Settlement cost reduction", "Provenance/traceability requirements", "Tokenized asset liquidity"],
        ),
    },
    "cloud": {
        "summary": "Cloud computing remains the default infrastructure model for new workloads, with growth now concentrated in AI infrastructure and cost optimization.",
        "trends": [
            MarketTrend("AI infrastructure buildout", "Hyperscalers are investing heavily in GPU capacity to meet AI workload demand.", "accelerating"),
            MarketTrend("FinOps maturity", "Cost governance practices are becoming a standard discipline alongside cloud adoption.", "steady"),
            MarketTrend("Sovereign and regional cloud", "Data residency requirements are driving demand for region-specific cloud offerings.", "emerging"),
        ],
        "vendors": [
            VendorProfile("AWS", "leader", ["Largest market share", "Broadest service catalog"]),
            VendorProfile("Microsoft Azure", "leader", ["Enterprise/Microsoft ecosystem integration"]),
            VendorProfile("Google Cloud", "challenger", ["AI/data analytics strength"]),
        ],
        "demand": DemandIndicators(
            overall_demand="high",
            growth_outlook="Continued growth, increasingly driven by AI workloads rather than general migration.",
            key_drivers=["AI compute demand", "Data center consolidation", "Elastic scaling needs"],
        ),
    },
    "cybersecurity": {
        "summary": "Cybersecurity spending continues to grow as threat surfaces expand with cloud, AI, and remote work adoption.",
        "trends": [
            MarketTrend("AI-powered threat detection", "Vendors are embedding AI/ML into detection and response tooling to keep pace with attacker automation.", "accelerating"),
            MarketTrend("Platform consolidation", "Enterprises are consolidating point tools into unified security platforms to reduce tool sprawl.", "steady"),
            MarketTrend("Identity-centric security", "Identity and access management is increasingly treated as the primary security perimeter.", "steady"),
        ],
        "vendors": [
            VendorProfile("CrowdStrike", "leader", ["Cloud-native EDR/XDR", "Strong threat intelligence"]),
            VendorProfile("Microsoft Security", "leader", ["Bundled with enterprise licensing"]),
            VendorProfile("Palo Alto Networks", "leader", ["Broad platform, network + cloud security"]),
        ],
        "demand": DemandIndicators(
            overall_demand="high",
            growth_outlook="Consistent growth driven by regulatory pressure and rising attack volume.",
            key_drivers=["Regulatory compliance", "Ransomware/breach risk", "Cloud attack surface growth"],
        ),
    },
    "data_analytics": {
        "summary": "Data analytics and platforms are converging with AI, as organizations invest in data infrastructure to enable machine learning and generative AI use cases.",
        "trends": [
            MarketTrend("Convergence with AI/ML pipelines", "Analytics platforms increasingly double as the data layer for AI/ML workloads.", "accelerating"),
            MarketTrend("Real-time analytics demand", "Streaming and real-time analytics are growing faster than traditional batch reporting.", "steady"),
        ],
        "vendors": [
            VendorProfile("Snowflake", "leader", ["Cloud data platform", "Strong ecosystem/marketplace"]),
            VendorProfile("Databricks", "leader", ["Lakehouse architecture", "Strong ML/AI tooling"]),
        ],
        "demand": DemandIndicators(
            overall_demand="high",
            growth_outlook="Strong growth as data infrastructure becomes a prerequisite for AI initiatives.",
            key_drivers=["AI/ML data readiness", "Real-time decisioning needs"],
        ),
    },
    "iot": {
        "summary": "IoT adoption is steady and increasingly focused on industrial and operational use cases rather than broad consumer deployments.",
        "trends": [
            MarketTrend("Edge/AI convergence", "AI inference is moving to edge devices to reduce latency and bandwidth costs.", "steady"),
            MarketTrend("Industrial IoT focus", "Growth is concentrated in manufacturing, logistics, and asset monitoring use cases.", "steady"),
        ],
        "vendors": [
            VendorProfile("AWS IoT", "leader", ["Broad device management tooling"]),
            VendorProfile("Siemens", "leader", ["Deep industrial/OT expertise"]),
        ],
        "demand": DemandIndicators(
            overall_demand="moderate",
            growth_outlook="Steady growth concentrated in industrial applications.",
            key_drivers=["Predictive maintenance", "Operational efficiency", "Asset tracking"],
        ),
    },
}


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------

def _normalize_technology(technology: str) -> str:
    """Map a free-text technology name to a normalized domain key.

    Returns the matched domain key (e.g. "rpa") if a known alias is found
    as a substring of the input, otherwise returns "generic" so that any
    technology -- not just the ones in the knowledge base -- still
    produces a complete result.
    """
    text = (technology or "").strip().lower()
    if not text:
        return "generic"
    # Exact alias match first, then substring match (longest alias wins).
    if text in _TECHNOLOGY_ALIASES:
        return _TECHNOLOGY_ALIASES[text]
    matches = [alias for alias in _TECHNOLOGY_ALIASES if alias in text]
    if matches:
        best = max(matches, key=len)
        return _TECHNOLOGY_ALIASES[best]
    return "generic"


def _generic_findings(technology: str) -> Dict[str, Any]:
    """Build a template-based result for a technology outside the KB."""
    name = technology.strip() or "the selected technology"
    return {
        "summary": (
            f"{name} does not yet have curated market data in this engine's "
            f"knowledge base; the findings below use a generic analysis "
            f"template so that research can still proceed for any technology."
        ),
        "trends": [
            MarketTrend(
                f"Growing interest in {name}",
                f"General market attention toward {name} is increasing as "
                f"organizations evaluate it against established alternatives.",
                "emerging",
            ),
            MarketTrend(
                "Early-stage vendor landscape",
                f"The vendor landscape around {name} is still consolidating, "
                f"with no single dominant provider yet established.",
                "emerging",
            ),
        ],
        "vendors": [
            VendorProfile(
                f"Leading {name} providers",
                "emerging",
                ["Specific vendor data not yet catalogued for this technology"],
            ),
        ],
        "demand": DemandIndicators(
            overall_demand="emerging",
            growth_outlook=(
                f"Demand signals for {name} should be validated with live "
                f"market data; this template reflects a cautious, "
                f"not-yet-established baseline."
            ),
            key_drivers=["Requires further research to identify specific drivers"],
        ),
    }


def research_market(
    technology: str,
    search_terms: str = "",
    target_audience: str = "",
    timeline_scope: str = "",
) -> Dict[str, Any]:
    """Run Level 1 market research for the given technology.

    Args:
        technology: The technology or category being researched (e.g. "RPA").
        search_terms: Comma or free-text separated search terms from the
            research configuration; used only to enrich audience framing.
        target_audience: Intended reader of the report (e.g. "manager"),
            used to tailor the audience-relevance note.
        timeline_scope: Requested time horizon for the research (e.g. "1year").

    Returns:
        A JSON-compatible dict containing the Level 1 market research
        findings. Never raises: any internal error is captured and returned
        as a degraded-but-valid result so the overall research pipeline can
        continue.
    """
    try:
        domain = _normalize_technology(technology)
        data = _MARKET_KB.get(domain) or _generic_findings(technology)

        demand = data["demand"]
        if target_audience:
            demand.audience_relevance = (
                f"For a '{target_audience}' audience, focus on the demand "
                f"drivers and growth outlook above rather than deep technical "
                f"vendor detail."
            )
        if timeline_scope:
            demand.growth_outlook += f" (framed for a {timeline_scope} horizon)"

        findings = MarketResearchFindings(
            technology=technology,
            domain=domain,
            summary=data["summary"],
            trends=data["trends"],
            vendors=data["vendors"],
            demand=demand,
            generated_at=datetime.now().isoformat(),
        )
        return findings.to_dict()

    except Exception as exc:  # pragma: no cover - defensive fallback
        logger.exception("Level 1 market research failed for technology=%r", technology)
        return {
            "technology": technology,
            "domain": "error",
            "summary": "Market research could not be completed due to an internal error.",
            "trends": [],
            "vendors": [],
            "demand": None,
            "generated_at": datetime.now().isoformat(),
            "error": str(exc),
        }
