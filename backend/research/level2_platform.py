"""
Level 2: Platform Analysis.

Auto-discovers specific platforms/products from the research
configuration's search terms and technology name, then produces a
feature/adoption/competitive-advantage breakdown for each one. This is
the second stage of the three-level ResearchEngine pipeline and answers
"which specific products should we look at, and how do they compare?".

Discovery works in two steps:
  1. Known-platform matching: search terms and the technology name are
     scanned for well-known platform names (e.g. "UiPath", "OpenAI",
     "Kubernetes", "Ethereum") using a curated alias table.
  2. Heuristic candidate extraction: any remaining capitalized token in
     the search terms that isn't a known stop word is treated as a
     candidate platform name and given a generic (but complete) analysis,
     so that platforms outside the knowledge base are still supported.
"""

from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Data models
# --------------------------------------------------------------------------

@dataclass
class PlatformProfile:
    """The full analysis of a single discovered platform."""

    name: str
    domain: str
    features: List[str] = field(default_factory=list)
    adoption_level: str = "unknown"  # widespread, growing, emerging, niche, unknown
    competitive_advantages: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class PlatformAnalysisFindings:
    """The full Level 2 result for a research configuration."""

    technology: str
    discovered_platforms: List[str] = field(default_factory=list)
    profiles: List[PlatformProfile] = field(default_factory=list)
    generated_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# --------------------------------------------------------------------------
# Knowledge base
# --------------------------------------------------------------------------

