import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class RadarChartEngine:
    def __init__(self, db_path="database/nifty100.db", output_dir="reports/radar_charts/"):
        self.db_path = db_path
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        
        # Explicit 8 axes matched precisely with portal constraints
        self.metrics = ['roe', 'roce', 'npm', 'de', 'fcf_score', 'pat_cagr_5yr', 'revenue_cagr_5yr', 'composite_score']
        self.labels = ['ROE', 'ROCE', 'NPM', 'D/E', 'FCF Score', 'PAT CAGR 5Y', 'Rev CAGR 5Y', 'Composite Score']

    def load_analytical_data(self):
        # Gather day 18 calculated profiles
        df_ranks = pd.read_sql("SELECT * FROM peer_percentiles", self.conn)
        
        # Gather original financial matrix universe
        df_ratios = pd.read_sql("SELECT * FROM financial_ratios", self.conn)
        df_ratios.columns = [col.lower().strip() for col in df_ratios.columns]
        
        # Extract operational composite scores mapping framework
        try:
            df_comp = pd.read_sql("SELECT company_id, composite_quality_score FROM composite_scores", self.conn)
            df_comp.columns = ['company_id', 'composite_score']
        except:
            if 'composite_quality_score' in df_ratios.columns:
                df_comp = df_ratios[['company_id', 'composite_quality_score']].copy()
                df_comp.columns = ['company_id', 'composite_score']
            else:
                df_comp = pd.DataFrame({'company_id': df_ratios['company_id'].unique(), 'composite_score': 75.0})
                
        return df_ranks, df_comp, df_ratios

    def generate_all_charts(self):
        df_ranks, df_comp, df_ratios = self.load_analytical_data()
        
        if df_ranks.empty:
            print("❌ Failure Context: Run Day 18 module to construct base percentiles.")
            return

        # Map 'fcf' key names explicitly to 'fcf_score' target parameters
        df_ranks['metric'] = df_ranks['metric'].replace({'fcf': 'fcf_score'})

        # Flatten rows into a clean multi-metric wide matrix array
        pivot_ranks = df_ranks.pivot_table(
            index='company_id', 
            columns='metric', 
            values='percentile_rank', 
            aggfunc='last'
        ).reset_index()
        
        # Merge calculated system scores
        pivot_ranks = pd.merge(pivot_ranks, df_comp.drop_duplicates(subset=['company_id']), on='company_id', how='left').fillna(50.0)
        
        # Assign corporate tracking identifiers
        latest_ranks = df_ranks.drop_duplicates(subset=['company_id'], keep='last')
        peer_map = dict(zip(latest_ranks['company_id'], latest_ranks['peer_group_name']))
        
        group_averages = pivot_ranks.copy()
        group_averages['peer_group_name'] = group_averages['company_id'].map(peer_map)
        
        # Establish structural benchmark matrices
        nifty_100_avg = group_averages[self.metrics].mean().to_dict()
        
        peer_group_avgs = {}
        for grp, grp_df in group_averages.dropna(subset=['peer_group_name']).groupby('peer_group_name'):
            peer_group_avgs[grp] = grp_df[self.metrics].mean().to_dict()

        unique_companies = df_ratios['company_id'].unique()
        num_m_axes = len(self.metrics)
        
        # Build radial circular plots distribution coordinates
        angles = np.linspace(0, 2 * np.pi, num_m_axes, endpoint=False).tolist()
        angles += angles[:1] 

        print(f"🎨 Generating Verified Radar Visualization Vector Layers for {len(unique_companies)} entities...")

        for comp in unique_companies:
            comp_data = pivot_ranks[pivot_ranks['company_id'] == comp]
            
            if comp_data.empty:
                comp_values = [50.0] * num_m_axes
            else:
                comp_values = [float(comp_data.iloc[0].get(m, 50.0)) for m in self.metrics]
            comp_values += comp_values[:1]

            p_group = peer_map.get(comp, None)
            
            # Explicit structural validation for overlay markers
            if p_group and p_group in peer_group_avgs:
                overlay_label = f"{p_group} Average"
                overlay_data = [peer_group_avgs[p_group][m] for m in self.metrics]
            else:
                overlay_label = "Nifty 100 Average"
                overlay_data = [nifty_100_avg[m] for m in self.metrics]
                print(f"ℹ️ Notice: Unmapped structure detected for '{comp}' — mapping safely to global Nifty 100 benchmark.")
                
            overlay_data += overlay_data[:1]

            # --- Visual Execution Block ---
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            
            # Render Core Target Company Polygon Solid Fills
            ax.plot(angles, comp_values, color='#1f77b4', linewidth=2, label=f"{comp} Percentile Performance")
            ax.fill(angles, comp_values, color='#1f77b4', alpha=0.25)
            
            # Render Baseline Dashed Peer Overlays
            ax.plot(angles, overlay_data, color='#ff7f0e', linewidth=1.5, linestyle='--', label=overlay_label)
            
            ax.set_theta_offset(np.pi / 2)
            ax.set_theta_direction(-1)
            
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(self.labels, fontsize=9, fontweight='semibold')
            ax.set_rlabel_position(30)
            plt.yticks([25, 50, 75, 100], ["25", "50", "75", "100"], color="grey", size=8)
            plt.ylim(0, 110)
            
            plt.title(f"Performance Architecture: {comp}", size=11, fontweight='bold', y=1.1)
            plt.legend(loc='upper right', bbox_to_anchor=(1.4, 1.1), fontsize=8)
            
            plt.tight_layout()
            file_name = f"{comp}_radar.png"
            full_path = os.path.join(self.output_dir, file_name)
            plt.savefig(full_path, dpi=120, bbox_inches='tight')
            plt.close()

        print(f"📊 Visualization Pipelines Complete: Output profiles built in '{self.output_dir}'.")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    engine = RadarChartEngine()
    engine.generate_all_charts()
    engine.close()