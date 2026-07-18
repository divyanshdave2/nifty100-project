Nifty100 Financial Intelligence Platform
Sprint 1 - Day 1
Completed:

Project structure setup
Database initialization
Raw data organization
Environment setup
GitHub repository setup


Sprint 1 - Day 2
Completed:

Excel loader implementation
Loading all 12 datasets from data/raw
normalize_year() function created
normalize_ticker() function created
Loader testing completed
Normalization testing completed


Sprint 1 - Day 3
Completed:

Data validation module created
Null value detection implemented
Duplicate row detection implemented
Validation testing completed
Dataset quality assessment performed


Sprint 1 - Day 4
Completed:

- Created SQLite database
- Implemented database loader
- Loaded all 12 datasets into SQLite
- Verified table creation
- Validated successful data ingestion


Sprint 1 - Day 5
Completed:

- Performed data quality audit
- Checked row counts across all tables
- Identified null values
- Checked duplicate records
- Generated load_audit.csv report


Sprint 1 - Day 6
Completed:

- Performed manual data quality review
- Reviewed 5 random companies
- Verified row counts across tables
- Checked database consistency
- Identified and documented header loading issue
- Generated DQ review notes

Sprint 1 - Day 7
Completed:

- Created exploratory SQL queries
- Reviewed database contents
- Summarized unit test results
- Completed sprint review documentation
- Prepared project for Sprint 2


Sprint 2 - Day 8
Completed:

Implemented Net Profit Margin (NPM) calculation
Implemented Operating Profit Margin (OPM) calculation
Added OPM cross-check validation against existing values
Implemented Return on Equity (ROE) calculation
Implemented Return on Capital Employed (ROCE) calculation
Implemented Return on Assets (ROA) calculation
Added Financial sector-specific ROCE evaluation logic
Added anomaly logging for OPM mismatches
Implemented edge-case handling for zero and invalid denominators
Created comprehensive unit tests (tests/test_ratios.py)
Successfully passed all 8/8 unit tests


Sprint 2 - Day 9
Completed:

* Implemented Debt-to-Equity (D/E) Ratio
* Implemented Interest Coverage Ratio (ICR)
* Implemented Net Debt calculation
* Implemented Asset Turnover Ratio
* Added edge-case handling for invalid denominators
* Added debt-free company handling
* Created comprehensive unit tests
* Successfully passed all 18 unit tests


Sprint 2 - Day 10
Completed:

* Developed a reusable CAGR (Compound Annual Growth Rate) engine in Python.
* Implemented Revenue CAGR, PAT CAGR, and EPS CAGR calculations for 3-year, 5-year, and 10-year periods.
* Added robust edge-case handling for zero base values, turnaround scenarios, decline-to-loss cases, negative values, and insufficient historical data.
* Created comprehensive unit tests covering normal calculations and all edge cases.
* Successfully passed all CAGR unit tests.


Sprint 2 - Day 11
Completed:

* Implemented Free Cash Flow (FCF) calculation.
* Developed FCF Quality classification based on multi-year cash flow trends.
* Built CFO/PAT Ratio for earnings quality analysis.
* Implemented CAPEX Intensity Ratio to measure asset intensity.
* Added Capital Allocation Pattern classification (Growth, Mature, Distressed, Unclassified).
* Created comprehensive unit tests covering all cash flow analytics and edge cases.
* Successfully passed all 19 unit tests.

Sprint 2 - Day 12
Completed:

* Developed the core financial ratio consolidation pipeline (`src/analytics/financial_ratios.py`).
* Consolidated over 14+ required financial KPIs spanning margins, returns, leverage, efficiency, and cash flows.
* Implemented True 5-Year CAGR calculation engines for Revenue, PAT, and EPS utilizing shift-based historical offsets.
* Engineered a 5-point Composite Quality Scoring ruleset evaluating fundamentals across efficiency, leverage, cash flow quality, coverage, and profitability.
* Built the Free Cash Flow (FCF) Conversion Rate metric with built-in zero-denominator exception handling.
* Designed an 8-Pattern Capital Allocation Matrix Classifier using CFO, CFI, and CFF sign permutations.
* Resolved database indexing issues by implementing standardized text cleaning (`strip()`) and LEFT join strategies.
* Successfully generated the required downstream analytical asset `output/capital_allocation.csv`.
* Replaced and updated the centralized SQLite `financial_ratios` table, securing a full target footprint of 1,276 rows.