# Known platform aliases -> canonical name, grouped by technology domain.
# The alias key is matched case-insensitively as a substring of the
# combined search text (search_terms + technology).
_PLATFORM_KB: Dict[str, Dict[str, Any]] = {
    "uipath": {
        "name": "UiPath",
        "domain": "rpa",
        "features": ["Studio/StudioX low-code designer", "Orchestrator for fleet management", "Document Understanding AI", "Marketplace of pre-built automations"],
        "adoption_level": "widespread",
        "competitive_advantages": ["Largest RPA ecosystem and partner network", "Strong enterprise governance tooling"],
    },
    "automation anywhere": {
        "name": "Automation Anywhere",
        "domain": "rpa",
        "features": ["Cloud-native Automation 360 platform", "IQ Bot for cognitive automation", "Bot Store marketplace"],
        "adoption_level": "widespread",
        "competitive_advantages": ["Cloud-first architecture", "Strong AI/ML integration roadmap"],
    },
    "power automate": {
        "name": "Microsoft Power Automate",
        "domain": "rpa",
        "features": ["Cloud flows and desktop flows", "Deep Microsoft 365/Dataverse integration", "AI Builder for cognitive tasks"],
        "adoption_level": "widespread",
        "competitive_advantages": ["Bundled pricing with Microsoft 365 licensing", "Low barrier to entry for existing Microsoft shops"],
    },
    "blue prism": {
        "name": "Blue Prism (SS&C)",
        "domain": "rpa",
        "features": ["Digital Exchange (DX) marketplace", "Strong security/audit model", "Control Room for bot orchestration"],
        "adoption_level": "growing",
        "competitive_advantages": ["Security- and compliance-first design", "Strong presence in regulated industries"],
    },
    "openai": {
        "name": "OpenAI",
        "domain": "ai",
        "features": ["GPT model family", "Assistants/agents API", "Fine-tuning and embeddings API"],
        "adoption_level": "widespread",
        "competitive_advantages": ["Frontier model performance", "Largest developer mindshare"],
    },
    "anthropic": {
        "name": "Anthropic (Claude)",
        "domain": "ai",
        "features": ["Claude model family", "Extended context windows", "Agentic tool-use / computer-use capabilities"],
        "adoption_level": "growing",
        "competitive_advantages": ["Strong coding and agentic task performance", "Safety-focused positioning for enterprise trust"],
    },
    "azure ai": {
        "name": "Microsoft Azure AI",
        "domain": "ai",
        "features": ["Azure OpenAI Service", "Copilot Studio", "Enterprise data governance integration"],
        "adoption_level": "widespread",
        "competitive_advantages": ["Deep enterprise/Azure ecosystem integration", "Simplified compliance story for regulated customers"],
    },
    "gemini": {
        "name": "Google Gemini",
        "domain": "ai",
        "features": ["Multimodal model family", "Vertex AI platform integration", "Long-context reasoning"],
        "adoption_level": "growing",
        "competitive_advantages": ["Tight integration with Google Cloud data services", "Strong multimodal capabilities"],
    },
    "kubernetes": {
        "name": "Kubernetes",
        "domain": "kubernetes",
        "features": ["Declarative workload orchestration", "Self-healing and autoscaling", "Extensible via CRDs/operators"],
        "adoption_level": "widespread",
        "competitive_advantages": ["De facto industry standard", "Massive ecosystem of tooling and vendors"],
    },
    "eks": {
        "name": "Amazon EKS",
        "domain": "kubernetes",
        "features": ["Managed control plane", "Deep AWS service integration", "Fargate serverless option"],
        "adoption_level": "widespread",
        "competitive_advantages": ["Native AWS integration", "Broadest managed-service footprint"],
    },
    "gke": {
        "name": "Google GKE",
        "domain": "kubernetes",
        "features": ["Autopilot fully-managed mode", "Origin implementation of Kubernetes", "Strong multi-cluster tooling"],
        "adoption_level": "widespread",
        "competitive_advantages": ["Deepest Kubernetes engineering expertise", "Autopilot reduces operational overhead"],
    },
    "aks": {
        "name": "Microsoft AKS",
        "domain": "kubernetes",
        "features": ["Managed control plane", "Azure Active Directory integration", "Azure Arc hybrid support"],
        "adoption_level": "widespread",
        "competitive_advantages": ["Tight Azure ecosystem integration", "Strong hybrid/on-prem story via Arc"],
    },
    "openshift": {
        "name": "Red Hat OpenShift",
        "domain": "kubernetes",
        "features": ["Integrated CI/CD pipelines", "Built-in developer console", "Strong hybrid/on-prem support"],
        "adoption_level": "growing",
        "competitive_advantages": ["Enterprise support contracts", "Strong presence in regulated/on-prem environments"],
    },
    "ethereum": {
        "name": "Ethereum",
        "domain": "blockchain",
        "features": ["Smart contract platform", "Largest DeFi/NFT ecosystem", "Layer-2 scaling network"],
        "adoption_level": "widespread",
        "competitive_advantages": ["Largest developer ecosystem", "Deepest liquidity and network effects"],
    },
    "hyperledger": {
        "name": "Hyperledger Fabric",
        "domain": "blockchain",
        "features": ["Permissioned network model", "Pluggable consensus", "Channel-based data privacy"],
        "adoption_level": "niche",
        "competitive_advantages": ["Enterprise/consortium governance fit", "Strong data privacy controls"],
    },
    "corda": {
        "name": "R3 Corda",
        "domain": "blockchain",
        "features": ["Point-to-point transaction model", "Notary-based finality", "Financial services tooling"],
        "adoption_level": "niche",
        "competitive_advantages": ["Purpose-built for regulated financial use cases", "Strong privacy-by-design model"],
    },
    "solana": {
        "name": "Solana",
        "domain": "blockchain",
        "features": ["High-throughput consensus (Proof of History)", "Low transaction costs", "Growing payments ecosystem"],
        "adoption_level": "growing",
        "competitive_advantages": ["High transaction throughput", "Emerging strength in consumer/payments use cases"],
    },
}

# Words that should never be treated as a discovered platform candidate,
# even if capitalized, because they are generic technology/domain terms.
_STOP_WORDS: Set[str] = {
    "rpa", "ai", "ml", "iot", "api", "sdk", "saas", "paas", "iaas",
    "automation", "technology", "platform", "software", "cloud",
    "blockchain", "kubernetes", "artificial", "intelligence", "machine",
    "learning", "data", "analytics", "security", "the", "and", "for", "with",
}

_CANDIDATE_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9\.\+#]*")


# --------------------------------------------------------------------------
# Discovery logic
# --------------------------------------------------------------------------

