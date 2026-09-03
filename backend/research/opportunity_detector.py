"""
Opportunity Detector
Analyzes research findings to identify business opportunities for PalTech
"""

import json
from datetime import datetime
from typing import Dict, List

class OpportunityDetector:
    """Detects business opportunities from research findings"""
    
    def __init__(self):
        self.opportunities = {}
    
    def detect(self, research_data: Dict, config: Dict) -> Dict:
        """
        Detect opportunities from research findings
        
        Args:
            research_data: Complete research from all 3 levels
            config: Research configuration
        
        Returns:
            Dictionary with 5 types of opportunities
        """
        
        print(f"\n🎯 OPPORTUNITY DETECTION")
        print("=" * 60)
        
        technology = config.get('technology', 'Unknown')
        
        # Extract findings
        market_findings = research_data.get('levels', {}).get('market_research', {})
        platform_findings = research_data.get('levels', {}).get('platform_analysis', {})
        industry_findings = research_data.get('levels', {}).get('industry_analysis', {})
        
        # Detect each opportunity type
        market_opps = self._detect_market_opportunities(technology, market_findings)
        project_opps = self._detect_project_opportunities(technology, industry_findings)
        capability_opps = self._detect_capability_opportunities(technology, platform_findings)
        sales_opps = self._detect_sales_opportunities(technology, industry_findings, market_findings)
        competitive_opps = self._detect_competitive_positioning(technology, market_findings)
        
        self.opportunities = {
            "detected_at": datetime.now().isoformat(),
            "technology": technology,
            "market_opportunities": market_opps,
            "project_opportunities": project_opps,
            "capability_opportunities": capability_opps,
            "sales_opportunities": sales_opps,
            "competitive_positioning": competitive_opps,
            "total_opportunities": len(market_opps) + len(project_opps) + len(capability_opps) + len(sales_opps) + len(competitive_opps)
        }
        
        print(f"✅ Opportunity Detection Complete")
        print(f"   Market Opportunities: {len(market_opps)}")
        print(f"   Project Opportunities: {len(project_opps)}")
        print(f"   Capability Opportunities: {len(capability_opps)}")
        print(f"   Sales Opportunities: {len(sales_opps)}")
        print(f"   Competitive Positioning: {len(competitive_opps)}")
        print(f"   Total: {self.opportunities['total_opportunities']}")
        
        return self.opportunities
    
    def _detect_market_opportunities(self, technology: str, market_data: Dict) -> List[Dict]:
        """
        Market Opportunities: Where is demand growing?
        """
        opportunities = []
        
        try:
            demand = market_data.get('demand', {})
            trends = market_data.get('trends', [])
            
            # Analyze demand trends
            if demand.get('overall_demand') == 'high':
                opportunities.append({
                    "title": f"High Market Demand for {technology}",
                    "description": demand.get('growth_outlook', ''),
                    "potential": "high",
                    "timeline": "immediate",
                    "key_drivers": demand.get('key_drivers', [])
                })
            
            # Analyze technology trends
            for trend in trends:
                if trend.get('momentum') in ['accelerating', 'steady']:
                    opportunities.append({
                        "title": f"{trend.get('title', 'Trend')} in {technology} Market",
                        "description": trend.get('description', ''),
                        "potential": "medium-high",
                        "timeline": "6-12 months",
                        "momentum": trend.get('momentum', '')
                    })
            
            # Add convergence opportunity
            opportunities.append({
                "title": f"{technology} + AI Convergence Opportunity",
                "description": "Market is shifting toward AI-augmented automation. Organizations adopting this early gain competitive advantage.",
                "potential": "high",
                "timeline": "immediate",
                "action": "Position PalTech as AI-augmented automation provider"
            })
            
        except Exception as e:
            print(f"  ⚠️ Error detecting market opportunities: {e}")
        
        return opportunities[:5]  # Top 5
    
    def _detect_project_opportunities(self, technology: str, industry_data: Dict) -> List[Dict]:
        """
        Project Opportunities: What projects could emerge?
        """
        opportunities = []
        
        try:
            industries = industry_data.get('industries', [])
            
            for industry in industries:
                industry_name = industry.get('industry', '')
                use_cases = industry.get('use_cases', [])
                industry_opps = industry.get('opportunities', [])
                
                for opp in industry_opps:
                    if opp.get('impact') in ['high', 'medium']:
                        opportunities.append({
                            "title": f"{industry_name}: {opp.get('title', 'Automation Project')}",
                            "description": opp.get('description', ''),
                            "industry": industry_name,
                            "potential_revenue": f"${500}K - ${5}M",
                            "timeline": "3-6 months implementation",
                            "related_use_cases": use_cases[:2],
                            "impact": opp.get('impact', '')
                        })
            
            # Add top opportunities
            opportunities = sorted(opportunities, key=lambda x: x.get('impact', ''), reverse=True)
            
        except Exception as e:
            print(f"  ⚠️ Error detecting project opportunities: {e}")
        
        return opportunities[:5]  # Top 5
    
    def _detect_capability_opportunities(self, technology: str, platform_data: Dict) -> List[Dict]:
        """
        Capability Opportunities: What skills should PalTech build?
        """
        opportunities = []
        
        try:
            platforms = platform_data.get('profiles', [])
            
            for platform in platforms:
                platform_name = platform.get('name', '')
                features = platform.get('features', [])
                
                opportunities.append({
                    "title": f"Build {platform_name} Expertise & Certifications",
                    "description": f"Develop deep expertise in {platform_name} platform and key features",
                    "platform": platform_name,
                    "key_features": features[:3],
                    "skill_gaps": [
                        f"{platform_name} development skills",
                        f"Bot design & architecture",
                        "Governance & best practices"
                    ],
                    "business_impact": "Differentiate PalTech as {platform} specialist",
                    "investment": "Training, certification, lab environment"
                })
            
            # Add AI integration capability
            opportunities.append({
                "title": "AI/LLM Integration Capabilities",
                "description": "Build capabilities to integrate LLMs and AI into automation solutions",
                "technology": f"{technology} + AI",
                "key_skills": [
                    "LLM API integration",
                    "Prompt engineering",
                    "AI model management",
                    "Ethical AI considerations"
                ],
                "business_impact": "Position for next-generation hyperautomation market",
                "investment": "R&D, training, partnerships with AI vendors"
            })
            
        except Exception as e:
            print(f"  ⚠️ Error detecting capability opportunities: {e}")
        
        return opportunities[:5]  # Top 5
    
    def _detect_sales_opportunities(self, technology: str, industry_data: Dict, market_data: Dict) -> List[Dict]:
        """
        Sales Opportunities: What should PalTech offer to which industries?
        """
        opportunities = []
        
        try:
            industries = industry_data.get('industries', [])
            vendors = market_data.get('vendors', [])
            
            for industry in industries:
                industry_name = industry.get('industry', '')
                use_cases = industry.get('use_cases', [])
                investment_trends = industry.get('investment_trends', [])
                
                trend_desc = investment_trends[0].get('rationale', '') if investment_trends else ''
                
                opportunities.append({
                    "title": f"Target {industry_name} Industry for {technology} Services",
                    "description": f"Offer implementation, optimization, and managed services for {technology} in {industry_name}",
                    "industry": industry_name,
                    "target_market_size": "500M+ annually",
                    "key_use_cases": use_cases[:2],
                    "investment_trend": trend_desc,
                    "go_to_market": [
                        f"Develop {industry_name} industry playbook",
                        f"Build partnerships with {industry_name} ISVs",
                        f"Create pre-built {industry_name} solutions"
                    ],
                    "estimated_deal_value": "$500K - $5M per engagement"
                })
            
        except Exception as e:
            print(f"  ⚠️ Error detecting sales opportunities: {e}")
        
        return opportunities[:5]  # Top 5
    
    def _detect_competitive_positioning(self, technology: str, market_data: Dict) -> List[Dict]:
        """
        Competitive Positioning: Why should customers choose PalTech?
        """
        opportunities = []
        
        try:
            vendors = market_data.get('vendors', [])
            trends = market_data.get('trends', [])
            
            # Find market gaps
            opportunities.append({
                "title": "SMB Market Gap - Accessible Automation",
                "description": "Most {technology} vendors target enterprises. SMBs are underserved.",
                "positioning": "PalTech as affordable, scalable {technology} provider for mid-market",
                "competitive_advantage": [
                    "Lower TCO than enterprise platforms",
                    "Easier deployment and training",
                    "Stronger support for SMB-sized teams"
                ],
                "target_segment": "100-1000 employee companies",
                "market_size": "$2B+ TAM"
            })
            
            # AI differentiation
            opportunities.append({
                "title": "AI-Augmented Automation Leadership",
                "description": "Vendors are converging on {technology} + AI. Be the leader.",
                "positioning": "PalTech as AI-first, {technology}-second automation provider",
                "competitive_advantage": [
                    "Purpose-built for modern LLM integration",
                    "Intelligent decision-making in bots",
                    "Natural language bot configuration"
                ],
                "differentiation": "While competitors add AI, PalTech is born from AI",
                "market_leadership": "First-mover advantage in AI-native automation"
            })
            
            # Industry specialization
            opportunities.append({
                "title": "Vertical Specialization Strategy",
                "description": "Build deep expertise in 1-2 high-value industries",
                "positioning": "PalTech as industry-specialist, not generalist",
                "recommended_verticals": ["Healthcare", "Financial Services"],
                "competitive_advantage": [
                    "Pre-built, compliance-ready solutions",
                    "Industry-specific best practices",
                    "Regulatory expertise built-in"
                ],
                "business_model": "Premium pricing for specialized solutions"
            })
            
        except Exception as e:
            print(f"  ⚠️ Error detecting competitive positioning: {e}")
        
        return opportunities[:3]  # Top 3
    
    def get_opportunities(self) -> Dict:
        """Return detected opportunities"""
        return self.opportunities