## 📅 Sprint 2 - Day 13: Bank ROCE Carve-Out & Edge-Case Logging

### ✅ Completed Tasks:
* **Sector-Specific Warnings:** Implemented custom logic to suppress Debt-to-Equity (D/E) warning flags for the Financial sector (Banks, NBFCs, Insurance) where high leverage is structural.
* **ROCE Cross-Verification:** Developed an automated engine to validate calculated ROCE metrics against `roce_percentage` from `companies.xlsx`.
* **ROE Validation Loop:** Built a secondary audit loop comparing calculated ROE values directly against `roe_percentage` from the reference source.
* **Automated Anomaly Detection:** Programmed variance tracking that captures and logs any metric discrepancies exceeding the absolute 5% threshold boundary.
* **Smart Categorization:** Implemented dynamic classification to bucket anomalies into distinct error types (`Formula Difference`, `Source Data Difference`, `Version Difference`).
* **UTF-8 Log File Generation:** Configured a clean text streaming layer to output fully structured discrepancy reports inside `output/ratio_edge_cases.log`.
* **Live Terminal Reporting:** Successfully tested and verified the execution engine with real-time console streams tracking 531 total logged anomalies.

Sprint 2 - Day 14: Tests & Sprint Review
Completed Tasks:

* 20 KPI Unit Tests: Successfully executed and passed the entire structural unit test suite with absolute zero failures.
* Audit Trail Check: Reviewed `ratio_edge_cases.log` to ensure all 531 detected metric anomalies are cleanly tracked with precise classifications.
* Screener Engine Validation: Ran a performance filter ($ROE > 15\%$ and $D/E < 1$) which safely isolated 60 unique target companies across 414 historical rows.
* Demo Ready Status: Configured a dataset preview script displaying 14+ calculated financial indicators for sample companies to facilitate the final team lead review.
* Sprint 2 Retrospective: Finalized code adjustments and documented business rule decisions for the repository knowledge base.


Sprint 3 - Day 15: Streamlit Dashboard Mockup & Core Layout Design
Completed Tasks:

* UI Architecture Initialization: Configured a dedicated Streamlit application footprint (`src/app.py`) for frontend layer mapping.
* Multi-Page Routing Framework: Programmed a clean sidebar navigation system supporting three integrated interface layers:
  * `Home / Overview`: Core market dynamic summary cards.
  * `Company Deep-Dive`: Granular organizational breakdown sheets.
  * `Screener Engine`: Dynamic metric constraint parameters.
* Airtight Session Caching: Integrated `@st.cache_resource` and `@st.cache_data` directives to optimize database connection handling and ensure zero-lag template state re-runs.
* Repository Deployment: Successfully localized, clean-tested, and synchronized the initial running frontend code tree to the GitHub main branch.


Sprint 3 - Day 16: Preset Screeners Execution & Bounds Verification
Completed Tasks:
* Preset Algorithmic Filter Chains: Programmed 6 customized corporate selection screeners inside `src/screener/engine.py` processing dynamic boolean metrics matrix matching.
* Robust Normalization Pipeline: Implemented text formatting and naming casing normalization hooks to seamlessly bridge structural columns under multiple fallback aliases (e.g., `pe_ratio`, `return_on_equity_pct`).
* Boundary Evaluation: Validated code logic via core command-line unit executions (`python -m src.screener.engine`).
* Successful Execution Outputs: Verified distribution metrics on the latest dynamic year blocks across the universe:
  * Quality Compounder: 20 companies matched.
  * Growth Accelerator: 9 companies matched.
  * Turnaround Watch: 42 companies matched.
* Version Control Sync: Pushed error-free, normalized, and benchmarked compilation files directly onto the GitHub main branch ecosystem.

Sprint 3 - Day 17: Composite Quality Score & P10/P90 Winsorization
Completed Tasks:

