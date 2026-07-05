import os
import sqlite3
import pandas as pd
import numpy as np

class NiftyScreenerEngine:
    def __init__(self, db_path="database/nifty100.db"):
        self.db_path = db_path
        self.df = self._load_data_layer()

    def _load_data_layer(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database not detected at: {self.db_path}")
        
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql("SELECT * FROM financial_ratios", conn)
        conn.close()
        
        df.columns = [col.lower().strip() for col in df.columns]
        
        if 'year' in df.columns:
            df['clean_year'] = df['year'].astype(str).str.extract(r'(\d{4})').astype(float)
        else:
            df['clean_year'] = 2024.0

        alias_dict = {
            'pe': ['pe_ratio', 'p_e', 'pe', 'p/e', 'price_to_earnings'],
            'pb': ['pb_ratio', 'p_b', 'pb', 'p/b', 'price_to_book'],
            'de': ['debt_to_equity', 'd_e', 'de', 'd/e', 'debt_equity_ratio'],
            'roe': ['return_on_equity_pct', 'roe', 'return_on_equity', 'roe_pct'],
            'fcf': ['free_cash_flow_cr', 'free_cash_flow', 'fcf', 'fcf_cr'],
            'rev_cagr': ['revenue_cagr_5yr', 'revenue_cagr', 'rev_cagr_5yr'],
            'pat_cagr': ['pat_cagr_5yr', 'pat_cagr', 'pat_cagr_5yr'],
            'div_yield': ['dividend_yield_pct', 'dividend_yield', 'div_yield']
        }
        
        for target, aliases in alias_dict.items():
            if target not in df.columns:
                for alias in aliases:
                    if alias in df.columns:
                        df[target] = df[alias]
                        break
                if target not in df.columns:
                    df[target] = 0.0

        numeric_targets = ['roe', 'de', 'fcf', 'rev_cagr', 'pat_cagr', 'pe', 'pb', 'div_yield']
        for col in numeric_targets:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

        if 'interest_coverage_ratio' in df.columns:
            df['interest_coverage_ratio'] = pd.to_numeric(df['interest_coverage_ratio'], errors='coerce').fillna(float('inf'))
            df.loc[df['de'] == 0, 'interest_coverage_ratio'] = float('inf')
            
        return df

    def _get_sector_column(self, df):
        possible_names = ['broad_sector', 'sector', 'industry', 'sector_name']
        for name in possible_names:
            if name in df.columns:
                return name
        return None

    def filter_by_custom_bounds(self, filter_params: dict):
        if self.df.empty:
            return pd.DataFrame()

        latest_year = self.df['clean_year'].max()
        df_latest = self.df[self.df['clean_year'] == latest_year].copy()
        sector_col = self._get_sector_column(df_latest)

        for metric, threshold in filter_params.items():
            key = metric
            if 'roe' in metric: key = 'roe'
            elif 'debt' in metric or 'de' in metric: key = 'de'
            
            if key in df_latest.columns:
                if key == 'de':
                    if sector_col:
                        is_financial = df_latest[sector_col].str.lower().str.contains('financial', na=False)
                        df_latest = df_latest[(df_latest[key] <= threshold) | is_financial]
                    else:
                        df_latest = df_latest[df_latest[key] <= threshold]
                else:
                    df_latest = df_latest[df_latest[key] >= threshold]

        return df_latest

    def run_preset_screener_day16(self, preset_name: str):
        latest_year = self.df['clean_year'].max()
        df_latest = self.df[self.df['clean_year'] == latest_year].copy()
        
        sector_col = self._get_sector_column(df_latest)
        is_financial = df_latest[sector_col].str.lower().str.contains('financial', na=False) if sector_col else pd.Series(False, index=df_latest.index)

        if preset_name == "Quality Compounder":
            cond = (df_latest['roe'] > 15.0) & ((df_latest['de'] < 1.0) | is_financial) & (df_latest['fcf'] > 0) & (df_latest['rev_cagr'] > 10.0)
            return df_latest[cond]

        elif preset_name == "Value Pick":
            cond = (df_latest['pe'] > 0) & (df_latest['pe'] < 30.0) & (df_latest['pb'] < 4.0)
            return df_latest[cond]

        elif preset_name == "Growth Accelerator":
            cond = (df_latest['pat_cagr'] > 20.0) & (df_latest['rev_cagr'] > 15.0) & ((df_latest['de'] < 2.0) | is_financial)
            return df_latest[cond]

        elif preset_name == "Dividend Champion":
            cond = (df_latest['div_yield'] > 1.5) & (df_latest['fcf'] > 0)
            return df_latest[cond]

        elif preset_name == "Debt-Free Blue Chip":
            cond = (df_latest['de'] == 0) & (df_latest['roe'] > 12.0)
            return df_latest[cond]

        elif preset_name == "Turnaround Watch":
            cond = (df_latest['rev_cagr'] > 10.0) & (df_latest['fcf'] > 0)
            return df_latest[cond]
        
        return pd.DataFrame()

if __name__ == "__main__":
    engine = NiftyScreenerEngine()
    
    print("\n" + "="*50)
    print(" 🚀 EXECUTION VERIFICATION: DAY 15 & DAY 16 ENGINES ")
    print("="*50)
    
    sample_criteria = {'roe': 15.0}
    custom_res = engine.filter_by_custom_bounds(sample_criteria)
    print(f"📊 Day 15 Core: Found {len(custom_res)} companies matching sample criteria.")
    
    presets = ["Quality Compounder", "Value Pick", "Growth Accelerator", "Dividend Champion", "Debt-Free Blue Chip", "Turnaround Watch"]
    for p in presets:
        preset_res = engine.run_preset_screener_day16(p)
        count = len(preset_res)
        print(f"🔹 Day 16 Preset '{p}': Matches {count} corporate rows.")