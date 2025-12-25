import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Brenda's Reconciliation Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# ENHANCED CUSTOM CSS FOR STUNNING UI
# =============================================================================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Animated Gradient Header */
    .hero-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.3rem;
        animation: gradientShift 3s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    /* Section Headers */
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #667eea, #764ba2) 1;
    }
    
    /* Beautiful Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1.5rem;
    }
    
    .welcome-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.8);
    }
    
    .welcome-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .welcome-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .welcome-text {
        color: #64748b;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    /* Step Cards */
    .step-container {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .step-card {
        flex: 1;
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #e2e8f0;
    }
    
    .step-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .step-number {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }
    
    .step-title {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.3rem;
    }
    
    .step-desc {
        font-size: 0.85rem;
        color: #64748b;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card.total {
        border-top: 4px solid #3b82f6;
    }
    
    .metric-card.matched {
        border-top: 4px solid #10b981;
    }
    
    .metric-card.unmatched {
        border-top: 4px solid #f59e0b;
    }
    
    .metric-card.pairs {
        border-top: 4px solid #8b5cf6;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    .sidebar-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .sidebar-step {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #667eea;
    }
    
    .sidebar-step-title {
        font-weight: 600;
        color: #1e293b;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    .stButton > button[kind="secondary"] {
        background: #f1f5f9;
        color: #475569;
    }
    
    /* Download Button Styling */
    .download-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .download-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .download-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .download-title {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.3rem;
    }
    
    .download-desc {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 1rem;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #f1f5f9;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* DataFrame Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 12px;
        font-weight: 500;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Info/Success/Warning Boxes */
    .stAlert {
        border-radius: 12px;
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    /* File Uploader Styling */
    .stFileUploader > div {
        border-radius: 12px;
    }
    
    /* Tooltip Styling */
    .stTooltipIcon {
        color: #667eea;
    }
    
    /* Footer */
    .app-footer {
        text-align: center;
        padding: 2rem 0;
        color: #94a3b8;
        font-size: 0.85rem;
    }
    
    .app-footer a {
        color: #667eea;
        text-decoration: none;
    }
    
    /* Animation for elements */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.5s ease forwards;
    }
    
    /* Success Animation */
    @keyframes successPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .success-animation {
        animation: successPulse 0.5s ease;
    }
    
    /* Loading Shimmer */
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .loading-shimmer {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        'process_log': [],
        'df_original': None,
        'df_matched': None,
        'df_unmatched': None,
        'processed': False,
        'file_uploaded': False,
        'available_sheets': [],
        'total_matches': 0,
        'match_details': []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def add_log(message: str, level: str = "INFO"):
    """Add timestamped log entry."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    icons = {
        "INFO": "ℹ️",
        "SUCCESS": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌",
        "PROCESS": "⚙️",
        "MATCH": "🔗"
    }
    icon = icons.get(level, "📝")
    entry = f"[{timestamp}] {icon} {message}"
    st.session_state.process_log.append(entry)


def clear_log():
    """Clear all log entries."""
    st.session_state.process_log = []


# =============================================================================
# FILE HANDLING FUNCTIONS
# =============================================================================
def get_excel_sheets(uploaded_file) -> list:
    """Get all sheet names from uploaded Excel file."""
    try:
        uploaded_file.seek(0)
        excel_file = pd.ExcelFile(uploaded_file, engine='openpyxl')
        return excel_file.sheet_names
    except Exception as e:
        add_log(f"Error reading sheets: {str(e)}", "ERROR")
        return []


def load_excel_data(uploaded_file, sheet_name: str):
    """Load data from specified sheet."""
    try:
        uploaded_file.seek(0)
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name, engine='openpyxl')
        add_log(f"Successfully loaded sheet: '{sheet_name}'", "SUCCESS")
        add_log(f"Found {df.shape[0]:,} rows and {df.shape[1]} columns", "INFO")
        return df, None
    except ValueError:
        return None, f"Sheet '{sheet_name}' not found in the file."
    except Exception as e:
        return None, f"Error loading file: {str(e)}"


# =============================================================================
# CORE RECONCILIATION FUNCTION
# =============================================================================
def perform_reconciliation(df: pd.DataFrame, move_col: str, entry_label_col: str):
    """
    Perform reconciliation matching Move text within Entry Label.
    Your exact notebook logic preserved!
    """
    add_log("🚀 Starting reconciliation process...", "PROCESS")
    add_log(f"Looking for '{move_col}' values inside '{entry_label_col}'", "INFO")
    
    # Create clean copy
    df_clean = df.copy()
    
    # Clean the text columns
    add_log("Cleaning and preparing data...", "PROCESS")
    df_clean[move_col] = df_clean[move_col].astype(str).str.strip()
    df_clean[entry_label_col] = df_clean[entry_label_col].astype(str).str.strip()
    add_log("Data cleaned successfully!", "SUCCESS")
    
    # Add tracking columns
    df_clean['Is_Matched'] = False
    df_clean['Match_Partner'] = -1
    add_log("Tracking columns initialized", "SUCCESS")
    
    # Matching process
    used_indices = set()
    matches_found = 0
    match_details = []
    
    add_log("🔍 Scanning for matches...", "PROCESS")
    
    # Progress tracking
    total_rows = len(df_clean)
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, (i, row) in enumerate(df_clean.iterrows()):
        # Update progress
        progress = (idx + 1) / total_rows
        progress_bar.progress(progress)
        status_text.text(f"🔍 Analyzing record {idx + 1:,} of {total_rows:,}...")
        
        move_text = row[move_col]
        
        # Skip if already matched or empty
        if i in used_indices or not move_text or move_text == 'nan' or move_text == '':
            continue
        
        # Find matches
        matches = df_clean[
            (~df_clean.index.isin(used_indices)) &
            (df_clean[entry_label_col].str.contains(move_text, case=False, na=False, regex=False)) &
            (df_clean.index != i)
        ]
        
        if not matches.empty:
            match_idx = matches.index[0]
            
            # Mark both rows as matched
            df_clean.loc[i, 'Is_Matched'] = True
            df_clean.loc[match_idx, 'Is_Matched'] = True
            df_clean.loc[i, 'Match_Partner'] = match_idx
            df_clean.loc[match_idx, 'Match_Partner'] = i
            
            used_indices.update([i, match_idx])
            matches_found += 1
            
            # Store match details
            match_details.append({
                'Pair #': matches_found,
                'Record A': i,
                'Move Value': move_text[:40] + '...' if len(str(move_text)) > 40 else move_text,
                'Record B': match_idx,
                'Found In': str(df_clean.loc[match_idx, entry_label_col])[:40] + '...'
            })
            
            add_log(f"✨ Match #{matches_found}: Record {i} ↔ Record {match_idx}", "MATCH")
    
    # Clear progress
    progress_bar.empty()
    status_text.empty()
    
    add_log(f"🎉 Matching complete! Found {matches_found} matching pairs", "SUCCESS")
    
    # Separate results
    df_matched = df_clean[df_clean['Is_Matched'] == True].copy()
    df_unmatched = df_clean[df_clean['Is_Matched'] == False].copy()
    
    add_log(f"📊 Results: {len(df_matched):,} matched, {len(df_unmatched):,} unmatched", "INFO")
    
    return df_clean, df_matched, df_unmatched, match_details, matches_found


# =============================================================================
# EXPORT FUNCTIONS
# =============================================================================
def create_excel_export(df_matched: pd.DataFrame, df_unmatched: pd.DataFrame) -> bytes:
    """Create Excel file with Matched and Unmatched sheets."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_matched.to_excel(writer, sheet_name='Matched', index=False)
        df_unmatched.to_excel(writer, sheet_name='Unmatched', index=False)
    buffer.seek(0)
    return buffer.getvalue()


def create_csv_export(df: pd.DataFrame) -> bytes:
    """Create CSV file in memory."""
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, encoding='utf-8')
    buffer.seek(0)
    return buffer.getvalue()


# =============================================================================
# BEAUTIFUL UI COMPONENTS
# =============================================================================
def render_hero():
    """Render the hero/header section."""
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <span class="hero-badge">✨ Automation demo</span>
            <h1 class="hero-header">Brenda's Reconciliation Assistant</h1>
            <p class="hero-subtitle">
                Effortlessly match and reconcile your outstanding receipts with precision
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_welcome():
    """Render the welcome screen."""
    st.markdown("""
        <div class="welcome-card">
            <div class="welcome-icon">🏦</div>
            <div class="welcome-title">Welcome!</div>
            <p class="welcome-text">
                Ready to reconcile your outstanding receipts? Upload your Excel file 
                in the sidebar to get started. This tool will automatically match 
                Move references with Entry Labels, so that you save your time.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Step cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="step-card">
                <div class="step-number">1</div>
                <div class="step-title">Upload</div>
                <div class="step-desc">Select your Excel file</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="step-card">
                <div class="step-number">2</div>
                <div class="step-title">Configure</div>
                <div class="step-desc">Choose sheet & columns</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="step-card">
                <div class="step-number">3</div>
                <div class="step-title">Process</div>
                <div class="step-desc">Run reconciliation</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="step-card">
                <div class="step-number">4</div>
                <div class="step-title">Download</div>
                <div class="step-desc">Export your results</div>
            </div>
        """, unsafe_allow_html=True)


def render_metrics(total: int, matched: int, unmatched: int, pairs: int):
    """Render beautiful metric cards."""
    col1, col2, col3, col4 = st.columns(4)
    
    match_pct = (matched / total * 100) if total > 0 else 0
    unmatch_pct = (unmatched / total * 100) if total > 0 else 0
    
    with col1:
        st.markdown(f"""
            <div class="metric-card total">
                <div style="font-size: 2.2rem; font-weight: 700; color: #3b82f6;">{total:,}</div>
                <div style="color: #64748b; font-weight: 500;">Total Records</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card matched">
                <div style="font-size: 2.2rem; font-weight: 700; color: #10b981;">{matched:,}</div>
                <div style="color: #64748b; font-weight: 500;">Matched ({match_pct:.1f}%)</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card unmatched">
                <div style="font-size: 2.2rem; font-weight: 700; color: #f59e0b;">{unmatched:,}</div>
                <div style="color: #64748b; font-weight: 500;">Unmatched ({unmatch_pct:.1f}%)</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card pairs">
                <div style="font-size: 2.2rem; font-weight: 700; color: #8b5cf6;">{pairs:,}</div>
                <div style="color: #64748b; font-weight: 500;">Match Pairs Found</div>
            </div>
        """, unsafe_allow_html=True)


def render_download_section(df_matched, df_unmatched):
    """Render the download section with beautiful cards."""
    st.markdown('<p class="section-title">💾 Download Your Results</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="download-card">
                <div class="download-icon">📊</div>
                <div class="download-title">Complete Report</div>
                <div class="download-desc">Excel file with both sheets</div>
            </div>
        """, unsafe_allow_html=True)
        excel_data = create_excel_export(df_matched, df_unmatched)
        st.download_button(
            label="⬇️ Download Excel",
            data=excel_data,
            file_name=f"Reconciliation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        st.markdown(f"""
            <div class="download-card">
                <div class="download-icon">✅</div>
                <div class="download-title">Matched Only</div>
                <div class="download-desc">{len(df_matched):,} records as CSV</div>
            </div>
        """, unsafe_allow_html=True)
        csv_matched = create_csv_export(df_matched)
        st.download_button(
            label="⬇️ Download Matched",
            data=csv_matched,
            file_name=f"Matched_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        st.markdown(f"""
            <div class="download-card">
                <div class="download-icon">⚠️</div>
                <div class="download-title">Unmatched Only</div>
                <div class="download-desc">{len(df_unmatched):,} records as CSV</div>
            </div>
        """, unsafe_allow_html=True)
        csv_unmatched = create_csv_export(df_unmatched)
        st.download_button(
            label="⬇️ Download Unmatched",
            data=csv_unmatched,
            file_name=f"Unmatched_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )


def display_log():
    """Display the processing log."""
    if st.session_state.process_log:
        log_text = "\n".join(st.session_state.process_log)
        st.code(log_text, language="bash")


# =============================================================================
# MAIN APPLICATION
# =============================================================================
def main():
    """Main application entry point."""
    
    # Initialize session state
    init_session_state()
    
    # Render hero header
    render_hero()
    
    # =========================================================================
    # SIDEBAR
    # =========================================================================
    with st.sidebar:
        st.markdown('<p class="sidebar-header">⚙️ Configuration Panel</p>', unsafe_allow_html=True)
        
        # Step 1: File Upload
        st.markdown("""
            <div class="sidebar-step">
                <div class="sidebar-step-title">📁 Step 1: Upload Your File</div>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose Excel file",
            type=['xlsx', 'xls'],
            help="Upload your Outstanding Receipts Excel file",
            label_visibility="collapsed"
        )
        
        sheet_name = None
        move_column = None
        entry_label_column = None
        
        if uploaded_file:
            st.success(f"✅ Loaded: {uploaded_file.name}")
            
            sheets = get_excel_sheets(uploaded_file)
            st.session_state.available_sheets = sheets
            
            if sheets:
                # Step 2: Sheet Selection
                st.markdown("""
                    <div class="sidebar-step">
                        <div class="sidebar-step-title">📑 Step 2: Select Sheet</div>
                    </div>
                """, unsafe_allow_html=True)
                
                sheet_name = st.selectbox(
                    "Choose sheet",
                    options=sheets,
                    help="Select the sheet containing your data",
                    label_visibility="collapsed"
                )
                
                if sheet_name:
                    uploaded_file.seek(0)
                    temp_df, error = load_excel_data(uploaded_file, sheet_name)
                    
                    if temp_df is not None:
                        st.session_state.df_original = temp_df
                        columns = temp_df.columns.tolist()
                        
                        # Step 3: Column Selection
                        st.markdown("""
                            <div class="sidebar-step">
                                <div class="sidebar-step-title">🔧 Step 3: Configure Columns</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Smart defaults
                        default_move = columns.index('Move') if 'Move' in columns else 0
                        default_entry = columns.index('Entry Label') if 'Entry Label' in columns else 0
                        
                        move_column = st.selectbox(
                            "🔍 Search FOR (Move column):",
                            options=columns,
                            index=default_move,
                            help="Values from this column will be searched for"
                        )
                        
                        entry_label_column = st.selectbox(
                            "📋 Search IN (Entry Label column):",
                            options=columns,
                            index=default_entry,
                            help="This column will be searched for matches"
                        )
                        
                        st.info(f"💡 Will find rows where **{move_column}** appears inside **{entry_label_column}**")
                    else:
                        st.error(error)
        
        st.markdown("---")
        
        # Action Buttons
        col1, col2 = st.columns(2)
        
        with col1:
            process_btn = st.button(
                "🚀 Process",
                type="primary",
                use_container_width=True,
                disabled=(uploaded_file is None or sheet_name is None)
            )
        
        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                clear_log()
                for key in ['df_matched', 'df_unmatched', 'processed', 'total_matches', 'match_details']:
                    if key == 'processed':
                        st.session_state[key] = False
                    elif key == 'total_matches':
                        st.session_state[key] = 0
                    elif key == 'match_details':
                        st.session_state[key] = []
                    else:
                        st.session_state[key] = None
                st.rerun()
        
        # Help Section
        st.markdown("---")
        with st.expander("ℹ️ How It Works"):
            st.markdown("""
            **Matching Logic:**
            
            This tool finds pairs of records where the text in the **Move** column 
            of one record appears somewhere inside the **Entry Label** column 
            of another record.
            
            **Example:**
            - Record A Move: `PAY-001`
            - Record B Entry Label: `Payment for PAY-001 received`
            - ✅ These would be matched!
            
            **Tips:**
            - Ensure your data is clean
            - Check column selection carefully
            - Review unmatched items manually
            """)
        
        # Footer
        st.markdown("---")
        st.markdown("""
            <div style="text-align: center; color: #94a3b8; font-size: 0.8rem;">
                Made with ❤️ for brie brie<br>
                <span style="font-size: 0.7rem;">v2.0 Enhanced Edition</span>
            </div>
        """, unsafe_allow_html=True)
    
    # =========================================================================
    # MAIN CONTENT
    # =========================================================================
    
    # No file uploaded - show welcome
    if uploaded_file is None:
        render_welcome()
        return
    
    # =========================================================================
    # DATA PREVIEW (Before Processing)
    # =========================================================================
    if st.session_state.df_original is not None and not st.session_state.processed:
        st.markdown('<p class="section-title">📊 Data Preview</p>', unsafe_allow_html=True)
        
        df = st.session_state.df_original
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Total Rows", f"{len(df):,}")
        with col2:
            st.metric("📊 Total Columns", f"{len(df.columns)}")
        with col3:
            st.metric("📑 Sheet", sheet_name)
        
        # Column info expander
        with st.expander("🔍 View Column Details", expanded=False):
            col_info = pd.DataFrame({
                'Column Name': df.columns,
                'Data Type': df.dtypes.astype(str).values,
                'Non-Null Count': df.count().values,
                'Sample Value': [str(df[col].iloc[0])[:50] if len(df) > 0 else 'N/A' for col in df.columns]
            })
            st.dataframe(col_info, use_container_width=True, hide_index=True)
        
        # Data preview
        st.markdown("**📋 First 10 Records:**")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)
        
        # Numeric stats
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            with st.expander("📈 Numeric Column Statistics", expanded=False):
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)
    
    # =========================================================================
    # PROCESS RECONCILIATION
    # =========================================================================
    if process_btn and st.session_state.df_original is not None:
        clear_log()
        add_log(f"📂 File: {uploaded_file.name}", "INFO")
        add_log(f"📑 Sheet: {sheet_name}", "INFO")
        add_log(f"📊 Records to process: {len(st.session_state.df_original):,}", "INFO")
        
        st.markdown("---")
        st.markdown('<p class="section-title">⚙️ Processing Your Data...</p>', unsafe_allow_html=True)
        
        with st.spinner(""):
            df_clean, df_matched, df_unmatched, match_details, total_matches = perform_reconciliation(
                st.session_state.df_original,
                move_column,
                entry_label_column
            )
        
        # Store results
        st.session_state.df_matched = df_matched
        st.session_state.df_unmatched = df_unmatched
        st.session_state.total_matches = total_matches
        st.session_state.processed = True
        st.session_state.match_details = match_details
        
        st.success("🎉 Reconciliation complete!")
        st.balloons()
        st.rerun()
    
    # =========================================================================
    # DISPLAY RESULTS
    # =========================================================================
    if st.session_state.processed and st.session_state.df_matched is not None:
        df_matched = st.session_state.df_matched
        df_unmatched = st.session_state.df_unmatched
        total_records = len(df_matched) + len(df_unmatched)
        
        # Results Header
        st.markdown('<p class="section-title">📊 Reconciliation Results</p>', unsafe_allow_html=True)
        
        # Metrics
        render_metrics(
            total=total_records,
            matched=len(df_matched),
            unmatched=len(df_unmatched),
            pairs=st.session_state.total_matches
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Results Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "✅ Matched Records",
            "⚠️ Unmatched Records",
            "🔗 Match Pairs",
            "📋 Process Log"
        ])
        
        with tab1:
            if not df_matched.empty:
                st.markdown(f"### ✅ Matched Records ({len(df_matched):,})")
                
                # Column filter
                all_cols = df_matched.columns.tolist()
                default_cols = all_cols[:min(8, len(all_cols))]
                
                selected_cols = st.multiselect(
                    "Select columns to display:",
                    options=all_cols,
                    default=default_cols,
                    key="matched_display_cols"
                )
                
                if selected_cols:
                    st.dataframe(
                        df_matched[selected_cols],
                        use_container_width=True,
                        height=400,
                        hide_index=True
                    )
                
                with st.expander("📈 Statistics for Matched Records"):
                    num_cols = df_matched.select_dtypes(include=[np.number]).columns
                    if len(num_cols) > 0:
                        st.dataframe(df_matched[num_cols].describe(), use_container_width=True)
                    else:
                        st.info("No numeric columns available for statistics.")
            else:
                st.info("🔍 No matched records found.")
        
        with tab2:
            if not df_unmatched.empty:
                st.markdown(f"### ⚠️ Unmatched Records ({len(df_unmatched):,})")
                st.caption("These records need manual review")
                
                # Column filter
                all_cols = df_unmatched.columns.tolist()
                default_cols = all_cols[:min(8, len(all_cols))]
                
                selected_cols = st.multiselect(
                    "Select columns to display:",
                    options=all_cols,
                    default=default_cols,
                    key="unmatched_display_cols"
                )
                
                if selected_cols:
                    st.dataframe(
                        df_unmatched[selected_cols],
                        use_container_width=True,
                        height=400,
                        hide_index=True
                    )
                
                with st.expander("📈 Statistics for Unmatched Records"):
                    num_cols = df_unmatched.select_dtypes(include=[np.number]).columns
                    if len(num_cols) > 0:
                        st.dataframe(df_unmatched[num_cols].describe(), use_container_width=True)
                    else:
                        st.info("No numeric columns available for statistics.")
            else:
                st.success("🎉 Perfect! All records have been matched!")
        
        with tab3:
            st.markdown("### 🔗 Match Pair Details")
            st.caption("Shows which records matched with each other")
            
            if st.session_state.match_details:
                match_df = pd.DataFrame(st.session_state.match_details)
                st.dataframe(match_df, use_container_width=True, height=400, hide_index=True)
            else:
                st.info("No match details available.")
        
        with tab4:
            st.markdown("### 📋 Processing Log")
            st.caption("Step-by-step record of what happened")
            display_log()
        
        # Download Section
        st.markdown("---")
        render_download_section(df_matched, df_unmatched)
        
        # Custom download
        st.markdown("---")
        st.markdown("**🎯 Custom Export Options**")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            export_choice = st.selectbox(
                "Select dataset to export:",
                options=["Matched Records", "Unmatched Records", "All Records (Combined)"],
                key="custom_export"
            )
        
        with col2:
            if export_choice == "Matched Records":
                data = create_csv_export(df_matched)
                fname = "Matched_Records"
                count = len(df_matched)
            elif export_choice == "Unmatched Records":
                data = create_csv_export(df_unmatched)
                fname = "Unmatched_Records"
                count = len(df_unmatched)
            else:
                full_df = pd.concat([df_matched, df_unmatched], ignore_index=True)
                data = create_csv_export(full_df)
                fname = "All_Records"
                count = len(full_df)
            
            st.download_button(
                label=f"⬇️ Download {export_choice} ({count:,} records)",
                data=data,
                file_name=f"{fname}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div class="app-footer">
            <p>🏦 Brenda's Reconciliation Assistant </p>
        </div>
    """, unsafe_allow_html=True)


# =============================================================================
# RUN APPLICATION
# =============================================================================
if __name__ == "__main__":
    main()