* Winsorization Pipeline Implementation: Developed an advanced statistical `_winsorize_and_scale` method using Numpy to cap extreme outliers at the 10th (P10) and 90th (P90) percentiles.
* Multi-Dimensional Weighting Matrix: Engineered the composite score structure matching strict corporate distribution metrics:
  * 35% Profitability Framework (ROE, ROCE, NPM)
  * 30% Cash Quality Architecture (PAT/FCF conversion and positive cash tracking flags)
  * 20% Structural Growth Engine (CAGR parameters)
  * 15% Capital Leverage Allocation (D/E and ICR inverse metrics)
* Sector-Relative Normalization: Linked the scoring matrices with `groupby` mechanics on the `broad_sector` identifier, preventing cross-industry metric skewing.
* Output Sorting Logic: Updated internal engines to enforce descending sorts on calculated composite quality scores across all presets and custom screeners.
* Automated Excel Compilation: Generated the multi-preset `output/screener_output.xlsx` containing custom soft-palette cell coloring injection for threshold rules.


Sprint 3 - Day 18: Peer Percentile Rankings Engine
* Peer Group Analysis Engine: Developed a calculation pipeline within `src/analytics/peer.py` mapping structural percentiles across 10 target KPIs within 11 distinct peer blocks.
* Inverse Metric Framework: Programmed custom directional adjustments for leverage calculations, enforcing an inverse rank formula ($1 - \text{PERCENT\_RANK}$) for Debt-to-Equity ($D/E$) ratios.
* Unmapped Entities Graceful Bypass: Integrated fallback handling to identify companies without a peer group mapping, logging an analytical message without raising fatal program exceptions.
* Persistent DB Layer Migration: Integrated dynamic truncation routines to refresh structural content inside SQLite's `peer_percentiles` datatable automatically.


Sprint 3 - Day 19: Multi-Axis Radar Visualization Engine
* 8-Axis Geometry Core: Programmed structural data parsing pipelines inside `src/visualization/radar.py` to plot multi-dimensional performance layers across exactly 8 distinct financial parameters (`ROE`, `ROCE`, `NPM`, `D/E`, `FCF Score`, `PAT CAGR 5Y`, `Rev CAGR 5Y`, and `Composite Score`).
* Double-Layered Data Mapping: Configured a dual-vector matplotlib interface plotting individual corporate data points as a shaded solid polygon alongside a clear dashed outline overlay mapping the respective peer group averages.
* Graceful Benchmark Fallback: Deployed logical left-join parameters ensuring unmapped market companies (e.g., `VBL`) dynamically map against global Nifty 100 statistical benchmarks without throwing operational runtime exceptions.
* Automated Output Pipeline: Standardized localized PNG generation outputting files safely under the strict `{company_id}_radar.png` naming framework inside the target `reports/radar_charts/` directory structure.


Sprint 3 - Day 20: Peer Comparison Excel Report

* Multi-Sheet Architecture: Developed an automated compiler engine inside `src/analytics/report.py` that segregates corporate analysis into exactly 11 distinct peer group sheets within a single workbook.
* Expanded Metrics Grid: Populated each individual sheet layout with comprehensive corporate metadata (Company ID and Company Name) alongside 20+ core financial metrics and their corresponding calculated peer percentile ranks.
* Tri-Tier Color-Coding Fills: Injected automated cell-level formatting using strict threshold conditions ($\ge$ 75th percentile maps to soft green, 25th to 75th percentile to soft yellow, and $\le$ 25th percentile to soft red).
* Benchmark & Summary Row Injection: Engineered custom rendering layers to highlight the primary benchmark company row using a gold/amber background fill, while embedding a rolling geometric `GROUP MEDIAN` summary calculation row across all metric parameters at the base of each workbook sheet.


Sprint 3 - Day 21: Tests & Sprint Review

* Zero-Failure Test Execution: Triggered the complete regression suite validating all 14 programmatic Data Quality (DQ) constraints across data loaders, ensuring comprehensive engine test coverage with 0 test suite failures.
* Quality Compounder Validation: Audited the `Quality Compounder` spreadsheet engine outputs to mathematically verify that the filtered layout properly extracts companies meeting the baseline threshold of ROE > 15% and D/E < 1.
* Percentile Scale Audit: Verified statistical correctness inside the `IT Services` peer domain to guarantee that individual ranking scores map monotonically against raw asset ratios, positioning top ROE values at the apex rank.
* Handoff & Sprint Review: Consolidated the core repository assets (`screener_output.xlsx` across 6 preset sheets and `peer_comparison.xlsx` with 11 structural sheets) for final deployment sign-off and retrospective documentation.

