import pandas as pd

class RecommendationEngine:
    def __init__(self, workforce_df, operations_df):
        self.wf = workforce_df
        self.op = operations_df
        
    def analyze_priorities(self):
        """
        Analyzes the datasets and returns a list of recommendation dictionaries.
        """
        recommendations = []
        
        # 1. Analyze Polyvalence (Skill Risk)
        sector_poly = self.wf.groupby("Sector")["Polyvalence_Score"].mean()
        for sector, score in sector_poly.items():
            if score < 50:
                recommendations.append({
                    "Sector": sector,
                    "Priority": "High",
                    "Methodology": "Skill Matrix",
                    "Type": "Training",
                    "Message": f"Low average polyvalence ({score:.1f}%). Critical risk of knowledge loss.",
                    "Action": "Initiate cross-training program immediately."
                })
                
        # 2. Analyze Operational Efficiency (Lean)
        if not self.op.empty:
            sector_eff = self.op.groupby("Sector")["Efficiency_Pct"].mean()
            for sector, eff in sector_eff.items():
                if eff < 85:
                    recommendations.append({
                        "Sector": sector,
                        "Priority": "Medium",
                        "Methodology": "Lean / Kaizen",
                        "Type": "Process",
                        "Message": f"Low efficiency ({eff:.1f}%). Potential Muda (Waste) detected.",
                        "Action": "Conduct Gemba Walk needed to identify bottlenecks."
                    })

        # 3. Analyze Incidents (Safety/5S)
        if not self.op.empty:
            sector_incidents = self.op.groupby("Sector")["Incidents"].sum()
            for sector, count in sector_incidents.items():
                if count > 3: # Arbitrary threshold
                    recommendations.append({
                        "Sector": sector,
                        "Priority": "Critical",
                        "Methodology": "5S / Safety",
                        "Type": "Organization",
                        "Message": f"High incident frequency ({count} incidents). Workspace operational risk.",
                        "Action": "Review 5S implementation and standard operating procedures (SOP)."
                    })
                    
        return pd.DataFrame(recommendations)
