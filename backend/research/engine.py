"""
Research Engine Orchestrator

Coordinates the three-level research pipeline using function-based modules.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

# Import the function-based research modules
from .level1_market import research_market
from .level2_platform import analyze_platforms
from .level3_industry import analyze_industries
from .opportunity_detector import OpportunityDetector
from .report_generator import ReportGenerator

logger = logging.getLogger(__name__)
DEFAULT_RESULTS_DIR = os.path.join("backend", "data", "results")


class ResearchEngine:
    """Orchestrates complete research pipeline using function-based modules"""
    
    def __init__(self, results_dir: str = DEFAULT_RESULTS_DIR) -> None:
        self.results_dir = results_dir
    
    def run_research(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run complete research pipeline:
        1. Level 1: Market Research (research_market function)
        2. Level 2: Platform Analysis (analyze_platforms function)
        3. Level 3: Industry Analysis (analyze_industries function)
        4. Opportunity Detection
        5. Report Generation
        
        Args:
            config: Research configuration dict
        
        Returns:
            Complete research report
        """
        started_at = datetime.now()
        
        technology = config.get("technology", "")
        search_terms = config.get("search_terms", "")
        target_audience = config.get("target_audience", "")
        timeline_scope = config.get("timeline_scope", "")
        config_id = config.get("id", "")
        
        logger.info(f"Starting research for {technology}")
        print(f"\n{'='*60}")
        print(f"🚀 STARTING RESEARCH: {technology}")
        print(f"{'='*60}\n")
        
        try:
            # LEVEL 1: Market Research
            print(f"📊 Running Level 1: Market Research...")
            level1_findings = research_market(technology, search_terms, target_audience, timeline_scope)
            print(f"   ✅ Level 1 Complete")
            
            # Extract vendors for Level 2
            vendors = level1_findings.get('vendors', [])
            if vendors and isinstance(vendors[0], dict):
                vendors = [v.get('name', '') for v in vendors]
            
            # LEVEL 2: Platform Analysis
            print(f"\n🔧 Running Level 2: Platform Analysis...")
            level2_findings = analyze_platforms(technology, search_terms)
            print(f"   ✅ Level 2 Complete")
            
            # LEVEL 3: Industry Analysis
            industries = ['Healthcare', 'Finance', 'Manufacturing', 'Insurance', 'Retail']
            print(f"\n🏢 Running Level 3: Industry Analysis...")
            level3_findings = analyze_industries(technology)
            print(f"   ✅ Level 3 Complete")
            
            # Combine all research levels
            research_data = {
                "config_id": config_id,
                "technology": technology,
                "generated_at": datetime.now().isoformat(),
                "duration_seconds": (datetime.now() - started_at).total_seconds(),
                "levels": {
                    "market_research": level1_findings,
                    "platform_analysis": level2_findings,
                    "industry_analysis": level3_findings
                },
                "status": "completed"
            }
            
            # OPPORTUNITY DETECTION
            print(f"\n🎯 DETECTING OPPORTUNITIES...")
            opportunity_detector = OpportunityDetector()
            opportunities = opportunity_detector.detect(research_data, config)
            research_data["opportunities"] = opportunities
            
            # REPORT GENERATION
            print(f"\n📄 GENERATING REPORT...")
            report_generator = ReportGenerator()
            report = report_generator.generate(research_data, opportunities, config)
            research_data["report"] = report
            
            print(f"\n{'='*60}")
            print(f"✅ RESEARCH COMPLETE")
            print(f"{'='*60}\n")
            
            logger.info(f"Research completed successfully for {technology}")
            return research_data
            
        except Exception as e:
            logger.exception(f"Error during research: {e}")
            print(f"\n❌ ERROR: {str(e)}\n")
            raise
    
    def save_results(self, report: Dict[str, Any], results_dir: Optional[str] = None) -> str:
        """
        Persist research results as JSON file
        
        Args:
            report: The report dict from run_research()
            results_dir: Optional override for destination directory
        
        Returns:
            Full file path where report was saved
        """
        target_dir = results_dir or self.results_dir
        os.makedirs(target_dir, exist_ok=True)
        
        config_id = report.get("config_id", "unknown")
        file_path = os.path.join(target_dir, f"{config_id}_research.json")
        
        with open(file_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Saved research results to {file_path}")
        print(f"✅ Research saved to: {file_path}\n")
        
        return file_path
    
    def run_and_save(self, config: Dict[str, Any], results_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Convenience wrapper: Run research and automatically save results
        
        Args:
            config: Research configuration
            results_dir: Optional override for destination directory
        
        Returns:
            Complete research report dict
        """
        report = self.run_research(config)
        self.save_results(report, results_dir)
        return report