Sprint 4 - Day 22: Streamlit App Scaffold & Core Utilities
* Multi-Page App Scaffolding: Created the central entry point src/dashboard/app.py utilizing Streamlit's native multi-page configuration with wide-screen page settings and default expanded sidebar layout.
* Directory Structural Mappings: Organized the codebase architecture by provisioning the pages/ directory with 8 core frontend screen files (01_home.py through 08_reports.py) to prevent navigation breaks.
* Shared Data Loader Integration: Implemented the central utility script src/dashboard/utils/db.py to handle heavy database-like lookups, applying the @st.cache_data(ttl=600) decorator to achieve a 10-minute caching threshold.
* Functional API Declarations: Programmed core data retrieval functions inside the cached module (get_companies(), get_ratios(), get_pl(), get_bs(), get_cf(), get_sectors(), get_peers(), and get_valuation()) to unify application logic.

Sprint 4 - Day 23: Home & Company Profile Screens Implementation
* Macro Aggregates Visualization: Programmed the Home Overview screen (pages/01_home.py) featuring 6 high-level summary KPI tiles for key financial ratios linked dynamically to a 6-year sidebar calendar selection menu.
* Sectoral & Quality Sorting: Integrated a Plotly sector distribution donut chart spanning 11 broad sectors on the Home screen alongside a quality tabular directory indexing the top-5 companies filtered by composite quality rankings.
* Autocomplete Lookup Architecture: Designed the Company Profile screen (pages/02_profile.py) with a flexible autocomplete selection input widget mapping explicit company name and NSE ticker strings.
* Dual-Axis & Cross-Filtering Trajectory: Built high-fidelity financial charts including a 10-year grouping bar chart for Revenue/Net Profit and a dual-axis Plotly trendline for ROE/ROCE, complete with graceful fallback error trapping (Ticker not found – please try another).

Sprint 4 - Day 24: Advanced Screener & Peer Comparison Screens
* Multi-Metric Filtering Presets: Developed the Metric Screener layout (pages/03_screener.py) containing 10 interactive sidebar threshold sliders wired to 6 macro filter preset shortcut buttons that automatically adjust operational bounds.
* Dynamic Table Exporter: Programmed live result row counters combined with a robust tabular dataset rendering pipeline, embedding a physical CSV data exporter utility mapping matching row conditions.
* Cross-Sectional Polar Charting: Built the Peer Comparison layer (pages/04_peers.py) using an interactive 11-sector dropdown configuration paired with a multi-variable Plotly radar chart (Scatterpolar) comparing focus targets against industry averages.
* Cross-Sectional Benchmark Grid: Standardized the peer data grid visualization layout, applying row accent formatting to distinctly isolate the benchmark company profile row from adjacent sectoral line items.

Sprint 4 - Day 25: Trend, Sector, Capital Allocation & Compliance Hubs
* Historical Overlay Modeling: Engineered the Trend Analysis workspace (pages/05_trends.py) allowing simultaneous overlay tracking of up to 3 specific financial metrics across a 10-year line graph annotated with YoY percentage changes.
* Four-Dimensional Sector Space: Scripted the Sector Dynamics application screen (pages/06_sectors.py) utilizing an interactive 4D Plotly bubble chart mapping X=Revenue, Y=ROE, Size = Market Cap, and Color = Sub-sector, with secondary sector median baseline plots below.
* Hierarchical Tree Structuring: Coded the Capital Allocation tool (pages/07_capital.py) featuring a Plotly treemap organizing 92 companies into 8 allocation buckets, with an auxiliary data table reacting dynamically to clicked blocks.
* Compliance PDF Repository: Formed the Annual Reports document hub (pages/08_reports.py) syncing profile selections with official external BSE corporate file attachments while mapping an custom red alert status badge (Report unavailable) for missing paths.