def _discover_known_platforms(search_text: str) -> List[Dict[str, Any]]:
    """Return knowledge-base entries whose alias appears in `search_text`."""
    text = search_text.lower()
    matched: List[Dict[str, Any]] = []
    seen_names: Set[str] = set()
    for alias, entry in _PLATFORM_KB.items():
        if alias in text and entry["name"] not in seen_names:
            matched.append(entry)
            seen_names.add(entry["name"])
    return matched


def _discover_candidate_tokens(search_terms: str, already_found: Set[str]) -> List[str]:
    """Extract free-text candidate platform names not already matched.

    Heuristic: split on commas/whitespace, keep tokens that look like a
    proper noun (start with an uppercase letter) and are at least 2
    characters, excluding common stop words and anything already covered
    by a known-platform match.
    """
    candidates: List[str] = []
    seen: Set[str] = set(name.lower() for name in already_found)
    for raw_term in re.split(r"[,;]", search_terms or ""):
        term = raw_term.strip()
        if not term:
            continue
        # Multi-word terms (e.g. "Power Automate") are kept whole if they
        # were not already matched by the KB; single generic words are
        # filtered via the stop-word list. A term is also skipped if it is
        # a substring of (or contains) an already-matched known platform
        # name, so e.g. "Hyperledger" doesn't duplicate "Hyperledger Fabric".
        lowered = term.lower()
        if lowered in seen:
            continue
        if lowered in _STOP_WORDS:
            continue
        if any(lowered in known or known in lowered for known in seen):
            continue
        if not _CANDIDATE_TOKEN_RE.match(term):
            continue
        if term[0].isupper() and len(term) > 1:
            candidates.append(term)
            seen.add(lowered)
    return candidates


def _generic_platform_profile(name: str, technology: str) -> PlatformProfile:
    """Build a template-based profile for a platform outside the KB."""
    return PlatformProfile(
        name=name,
        domain=technology,
        features=["Specific feature data not yet catalogued for this platform"],
        adoption_level="unknown",
        competitive_advantages=["Requires further research to identify specific advantages"],
        notes=(
            f"'{name}' was auto-discovered from the search terms but is not "
            f"yet present in the platform knowledge base. This is a generic "
            f"placeholder profile; validate details with a live source before "
            f"relying on it."
        ),
    )


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------

def analyze_platforms(technology: str, search_terms: str = "") -> Dict[str, Any]:
    """Run Level 2 platform analysis for the given research configuration.

    Args:
        technology: The technology or category being researched (e.g. "RPA").
        search_terms: Comma/free-text separated search terms from the
            research configuration (e.g. "RPA, automation, UiPath"), used
            to auto-discover specific platforms to analyze.

    Returns:
        A JSON-compatible dict listing every discovered platform and its
        feature/adoption/competitive-advantage profile. Never raises: any
        internal error is captured and returned as a degraded-but-valid
        result so the overall research pipeline can continue.
    """
    try:
        combined_text = f"{search_terms} {technology}"
        known_profiles_raw = _discover_known_platforms(combined_text)
        known_names = {entry["name"] for entry in known_profiles_raw}

        profiles: List[PlatformProfile] = [
            PlatformProfile(
                name=entry["name"],
                domain=entry["domain"],
                features=list(entry["features"]),
                adoption_level=entry["adoption_level"],
                competitive_advantages=list(entry["competitive_advantages"]),
            )
            for entry in known_profiles_raw
        ]

        candidate_names = _discover_candidate_tokens(search_terms, known_names)
        for candidate in candidate_names:
            profiles.append(_generic_platform_profile(candidate, technology))

        if not profiles:
            # No platforms could be discovered at all (e.g. empty search
            # terms) -- still return a usable, non-empty result.
            profiles.append(_generic_platform_profile(f"{technology} platforms", technology))

        findings = PlatformAnalysisFindings(
            technology=technology,
            discovered_platforms=[p.name for p in profiles],
            profiles=profiles,
            generated_at=datetime.now().isoformat(),
        )
        return findings.to_dict()

    except Exception as exc:  # pragma: no cover - defensive fallback
        logger.exception("Level 2 platform analysis failed for technology=%r", technology)
        return {
            "technology": technology,
            "discovered_platforms": [],
            "profiles": [],
            "generated_at": datetime.now().isoformat(),
            "error": str(exc),
        }
