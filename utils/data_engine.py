import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

class DataEngine:
    def __init__(self):
        self.sectors = ["Assembly A", "Assembly B", "Machining", "Quality Control", "Logistics", "Maintenance"]
        self.roles = ["Operator", "Senior Operator", "Team Leader", "Technician", "Supervisor"]
        self.categories = ["L1", "L2", "L3", "L4"]
        
    def generate_workforce_data(self, n_employees=150):
        """Generates a simulated dataset for workforce demographics and performance"""
        data = []
        for i in range(1, n_employees + 1):
            sector = random.choice(self.sectors)
            role = random.choice(self.roles)
            seniority = random.randint(1, 25)
            
            # Logic: Seniority usually correlates with Category and Role
            if seniority > 10:
                cat = "L4"
                if random.random() > 0.6: role = "Supervisor"
            elif seniority > 5:
                cat = "L3"
            elif seniority > 2:
                cat = "L2"
            else:
                cat = "L1"
            
            # Polyvalence score (skill coverage) 0-100%
            polyvalence = np.clip(random.normalvariate(50 + (seniority * 1.5), 15), 20, 100)
            
            # Absenteeism (days per year)
            absenteeism = round(np.clip(random.normalvariate(5, 3), 0, 20))
            
            employee = {
                "ID": f"EMP-{i:03d}",
                "Sector": sector,
                "Role": role,
                "Category": cat,
                "Seniority_Years": seniority,
                "Polyvalence_Score": round(polyvalence, 1),
                "Absenteeism_Days": absenteeism,
                "Training_Hours": random.randint(5, 80),
                "Shift": random.choice(["Morning", "Afternoon", "Night"]),
                "Education": random.choice(["High School", "Technical Degree", "Associate", "Bachelor"])
            }
            data.append(employee)
            
        return pd.DataFrame(data)

    def generate_operational_data(self, months=6):
        """Generates operational KPIs per sector over time"""
        today = datetime.now()
        data = []
        
        for i in range(months * 30):
            date = today - timedelta(days=i)
            day_type = "Weekday" if date.weekday() < 5 else "Weekend"
            
            if day_type == "Weekday":
                for sector in self.sectors:
                    # Simulation Logic
                    volume = random.randint(100, 500)
                    defects = round(volume * random.uniform(0.005, 0.05)) # 0.5% to 5% defect rate
                    rework = round(defects * 0.8) # 80% of defects are reworkable
                    scrap = defects - rework
                    
                    std_time = 120 # seconds
                    actual_time_avg = std_time * random.uniform(0.95, 1.15)
                    efficiency = (std_time / actual_time_avg) * 100
                    
                    record = {
                        "Date": date.strftime("%Y-%m-%d"),
                        "Sector": sector,
                        "Production_Volume": volume,
                        "Defects": defects,
                        "Rework_Count": rework,
                        "Scrap_Count": scrap,
                        "Efficiency_Pct": round(efficiency, 1),
                        "Incidents": 1 if random.random() > 0.95 else 0 # 5% chance of incident
                    }
                    data.append(record)
                    
        return pd.DataFrame(data)

    def generate_initial_kanban(self):
        """Generates dummy tasks for the Kanban board"""
        tasks = [
            {"ID": "ACT-001", "Desc": "Standardize formatting in Line A", "Owner": "EMP-012", "Status": "Done", "Area": "Assembly A", "Type": "Lean"},
            {"ID": "ACT-002", "Desc": "Safety guard repair", "Owner": "EMP-045", "Status": "In Progress", "Area": "Machining", "Type": "Safety"},
            {"ID": "ACT-003", "Desc": "Cross-train Operator B on QC", "Owner": "Supervisor", "Status": "To Do", "Area": "Quality Control", "Type": "Training"},
            {"ID": "ACT-004", "Desc": "5S Audit - Tool Shadow Boards", "Owner": "EMP-003", "Status": "In Progress", "Area": "Logistics", "Type": "5S"},
            {"ID": "ACT-005", "Desc": "Reduce changeover time (SMED)", "Owner": "Eng. Team", "Status": "To Do", "Area": "Assembly B", "Type": "Kaizen"},
        ]
        return pd.DataFrame(tasks)