Sprint 4 - Day 26: Algorithmic Valuation Module Development
* Valuation Script Architecture: Developed the core analysis file src/analytics/valuation.py to handle out-of-core data extraction pipelines linked with regional market capitalization Excel workbook matrices.
* FCF Yield Computations: Coded internal calculation arrays to evaluate standard Free Cash Flow (FCF) Yield metrics for the entire index universe using the explicit evaluation equation:
* FCF/market_cap_crore×100
Sectoral Multiple Benchmarking: Formed localized grouping functions to compute true trailing sector median price-to-earnings (P/E) multiples across every broad industry quadrant.
* Overvaluation Flags Exporter: Implemented automated analytical threshold logic to classify structural exceptions into explicit output datasets (valuation_summary.xlsx and valuation_flags.csv), flagging records as Caution, Discount, or Fair based on sector medians.

Sprint 4 - Day 27: Integration QA & Stress-Testing Operations
* Cross-Sector Rigorous Testing: Executed multi-point regression verification loops utilizing 10 distinctive company tickers across 5 key economic sectors to confirm application stability.
* Data Scarcity Resiliency: Implemented partial history fallback workflows to gracefully process newly listed asset classes under 10 years without causing script disruptions or application fatal errors.
* Boundary & Crash Verifications: Stress-tested the interactive screener engines using extreme slider data constraints (absolute minimums and maximums) to verify structural boundary safety.
* Null Value Sanitization: Added strict sanitization rules that trap raw null values (None / NaN), translating them into uniform "N/A" layout strings to ensure front-end rendering stability.
* Latency Benchmarking Run: Conducted performance timing audits across multiple active modules, validating that profile screen loading procedures stay within the strict 3-second target threshold.

Sprint 4 - Day 28: Retrospective, Documentation & Final Sign-Off
* Repository Documentation Overhaul: Rewrote the global documentation guide (README.md) to integrate clear runtime initialization guidelines (streamlit run src/dashboard/app.py) along with comprehensive descriptions for all 8 frontend analytical screens.
* UX Retrospective Archival: Drafted the formal Sprint 4 Retrospective report documenting core UX design choices, newly discovered missing data patterns, and caching speed optimizations.
* Task Board Finalization: Audited and cleared the open development pipeline, marking all Sprint 4 epics and auxiliary engineering check items as Complete across tracking project boards.
* Technical Sign-Off Demonstration: Conducted a comprehensive live platform walkthrough displaying data accuracy across all 8 screens, successfully securing the formal project sign-off and review confirmation.

# 📊 Bluestock Fintech MJ28 - Capstone Project I

Nifty 100 universe ke analytics, quality metrics aur valuation tracking ke liye ek advanced internal multi-page Streamlit dashboard.

---

## 🚀 Application Run Instructions

Dashboard ko local development machine par run karne ke liye terminal me ye command execute karein:
```bash
streamlit run src/dashboard/app.py


Screen Descriptions (All 8 Screens Detailed Catalog)
Screen 1: Home Overview (01_home.py)
Layout Structure: Top par 6 horizontal cards (KPI Summary Tiles) hain jo Average ROE, Median P/E, Median D/E, Total Companies, Median Revenue CAGR 5yr, aur Debt-Free Companies ka count dikhate hain.
Controls: Sidebar mein ek dynamic Year Selector dropdown hai (2019 se 2024 tak) jisse poore page ka data ek baar mein filter ho jata hai.
Visual Components: Left side mein Plotly ka use karke bana hua ek interactive Sector Breakdown Donut Chart hai jo 11 sectors ki distribution dikhata hai. Right side mein top 5 companies ki data table hai jo Composite Quality Score ke mutabik sorted hai.

Screen 2: Company Profile (02_profile.py)
Layout Structure: Sabse upar ek Autocomplete Search Input box hai jahan company ka naam ya ticker symbol type karke search kar sakte hain.
Components: Filter karne par ek detailed Company Profile Card open hota hai jismein Sector, Sub-Sector, NSE Ticker, aur Company Description likha hota hai. Iske theek neehe 6 metric summary tiles hain (ROE, ROCE, NPM, D/E, 5Yr CAGR, FCF).
Charts & Analysis: Neehe do bade charts hain—pehla 10-Year Bar Chart jo Revenue aur Net Profit ka compression dikhata hai, aur doosra dual-axis Line Chart jo ROE vs ROCE ke trends dikhata hai. Sabse neehe green checkmarks ke saath Pros aur red cross ke saath Cons points display hote hain.
Error Handling: Agar koi galat ticker daalta hai, toh frontend par alert aata hai: Ticker not found – please try another.

Screen 3: Advanced Metric Screener (03_screener.py)
Layout Structure: Sidebar panel mein 10 financial metrics ke alag-alag range adjustment sliders diye gaye hain. Main screen par upar 6 clickable Preset Buttons hain (Quality, Value, Growth, Dividend, Debt-Free, Turnaround) jinpar click karte hi saare sliders automatically preset values par set ho jaate hain.
Live Feed Table: Sliders ko move karte hi neehe ki data table live update hoti hai. Table ke upar ek dynamic counter label hai jo dikhata hai ki kitne companies filter match kar rahe hain (e.g., 23 companies match your filters).
Data Exporter: Table ke theek upar ek permanent Download Results CSV button hai jispar click karte hi filtered list pure column headers ke saath excel/csv format mein download ho jaati hai.

Screen 4: Peer Comparison (04_peers.py)
Layout Structure: Isme sabse upar ek Dropdown menu hai jahan se 11 unique sector groups mein se kisi ek ko select kiya jata hai. Uske neehe ek doosra selector hai jisse us sector ki kisi ek benchmark company ko focus row banaya jata hai.
Radar Matrix Chart: Ek custom Plotly Radar Chart (Scatterpolar) display hota hai jo selected company ke 8 alag-alag metrics ko pure sector ke average (mean) score se visually overlay karke compare karta hai.
Side-by-Side Matrix Table: Neehe ek comprehensive data table hai jismein sector ke saare peers side-by-side dikhte hain aur selected benchmark company ki puri row background color highlight ke saath alag chamakti hai.

Screen 5: Trend Analysis Tool (05_trends.py)
Layout Structure: Isme ek search box hai company select karne ke liye aur ek Multi-metric Selector dropdown hai, jahan se user ek saath maximum 3 metrics ko select karke aapas mein compare kar sakta hai.
Line Chart & Annotations: Yeh ek 10-year historical trend line chart generate karta hai. Iski sabs badi khasiyat yeh hai ki chart ke har ek data point ke upar automatic calculation hoke YoY (Year-on-Year) percentage change ka text annotation dikhta hai (e.g., +12.4% green mein ya -5.2% red mein).

Screen 6: Sector Analysis Workspace (06_sectors.py)
Layout Structure: Target sector dropdown select karne par ek advanced 4D Plotly Scatter Bubble Chart load hota hai.
Bubble Configurations: Is chart mein X-axis par Revenue, Y-axis par ROE, bubbles ka size unki Market Cap ke mutabik, aur bubble ka color unke Sub-sector ke hisab se dynamically render hota hai. Is bubble plot ke theek neehe pure sector ka median benchmark bar chart display hota hai.

Screen 7: Capital Allocation Map (07_capital.py)
Layout Structure: Pura page ek bade Plotly Treemap chart se cover hota hai jo index ki saari 92 companies ko unki capital deployment habits ke hisab se 8 distinct allocation patterns (e.g., Aggressive CapEx, High Dividend Payout) mein group karta hai.
Click Drill-down: Kisi bhi pattern block par click karte hi screen ke neehe ek standalone nested data directory khul jaati hai jo sirf us specific pattern se match hone waali companies ki sorted list unke market cap ke saath table mein dikhati hai.

Screen 8: Annual Reports Vault (08_reports.py)
Layout Structure: Ek dynamic company document directory sheet jahan user corporate profile search karta hai. Search karte hi pichle saalon ke reports ki ek clean row-wise index list khul jaati hai.
Compliance Links & Fallback Badges: Sahi files ke aage clickable hyperlinks hote hain jo seedhe official BSE Annual Report PDF par redirect karte hain. Agar koi link broken hai ya server se 404 response aata hai, toh wahan link ki jagah ek custom red badge render hota hai jispar likha hota hai: Report unavailable.