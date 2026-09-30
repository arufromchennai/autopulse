import streamlit as st
import snowflake.snowpark.context as context
import pandas as pd
import datetime
import random
import io

# -----------------------------------------------------------------------------
# 1. APPLICATION SETUP & TESLA LIGHT / STUDIO CERAMIC DESIGN SYSTEM
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AutoPulse OS | Connected Telematics & Diagnostics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    session = context.get_active_session()
except Exception:
    session = None

st.markdown("""
<style>
    @import url('[https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap](https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap)');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F8F9FA !important;
        color: #0F172A !important;
    }
    
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        z-index: 1 !important;
    }

    .main .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 98% !important;
    }

    .tesla-dock {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 16px 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04), 0 1px 3px rgba(0, 0, 0, 0.02);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .tesla-logo-group {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .tesla-wordmark {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #0F172A;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .tesla-pill {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 3px 8px;
        border-radius: 4px;
        background-color: #E82127;
        color: #FFFFFF;
    }

    .telemetry-status {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.76rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        color: #64748B;
    }

    .status-bulb {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
        animation: pulse-glow 2.5s infinite;
    }

    @keyframes pulse-glow {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.9); }
    }

    .hud-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        transition: all 0.2s ease-in-out;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }

    .hud-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
        transform: translateY(-2px);
    }

    .hud-label {
        font-size: 0.70rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.10em;
        color: #64748B;
        margin-bottom: 6px;
    }

    .hud-value {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #0F172A;
        line-height: 1.1;
    }

    .hud-meta {
        font-size: 0.78rem;
        font-weight: 500;
        color: #64748B;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .hud-danger { border-top: 4px solid #E82127; }
    .hud-warning { border-top: 4px solid #F59E0B; }
    .hud-success { border-top: 4px solid #10B981; }
    .hud-info { border-top: 4px solid #0284C7; }

    .live-stream-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: #065F46;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .copilot-role-badge {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #E82127;
        background: #FEE2E2;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 12px;
        border: 1px solid #FECACA;
    }

    .copilot-bubble {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #E82127;
        border-radius: 8px;
        padding: 14px 18px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #0F172A;
        line-height: 1.6;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }

    .notification-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    .notif-crit { border-left-color: #E82127; }
    .notif-warn { border-left-color: #F59E0B; }
    .notif-info { border-left-color: #10B981; }

    .user-profile-header {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }

    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. TRIAL-PROOF CORTEX COPILOT & DETERMINISTIC FALLBACK
# -------------------------------------------------------------
def generate_deterministic_briefing(prompt_text: str, user_role: str) -> str:
    p_lower = prompt_text.lower()
    
    if "consumer" in user_role.lower() or "owner" in user_role.lower() or "driver" in user_role.lower():
        if any(k in p_lower for k in ["brake", "caliper", "pad", "rotor"]):
            return (
                "**[AUTOPULSE OWNER ASSISTANT]**\n\n"
                "• **System Status**: Front brake assembly thermal profile is running higher than expected.\n"
                "• **What It Means**: Minor pad friction wear detected under repeated deceleration cycles.\n"
                "• **Recommended Action**: A replacement pad kit is reserved at `DLR-WEST-01`. You can schedule a zero-cost warranty check in the app."
            )
        elif any(k in p_lower for k in ["battery", "voltage", "charge", "range", "inverter"]):
            return (
                "**[AUTOPULSE OWNER ASSISTANT]**\n\n"
                "• **System Status**: Powertrain battery pack and auxiliary 12V cells are healthy.\n"
                "• **What It Means**: Routine voltage drop occurred during parked accessory usage; cell balancing is verified nominal.\n"
                "• **Recommended Action**: Maintain charging target at 80% for daily use. No workshop service needed."
            )
        else:
            return (
                "**[AUTOPULSE OWNER ASSISTANT]**\n\n"
                "• **Vehicle Health**: Core vehicle systems are operating within certified factory parameters.\n"
                "• **Driving Score**: Your 30-day driver score is 94/100, qualifying your account for safe-driver subscription credits.\n"
                "• **Contract Status**: 36-Month Lease active with comprehensive warranty and roadside protection."
            )

    if any(k in p_lower for k in ["brake", "caliper", "pad", "rotor"]):
        return (
            f"**[AUTOPULSE COPILOT EVALUATION — {user_role.upper()}]**\n\n"
            "• **Telemetry Physics Analysis**: CAN registers indicate persistent high-temperature thermal cycling (>380°C) with asymmetric front-axle heat dissipation.\n"
            "• **ISO 26262 ASIL-D Hazard**: Hydraulic fluid boiling and rotor glazing detected. Stopping distance margin degraded.\n"
            "• **Workshop Protocol**: Depressurize electro-hydraulic circuit; install replacement OEM caliper carrier assembly (torque to 115 Nm).\n"
            "• **Sign-off Test**: Pressure-bleed with DOT 4 Low-Viscosity fluid; complete deceleration burnish run."
        )
    elif any(k in p_lower for k in ["battery", "voltage", "alternator", "electrical", "inverter"]):
        return (
            f"**[AUTOPULSE COPILOT EVALUATION — {user_role.upper()}]**\n\n"
            "• **Telemetry Physics Analysis**: Voltage dips (<11.2V) recorded under idle accessory loads. Harmonic ripple indicates power stage diode degradation.\n"
            "• **ISO 26262 ASIL-D Hazard**: Bus brownouts trigger spurious CAN U0100 communication drops and ADAS failsafe disengagements.\n"
            "• **Workshop Protocol**: Isolate auxiliary ground; replace power inverter/converter unit with certified OEM part.\n"
            "• **Sign-off Test**: Reset Battery Monitoring Sensor (BMS) adaptives; verify regulated rail voltage between 14.1V and 14.5V."
        )
    elif any(k in p_lower for k in ["driver", "score", "lease", "behavior"]):
        return (
            f"**[AUTOPULSE COPILOT EVALUATION — {user_role.upper()}]**\n\n"
            "• **Driver Behavior Insights**: Telemetry indicates 94% highway speed compliance with infrequent harsh braking events (<0.2 per 100km).\n"
            "• **Lease Residual Value**: Wear index is within nominal bounds. Residual asset value projected at +4.2% above fleet average.\n"
            "• **Policy Recommendation**: Eligible for proactive subscription renewal discount or performance tier upgrade."
        )
    else:
        return (
            f"**[AUTOPULSE COPILOT EVALUATION — {user_role.upper()}]**\n\n"
            "• **Fleet State**: CAN-bus registers and feature streams are synchronized across active dealer zones.\n"
            "• **Operational Advisory**: Immediate service reservations recommended for units with RUL ≤ 7 days to maintain platform availability targets.\n"
            "• **Quality Notice**: Tracking early thermal wear batches to prevent multi-vehicle warranty liability exposure."
        )

def query_cortex_copilot(prompt_text: str, user_role: str, model: str = "mistral-large2") -> str:
    role_directives = {
        "🏢 OEM Corporate HQ": "You are AutoPulse Copilot advising OEM Executive Leadership on fleet availability and warranty risks.",
        "🔧 Dealership Service Hub": "You are AutoPulse Copilot advising Dealership Diagnostic Technicians on DTCs and part reservations.",
        "📈 Quality & Reliability Lab": "You are AutoPulse Copilot advising Reliability Engineers on sensor degradation physics.",
        "👤 Vehicle Owner / Driver": "You are AutoPulse Personal Companion explaining automotive telematics in simple, friendly, reassuring terms to the car owner."
    }

    directive = role_directives.get(user_role, "You are AutoPulse Copilot, an enterprise OEM automotive diagnostics AI.")
    full_prompt = f"[PERSONA DIRECTIVE]\n{directive}\n\n[USER QUERY & TELEMETRY]\n{prompt_text}"
    escaped_prompt = full_prompt.replace("'", "''")

    if session:
        cortex_sql = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', '{escaped_prompt}') AS RESPONSE;"
        try:
            res = session.sql(cortex_sql).collect()
            if res and res[0]["RESPONSE"]:
                return res[0]["RESPONSE"]
        except Exception:
            return generate_deterministic_briefing(prompt_text, user_role)
    
    return generate_deterministic_briefing(prompt_text, user_role)

# -------------------------------------------------------------
# 3. PURE-PYTHON 2-PAGE PDF GENERATOR (ZERO DEPENDENCIES)
# -------------------------------------------------------------
def generate_oem_pdf_report(vin: str, veh_meta: dict, briefing_text: str) -> bytes:
    clean_briefing = briefing_text.replace('\r', '').strip()
    raw_paragraphs = [p.strip() for p in clean_briefing.split('\n') if p.strip()]
    
    wrapped_lines = []
    for p in raw_paragraphs:
        words = p.split(' ')
        curr = []
        for w in words:
            curr.append(w)
            if len(' '.join(curr)) > 75:
                wrapped_lines.append(' '.join(curr))
                curr = []
        if curr:
            wrapped_lines.append(' '.join(curr))
        wrapped_lines.append("")

    p1_lines = wrapped_lines[:15]
    p2_lines = wrapped_lines if len(wrapped_lines) > 15 else [
        "ISO 26262 ASIL-D Directives validated by AutoPulse Telematics Core.",
        "Verify high-voltage cutoff interlocks prior to mechanical chassis access.",
        "Perform zero-point CAN calibration run before customer handoff."
    ]

    def build_page_stream(page_num: int, content_lines: list) -> bytes:
        if page_num == 1:
            stream = f"""BT
/F1 16 Tf
45 750 Td
(AUTOPULSE TELEMATICS & DIAGNOSTICS REPORT) Tj
/F2 9 Tf
0 -16 Td
(ISO 26262 ASIL-D OFFICIAL VEHICLE HEALTH ASSESSMENT & SERVICE DIRECTIVE) Tj
/F1 11 Tf
0 -26 Td
(1. IDENTIFICATION & TELEMETRY LEDGER) Tj
/F2 9 Tf
0 -15 Td
(Asset VIN: {vin}                        Platform: {veh_meta.get('MODEL_YEAR', '2025')} {veh_meta.get('MODEL', 'Pulse-EV')} {veh_meta.get('VARIANT', 'Performance')}) Tj
0 -13 Td
(Accumulated Odometer: {int(veh_meta.get('CURRENT_ODOMETER_KM', 42100)):,} km      Primary Hub: {veh_meta.get('PRIMARY_DEALER_ID', 'DLR-WEST-01')}) Tj
0 -13 Td
(Factory Warranty Status: {veh_meta.get('WARRANTY_STATUS', 'ACTIVE')}          Inspection Date: 2026-09-30) Tj
/F1 11 Tf
0 -24 Td
(2. PREDICTIVE HEALTH & FAILURE HAZARD CLASSIFICATION) Tj
/F2 9 Tf
0 -15 Td
(ASIL Hazard Severity: {veh_meta.get('HIGHEST_COMPONENT_RISK', 'CRITICAL')}            Forecast RUL: {int(veh_meta.get('MIN_PREDICTED_RUL_DAYS', 4))} Days) Tj
0 -13 Td
(Degraded Subsystem Target: {veh_meta.get('CRITICAL_COMPONENT_AT_RISK', 'Inverter Phase B')}) Tj
/F1 11 Tf
0 -24 Td
(3. REPAIR SPECIFICATIONS) Tj
/F2 9 Tf
0 -15 Td
(Authorized Service Code: {veh_meta.get('RECOMMENDED_SERVICE_CODE', 'SRV-INV-99')}      OEM Part: {veh_meta.get('PART_NUMBER_REQUIRED', 'INV-8820-T')}) Tj
0 -13 Td
(Local Hub Stock: {veh_meta.get('DEALER_PARTS_ON_HAND', 4)} Units          Estimated Cost: ${float(veh_meta.get('ESTIMATED_REPAIR_COST', 1850.0)):,.2f}) Tj
/F1 11 Tf
0 -24 Td
(4. CORTEX COPILOT SYNTHESIS) Tj
/F2 8 Tf
"""
            for l in content_lines:
                safe_line = l.replace('(', '[').replace(')', ']').replace('\\', '/')
                stream += f"0 -12 Td\n({safe_line}) Tj\n"
            stream += f"""/F2 7 Tf
0 -25 Td
(PAGE 1 OF 2  |  CONFIDENTIAL AUTOPULSE VEHICLE SPECIFICATION) Tj
ET"""
        else:
            stream = f"""BT
/F1 14 Tf
45 750 Td
(AUTOPULSE TECHNICAL SERVICE BULLETIN: {vin}) Tj
/F2 9 Tf
0 -16 Td
(PAGE 2: EXTENDED WORKSHOP PROTOCOL) Tj
/F1 11 Tf
0 -26 Td
(5. EXTENDED WORKSHOP DIRECTIVES & REPAIR STEPS) Tj
/F2 8 Tf
"""
            for l in content_lines:
                safe_line = l.replace('(', '[').replace(')', ']').replace('\\', '/')
                stream += f"0 -12 Td\n({safe_line}) Tj\n"
            stream += f"""
/F1 11 Tf
0 -26 Td
(6. ISO 26262 POST-REPAIR QUALITY SIGN-OFF) Tj
/F2 8 Tf
0 -15 Td
([ ] Verified ground isolation & harness integrity.) Tj
0 -13 Td
([ ] Replacement part {veh_meta.get('PART_NUMBER_REQUIRED', 'PRT-OEM')} calibrated.) Tj
0 -25 Td
(Lead Technician Signature: _______________________    Date: 2026-09-30) Tj
ET"""
        return stream.encode('latin-1', 'replace')

    p1_bytes = build_page_stream(1, p1_lines)
    p2_bytes = build_page_stream(2, p2_lines)

    pdf_buffer = io.BytesIO()
    offsets = []

    def write_obj(content):
        offsets.append(pdf_buffer.tell())
        pdf_buffer.write(content)

    pdf_buffer.write(b"%PDF-1.4\n")
    write_obj(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    write_obj(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >>\nendobj\n")
    write_obj(b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> /Contents 7 0 R >>\nendobj\n")
    write_obj(b"4 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> /Contents 8 0 R >>\nendobj\n")
    write_obj(b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n")
    write_obj(b"6 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
    write_obj(f"7 0 obj\n<< /Length {len(p1_bytes)} >>\nstream\n".encode('latin-1') + p1_bytes + b"\nendstream\nendobj\n")
    write_obj(f"8 0 obj\n<< /Length {len(p2_bytes)} >>\nstream\n".encode('latin-1') + p2_bytes + b"\nendstream\nendobj\n")

    xref_offset = pdf_buffer.tell()
    pdf_buffer.write(b"xref\n0 9\n0000000000 65535 f \n")
    for off in offsets:
        pdf_buffer.write(f"{off:010d} 00000 n \n".encode('latin-1'))

    pdf_buffer.write(f"trailer\n<< /Size 9 /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF".encode('latin-1'))
    return pdf_buffer.getvalue()

# -------------------------------------------------------------
# 4. POPUP MODAL: COPILOT CALLOUT WITH RAG INJECTION (@st.dialog)
# -------------------------------------------------------------
@st.dialog("⚡ AutoPulse Copilot Assistant", width="large")
def render_copilot_callout(active_role: str):
    st.markdown(f"""
        <div class="copilot-role-badge">Active Viewpoint: {active_role}</div>
        <p style="color:#64748B; font-size:0.82rem; margin:0 0 14px 0;">
            Reasoning is calibrated to your profile directives, active CAN telemetry, and TSB repair repositories.
        </p>
    """, unsafe_allow_html=True)

    if "copilot_history" not in st.session_state:
        st.session_state.copilot_history = []

    chat_box = st.container(height=360)
    with chat_box:
        if not st.session_state.copilot_history:
            st.caption(f"Copilot ready for {active_role}. Ask questions regarding telemetry, parts, or vehicle health.")
        for msg in st.session_state.copilot_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if query_input := st.chat_input("Inquire with AutoPulse Copilot (e.g. 'Assess risk on CAR-18391')...", key="copilot_callout_input"):
        st.session_state.copilot_history.append({"role": "user", "content": query_input})
        
        injected_context = ""
        vins = [w for w in query_input.replace(",", " ").split() if w.startswith("CAR-")]
        if not vins and "Owner" in active_role:
            vins = ["CAR-18391"]

        if vins and session:
            t_vin = vins[0]
            try:
                c_df = session.sql(f"""
                    SELECT VIN, MODEL, HIGHEST_COMPONENT_RISK, CRITICAL_COMPONENT_AT_RISK, MIN_PREDICTED_RUL_DAYS, PRIMARY_DEALER_ID
                    FROM AUTOPULSE_DB.MART.DIM_VEHICLE_FLEET_HEALTH
                    WHERE VIN = '{t_vin}' LIMIT 1;
                """).to_pandas()
                if not c_df.empty:
                    injected_context += f"\n[Live Telemetry Record for {t_vin}]:\n" + str(c_df.iloc[0].to_dict()) + "\n"
            except Exception:
                pass

        if session:
            clean_search = query_input.lower().replace("'", "")
            try:
                tsb_match = session.sql(f"""
                    SELECT TSB_ID, COMPONENT_CATEGORY, REPAIR_INSTRUCTIONS, SAFETY_WARNINGS
                    FROM AUTOPULSE_DB.AGENT.OEM_TSB_MANUALS
                    WHERE '{clean_search}' LIKE '%' || LOWER(COMPONENT_CATEGORY) || '%'
                       OR '{clean_search}' LIKE '%' || LOWER(SYMPTOM_DESCRIPTION) || '%'
                    LIMIT 1;
                """).to_pandas()
                if not tsb_match.empty:
                    tsb = tsb_match.iloc[0]
                    injected_context += f"\n[Matched Service Bulletin {tsb['TSB_ID']} ({tsb['COMPONENT_CATEGORY']})]:\nInstructions: {tsb['REPAIR_INSTRUCTIONS']}\nSafety Warnings: {tsb['SAFETY_WARNINGS']}\n"
            except Exception:
                pass

        full_user_prompt = f"{query_input}\n{injected_context}"
        
        with chat_box:
            with st.spinner("Synthesizing telemetry through Cortex Copilot..."):
                answer = query_cortex_copilot(full_user_prompt, user_role=active_role)
                st.session_state.copilot_history.append({"role": "assistant", "content": answer})
        st.rerun()

# -------------------------------------------------------------
# 5. TESLA HEADER DOCK: BRANDING, USER ROLE SELECTOR & COPILOT TRIGGER
# -------------------------------------------------------------
dock_col1, dock_col2, dock_col3 = st.columns([4, 4, 2], vertical_alignment="center")

with dock_col1:
    st.markdown("""
    <div class="tesla-logo-group">
        <div class="tesla-wordmark">⚡ AUTOPULSE <span style="font-weight:300; color:#E82127;">OS</span></div>
        <div class="tesla-pill">ASIL-D</div>
        <div class="telemetry-status">
            <span class="status-bulb"></span>
            <span>TELEMETRY ONLINE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with dock_col2:
    active_profile = st.selectbox(
        "ACTIVE PERSONA",
        options=[
            "👤 Vehicle Owner / Driver",
            "🏢 OEM Corporate HQ",
            "🔧 Dealership Service Hub",
            "📈 Quality & Reliability Lab"
        ],
        index=0,
        label_visibility="collapsed"
    )

with dock_col3:
    if st.button("💬 Copilot Callout", use_container_width=True, type="primary"):
        render_copilot_callout(active_profile)

st.divider()

# -------------------------------------------------------------
# 6. SIDEBAR: NAVIGATION CONSOLE & FILTERS
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("<p class='hud-label'>OPERATIONAL CONTROL CONSOLE</p>", unsafe_allow_html=True)

    if active_profile == "👤 Vehicle Owner / Driver":
        nav_options = [
            "📱 My Connected Vehicle & Subscription Hub",
            "🔔 My Vehicle Health & Alert Feed"
        ]
    elif active_profile == "🏢 OEM Corporate HQ":
        nav_options = [
            "⚡ Auto-Driven KPI Mission Control",
            "📍 Subscription & Lease Vehicle Control Center",
            "🔔 Customer Experience (CX) Alert Center",
            "🏢 Fleet Overview & Management",
            "🚗 Vehicle 360 & ISO Dossier"
        ]
    elif active_profile == "🔧 Dealership Service Hub":
        nav_options = [
            "⚡ Auto-Driven KPI Mission Control",
            "🔧 Service Triage & Dispatch",
            "📦 Inventory & Parts Hub",
            "🔔 Customer Experience (CX) Alert Center",
            "🚗 Vehicle 360 & ISO Dossier"
        ]
    else:
        nav_options = [
            "⚡ Auto-Driven KPI Mission Control",
            "📈 Quality & Degradation Lab",
            "📍 Subscription & Lease Vehicle Control Center",
            "🔔 Customer Experience (CX) Alert Center",
            "🚗 Vehicle 360 & ISO Dossier"
        ]

    active_view = st.radio("CONSOLES", nav_options, label_visibility="collapsed")

    if active_profile != "👤 Vehicle Owner / Driver":
        st.markdown("<br><p class='hud-label'>GLOBAL TELEMETRY FILTERS</p>", unsafe_allow_html=True)
        f_risk = st.selectbox("Hazard Severity", ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"], index=0)
        f_model = st.multiselect("Platform Lines", ["Pulse-Sedan", "Pulse-SUV", "Pulse-GT", "Pulse-Truck", "Pulse-EV"])

    st.markdown("---")
    if st.button("🔄 Sync Telematics Bus", use_container_width=True):
        st.cache_data.clear()
        st.toast("Telematics registers synchronized.", icon="⚡")

# -------------------------------------------------------------
# 7. SCREEN: USER VIEW - MY CONNECTED VEHICLE & SUBSCRIPTION HUB
# -------------------------------------------------------------
if active_view == "📱 My Connected Vehicle & Subscription Hub":
    user_vin = "CAR-18391"
    
    st.markdown(f"""
    <div class="user-profile-header">
        <div>
            <div style="font-size:1.3rem; font-weight:800; color:#0F172A;">Welcome Back, Alexander</div>
            <div style="font-size:0.85rem; color:#64748B;">2025 Pulse-EV Performance Dual-Motor &nbsp;|&nbsp; Asset ID: <code>{user_vin}</code></div>
        </div>
        <div style="text-align:right;">
            <span class="live-stream-badge"><span class="status-bulb"></span> CONNECTED & PROTECTED</span>
            <div style="font-size:0.75rem; color:#64748B; margin-top:4px;">Subscription: All-Inclusive Premium Lease</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    u1, u2, u3, u4 = st.columns(4)
    with u1:
        st.markdown("""
        <div class="hud-card hud-success">
            <div class="hud-label">Driver Safety Score</div>
            <div class="hud-value" style="color:#10B981;">94 <span style="font-size:1.1rem; color:#64748B;">/100</span></div>
            <div class="hud-meta">⭐ Top 5% Fleet Tier (Discount Active)</div>
        </div>
        """, unsafe_allow_html=True)
    with u2:
        st.markdown("""
        <div class="hud-card hud-info">
            <div class="hud-label">Battery State of Charge</div>
            <div class="hud-value">78%</div>
            <div class="hud-meta">⚡ Est. Range: 382 km (398V Rail)</div>
        </div>
        """, unsafe_allow_html=True)
    with u3:
        st.markdown("""
        <div class="hud-card hud-warning">
            <div class="hud-label">Next Service Target</div>
            <div class="hud-value" style="color:#F59E0B;">3 Days</div>
            <div class="hud-meta">Front Brake Pad Wear Check Required</div>
        </div>
        """, unsafe_allow_html=True)
    with u4:
        st.markdown("""
        <div class="hud-card hud-info">
            <div class="hud-label">Monthly Lease Cost</div>
            <div class="hud-value">$890</div>
            <div class="hud-meta">Includes Tire, Brake & Battery Coverage</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    g_map, g_stats = st.columns([1, 1], gap="large")
    with g_map:
        st.markdown("#### **📍 Live Vehicle Location & Parked Anchor**")
        st.caption("Active GPS ping: Seattle Center, WA (Speed: 0 km/h, Parked & Locked)")
        user_coords = pd.DataFrame([{"LAT": 47.6062, "LON": -122.3321}])
        st.map(user_coords, zoom=12)

    with g_stats:
        st.markdown("#### **Driver Safety Performance (Past 7 Days)**")
        st.caption("Continuous analysis of braking smoothness, speed limits, and cornering stability.")
        user_score_trend = pd.DataFrame({
            "Smooth Braking": [96, 95, 93, 94, 91, 95, 97],
            "Speed Compliance": [92, 90, 94, 95, 93, 92, 95]
        }, index=["Thu", "Fri", "Sat", "Sun", "Mon", "Tue", "Today"])
        st.line_chart(user_score_trend)

    st.markdown("---")
    st.markdown("#### **Subscription Protection & One-Touch Service Scheduling**")
    
    col_sub_details, col_action = st.columns([2, 1], gap="large")
    with col_sub_details:
        st.write("**Subscription Term:** 36-Month All-Inclusive (Month 14 of 36)")
        st.progress(14 / 36, text="Lease Progress: 38% Completed")
        st.write("• **Authorized Dealership:** `DLR-WEST-01 (Seattle West Coast Hub)`")
        st.write("• **Warranty Protection:** Fully Covered (Zero Out-of-Pocket for Brake & Inverter Services)")
        st.write("• **Wear & Tear Policy:** Included within 25,000 km/year allowance")

    with col_action:
        st.markdown("##### **Proactive Maintenance Booking**")
        st.info("Your vehicle has signaled a brake pad thermal check. A replacement kit is allocated at your hub.")
        if st.button("📅 Confirm Service Bay Reservation (Zero Cost)", type="primary", use_container_width=True):
            st.success("Appointment reserved for Friday at 10:00 AM at DLR-WEST-01. Complimentary loaner vehicle assigned.")

# -------------------------------------------------------------
# 8. SCREEN: USER VIEW - MY VEHICLE HEALTH & ALERT FEED
# -------------------------------------------------------------
elif active_view == "🔔 My Vehicle Health & Alert Feed":
    st.markdown("### 🔔 **My Vehicle Health & Notification Stream**")
    st.caption("Direct telemetry notifications sent to your AutoPulse Mobile App and in-cabin dashboard.")

    user_notifs = [
        {
            "SEVERITY": "WARNING",
            "TITLE": "Front Caliper Thermal Dissipation Advisory",
            "BODY": "Our sensors noted higher-than-average thermal cycles on your front brakes during deceleration. A complimentary inspection slot has been reserved.",
            "TIME": "Today, 11:42 AM",
            "ACTION": "Reserved at DLR-WEST-01"
        },
        {
            "SEVERITY": "INFO",
            "TITLE": "Fast Charging Thermal Balance Complete",
            "BODY": "Battery pack reached 80% charge at 150 kW DC Fast Station. Cell temperatures stabilized to nominal 28°C.",
            "TIME": "Yesterday, 04:15 PM",
            "ACTION": "Logged"
        },
        {
            "SEVERITY": "SUCCESS",
            "TITLE": "Driver Safety Score Tier Bonus Applied",
            "BODY": "Congratulations! Your 94/100 score qualified your subscription for a $35 monthly safe-driver credit on your upcoming lease bill.",
            "TIME": "Sep 28, 2026",
            "ACTION": "Credit Applied"
        }
    ]

    for n in user_notifs:
        sev_border = "#F59E0B" if n["SEVERITY"] == "WARNING" else ("#10B981" if n["SEVERITY"] == "SUCCESS" else "#3B82F6")
        st.markdown(f"""
        <div class="notification-card" style="border-left-color: {sev_border};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <strong style="font-size:0.95rem; color:#0F172A;">{n['TITLE']}</strong>
                <span style="font-size:0.75rem; color:#64748B;">{n['TIME']}</span>
            </div>
            <p style="font-size:0.85rem; color:#334155; margin:8px 0;">{n['BODY']}</p>
            <div style="font-size:0.75rem; font-weight:700; color:{sev_border};">STATUS: {n['ACTION']}</div>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 9. SCREEN: ENTERPRISE VIEW - AUTO-DRIVEN KPI MISSION CONTROL (@st.fragment)
# -------------------------------------------------------------
elif active_view == "⚡ Auto-Driven KPI Mission Control":
    @st.fragment(run_every="3s")
    def render_auto_driven_kpi_dashboard():
        now_str = datetime.datetime.now().strftime("%H:%M:%S")

        if session:
            try:
                kpi_df = session.sql("""
                    SELECT 
                        COUNT(VIN) AS TOTAL_FLEET,
                        COUNT(CASE WHEN HIGHEST_COMPONENT_RISK = 'CRITICAL' THEN 1 END) AS CRITICAL_COUNT,
                        COUNT(CASE WHEN HIGHEST_COMPONENT_RISK = 'HIGH' THEN 1 END) AS HIGH_COUNT,
                        ROUND(AVG(CURRENT_ODOMETER_KM), 0) AS AVG_MILEAGE
                    FROM AUTOPULSE_DB.MART.DIM_VEHICLE_FLEET_HEALTH
                """).to_pandas().iloc[0]
                tot = int(kpi_df['TOTAL_FLEET'])
                crit = int(kpi_df['CRITICAL_COUNT'])
                high = int(kpi_df['HIGH_COUNT'])
                odo = int(kpi_df['AVG_MILEAGE'])
            except Exception:
                tot, crit, high, odo = 12480, 24, 118, 38400
        else:
            tick = random.choice([-1, 0, 1])
            tot = 12480 + (tick * 2)
            crit = max(18, 24 + tick)
            high = 118 - tick
            odo = 38420 + random.randint(1, 5)

        availability = ((tot - crit) / tot * 100) if tot > 0 else 100.0

        kpi_bar1, kpi_bar2 = st.columns([3, 1], vertical_alignment="center")
        with kpi_bar1:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px;">
                <h3 style="margin:0; font-weight:800; color:#0F172A;">⚡ Auto-Driven Fleet Telemetry Mission Control</h3>
                <span class="live-stream-badge">
                    <span class="status-bulb"></span> AUTO-REFRESHING (3s POLLING)
                </span>
            </div>
            """, unsafe_allow_html=True)
        with kpi_bar2:
            st.markdown(f"""
            <div style="text-align:right; font-family:'JetBrains Mono'; font-size:0.8rem; color:#64748B;">
                LAST PACKET: <strong style="color:#0F172A;">{now_str} UTC</strong>
            </div>
            """, unsafe_allow_html=True)

        st.caption("Zero-latency connected vehicle stream. Monitors ISO 26262 ASIL-D threshold breaches across deployed platforms.")
        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="hud-card hud-info"><div class="hud-label">Connected Assets (Active)</div><div class="hud-value">{tot:,}</div><div class="hud-meta">⚡ Ping: 12ms &nbsp;|&nbsp; Avg Odo: {odo:,} km</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="hud-card hud-danger"><div class="hud-label">ASIL-D Critical Units (RUL ≤ 7d)</div><div class="hud-value" style="color:#E82127;">{crit}</div><div class="hud-meta">⚠️ Immediate Dispatch Triggered</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="hud-card hud-warning"><div class="hud-label">Thermal & High-Wear Watchlist</div><div class="hud-value" style="color:#D97706;">{high}</div><div class="hud-meta">📉 Harmonic Drift Detected</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="hud-card hud-success"><div class="hud-label">Fleet Operational SLA</div><div class="hud-value" style="color:#059669;">{availability:.2f}%</div><div class="hud-meta">Target: >98.00% Platform Uptime</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        g1, g2 = st.columns([2, 1], gap="large")
        with g1:
            st.markdown("#### **Real-Time CAN Inverter Temperature & Battery Bus (Rolling Window)**")
            chart_len = 15
            temps = [round(68.0 + random.uniform(-1.5, 3.5), 1) for _ in range(chart_len)]
            volts = [round(398.0 + random.uniform(-2.0, 2.0), 1) for _ in range(chart_len)]
            timestamps = [f"T-{(chart_len - 1 - i)*3}s" for i in range(chart_len)]
            live_telemetry_df = pd.DataFrame({"Inverter Temp (°C)": temps, "Pack Voltage (V)": volts}, index=timestamps)
            st.line_chart(live_telemetry_df)

        with g2:
            st.markdown("#### **Live Risk Allocation by Platform**")
            mock_live_bar = pd.DataFrame({
                "CRITICAL": [crit // 2, crit // 4, crit // 5, 2],
                "HIGH": [high // 3, high // 4, high // 4, 15]
            }, index=["Pulse-EV", "Pulse-SUV", "Pulse-Sedan", "Pulse-GT"])
            st.bar_chart(mock_live_bar)

    render_auto_driven_kpi_dashboard()

# -------------------------------------------------------------
# 10. SCREEN: SUBSCRIPTION & LEASE VEHICLE CONTROL CENTER
# -------------------------------------------------------------
elif active_view == "📍 Subscription & Lease Vehicle Control Center":
    st.markdown("### 📍 **Subscription & Lease Vehicle Control Center**")
    st.caption("Live asset geolocation tracking, demographic segmentation, driver safety telemetry, and contract tenure status.")

    lk1, lk2, lk3, lk4 = st.columns(4)
    with lk1:
        st.markdown("""<div class="hud-card hud-info"><div class="hud-label">Subscribed Assets</div><div class="hud-value">3,842</div><div class="hud-meta">Active Subscriptions & Leases</div></div>""", unsafe_allow_html=True)
    with lk2:
        st.markdown("""<div class="hud-card hud-success"><div class="hud-label">Average Driver Score</div><div class="hud-value" style="color:#10B981;">88.4<span style="font-size:1.1rem; color:#64748B;"> /100</span></div><div class="hud-meta">Low Asset Wear Factor</div></div>""", unsafe_allow_html=True)
    with lk3:
        st.markdown("""<div class="hud-card hud-warning"><div class="hud-label">Aggressive Driving Alerts</div><div class="hud-value" style="color:#F59E0B;">47</div><div class="hud-meta">Harsh Accel / Cornering G > 0.4g</div></div>""", unsafe_allow_html=True)
    with lk4:
        st.markdown("""<div class="hud-card hud-danger"><div class="hud-label">Lease Renewal Horizon</div><div class="hud-value" style="color:#E82127;">184</div><div class="hud-meta">Contracts Expiring in ≤ 30 Days</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    lease_fleet_data = [
        {"VIN": "CAR-18391", "DRIVER_NAME": "Alexander Wright", "LOCATION_CITY": "Seattle, WA", "LAT": 47.6062, "LON": -122.3321, "DRIVER_SCORE": 94, "PLAN_TYPE": "All-Inclusive Subscription", "CONTRACT_STATUS": "ACTIVE", "MONTHLY_RATE": "$890", "HARSH_EVENTS": 1, "CURRENT_SPEED_KMH": 0},
        {"VIN": "CAR-20412", "DRIVER_NAME": "Sophia Chen", "LOCATION_CITY": "San Francisco, CA", "LAT": 37.7749, "LON": -122.4194, "DRIVER_SCORE": 91, "PLAN_TYPE": "36-Month Lease", "CONTRACT_STATUS": "ACTIVE", "MONTHLY_RATE": "$650", "HARSH_EVENTS": 2, "CURRENT_SPEED_KMH": 62},
        {"VIN": "CAR-99120", "DRIVER_NAME": "Marcus Vance", "LOCATION_CITY": "Austin, TX", "LAT": 30.2672, "LON": -97.7431, "DRIVER_SCORE": 89, "PLAN_TYPE": "Corporate Fleet", "CONTRACT_STATUS": "ACTIVE", "MONTHLY_RATE": "$1,120", "HARSH_EVENTS": 3, "CURRENT_SPEED_KMH": 88},
        {"VIN": "CAR-33104", "DRIVER_NAME": "Elena Rostova", "LOCATION_CITY": "Chicago, IL", "LAT": 41.8781, "LON": -87.6298, "DRIVER_SCORE": 68, "PLAN_TYPE": "24-Month Lease", "CONTRACT_STATUS": "EXPIRING_SOON", "MONTHLY_RATE": "$720", "HARSH_EVENTS": 9, "CURRENT_SPEED_KMH": 104}
    ]
    df_lease = pd.DataFrame(lease_fleet_data)

    map_col, chart_col = st.columns([2, 1], gap="large")
    with map_col:
        st.markdown("#### **Active Vehicle Geolocation Radar**")
        st.map(df_lease[["LAT", "LON"]], zoom=3)
    with chart_col:
        st.markdown("#### **Driver Safety Score Distribution**")
        st.bar_chart(df_lease.set_index("DRIVER_NAME")["DRIVER_SCORE"])

    st.markdown("---")
    st.dataframe(df_lease, use_container_width=True, hide_index=True)

# -------------------------------------------------------------
# 11. SCREEN: CUSTOMER EXPERIENCE (CX) ALERT CENTER
# -------------------------------------------------------------
elif active_view == "🔔 Customer Experience (CX) Alert Center":
    st.markdown("### 🔔 **Customer Experience (CX) Alert Center**")
    st.caption("Active monitoring of consumer-facing notifications, critical battery alarms, preventive health alerts, and service advisories.")

    notifications_data = [
        {"ALERT_ID": "ALR-88102", "VIN": "CAR-18391", "SEVERITY": "CRITICAL", "CATEGORY": "BATTERY_THERMAL", "TITLE": "High-Voltage Inverter Thermal Surge", "CUSTOMER_MESSAGE": "AutoPulse Alert: Critical thermal spike detected in Inverter. Nearest dealer reserved.", "CHANNEL": "Mobile App Push + SMS", "TIMESTAMP": "12:54:10 UTC", "STATUS": "SENT"},
        {"ALERT_ID": "ALR-88103", "VIN": "CAR-20412", "SEVERITY": "CRITICAL", "CATEGORY": "BRAKE_HYDRAULIC", "TITLE": "Brake Line Pressure Anomaly", "CUSTOMER_MESSAGE": "AutoPulse Alert: Irregular brake pressure curve detected. Stopping distance may be extended.", "CHANNEL": "Mobile App Push", "TIMESTAMP": "12:49:22 UTC", "STATUS": "READ"},
        {"ALERT_ID": "ALR-88104", "VIN": "CAR-99120", "SEVERITY": "HIGH", "CATEGORY": "BATTERY_CELL_VOLTAGE", "TITLE": "Auxiliary 12V Cell Voltage Sag", "CUSTOMER_MESSAGE": "Notice: 12V auxiliary battery voltage dropped to 10.8V during idle. Please schedule diagnostic check.", "CHANNEL": "In-Car Infotainment + App", "TIMESTAMP": "12:38:05 UTC", "STATUS": "SENT"}
    ]
    df_notifs = pd.DataFrame(notifications_data)

    for _, row in df_notifs.iterrows():
        sev_class = "notif-crit" if row["SEVERITY"] == "CRITICAL" else "notif-warn"
        st.markdown(f"""
        <div class="notification-card {sev_class}">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <strong style="color:#0F172A; font-size:0.95rem;">{row['TITLE']}</strong>
                <span style="font-size:0.75rem; font-weight:700; color:#64748B;">{row['TIMESTAMP']} | {row['CHANNEL']}</span>
            </div>
            <div style="font-size:0.85rem; color:#334155; margin-bottom:8px;">{row['CUSTOMER_MESSAGE']}</div>
            <div style="display:flex; gap:16px; font-size:0.75rem; color:#64748B; font-weight:600;">
                <span>ASSET: <code style="color:#E82127;">{row['VIN']}</code></span>
                <span>STATUS: <strong style="color:#0284C7;">{row['STATUS']}</strong></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 12. SCREEN: FLEET OVERVIEW & MANAGEMENT
# -------------------------------------------------------------
elif active_view == "🏢 Fleet Overview & Management":
    st.markdown("### 🏢 **Fleet Executive Command Console**")
    st.caption(f"Profile: {active_profile} | Real-time aggregate telemetry across active vehicle nodes.")

    if session:
        try:
            kpi_df = session.sql("""
                SELECT 
                    COUNT(VIN) AS TOTAL_FLEET,
                    COUNT(CASE WHEN HIGHEST_COMPONENT_RISK = 'CRITICAL' THEN 1 END) AS CRITICAL_COUNT,
                    COUNT(CASE WHEN HIGHEST_COMPONENT_RISK = 'HIGH' THEN 1 END) AS HIGH_COUNT,
                    ROUND(AVG(CURRENT_ODOMETER_KM), 0) AS AVG_MILEAGE
                FROM AUTOPULSE_DB.MART.DIM_VEHICLE_FLEET_HEALTH
            """).to_pandas().iloc[0]
            tot = int(kpi_df['TOTAL_FLEET'])
            crit = int(kpi_df['CRITICAL_COUNT'])
            high = int(kpi_df['HIGH_COUNT'])
            odo = int(kpi_df['AVG_MILEAGE'])
        except Exception:
            tot, crit, high, odo = 12480, 24, 118, 38400
    else:
        tot, crit, high, odo = 12480, 24, 118, 38400

    availability = ((tot - crit) / tot * 100) if tot > 0 else 100.0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="hud-card hud-info">
            <div class="hud-label">Connected Fleet Assets</div>
            <div class="hud-value">{tot:,}</div>
            <div class="hud-meta">Avg Odometer: {odo:,} km</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="hud-card hud-danger">
            <div class="hud-label">ASIL-D Critical (RUL ≤ 7d)</div>
            <div class="hud-value" style="color:#E82127;">{crit}</div>
            <div class="hud-meta">Immediate Factory Attention Required</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="hud-card hud-warning">
            <div class="hud-label">Degradation Watchlist</div>
            <div class="hud-value" style="color:#D97706;">{high}</div>
            <div class="hud-meta">Thermal & High-Wear Signatures</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="hud-card hud-success">
            <div class="hud-label">Platform Availability SLA</div>
            <div class="hud-value" style="color:#059669;">{availability:.1f}%</div>
            <div class="hud-meta">Target: >98.0% Global Uptime</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c_chart, c_ai = st.columns([2, 1], gap="medium")

    with c_chart:
        st.markdown("#### **Hazard Distribution Across Platforms**")
        mock_chart_df = pd.DataFrame({
            "CRITICAL": [12, 5, 4, 3],
            "HIGH": [45, 30, 22, 21]
        }, index=["Pulse-Sedan", "Pulse-SUV", "Pulse-GT", "Pulse-EV"])
        st.bar_chart(mock_chart_df)

    with c_ai:
        st.markdown("#### **Executive Briefing Synthesis**")
        st.caption("Powered by Snowflake Cortex with trial-safe execution.")
        if st.button("Generate Morning Fleet Briefing", use_container_width=True, type="primary"):
            with st.spinner("Synthesizing telematics stream..."):
                prompt = f"Executive briefing for {tot} connected units with {crit} critical alarms. Detail warranty risk and 3 supply chain directives."
                briefing = query_cortex_copilot(prompt, user_role=active_profile)
                st.markdown(f"""<div class="copilot-bubble">{briefing.replace(chr(10), '<br>')}</div>""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 13. SCREEN: DEALERSHIP SERVICE TRIAGE & DISPATCH
# -------------------------------------------------------------
elif active_view == "🔧 Service Triage & Dispatch":
    st.markdown("### 🔧 **Dealership Diagnostic Triage & Work Orders**")
    st.caption("Active diagnostic triage queue with automated parts reservation.")

    if session:
        try:
            triage_query = """
            SELECT h.VIN, h.MODEL, h.HIGHEST_COMPONENT_RISK, h.CRITICAL_COMPONENT_AT_RISK,
                   h.MIN_PREDICTED_RUL_DAYS, r.SERVICE_CODE, r.ESTIMATED_COST, h.PRIMARY_DEALER_ID,
                   f.PART_NUMBER_REQUIRED
            FROM AUTOPULSE_DB.MART.DIM_VEHICLE_FLEET_HEALTH h
            JOIN AUTOPULSE_DB.AGENT.SERVICE_RECOMMENDATIONS r ON h.VIN = r.VIN
            LEFT JOIN AUTOPULSE_DB.MART.FACT_SERVICE_MAINTENANCE_ANALYTICS f ON h.VIN = f.VIN
            WHERE r.APPROVAL_STATUS != 'DISPATCHED_TO_WORK_ORDER'
            """
            if f_risk != "ALL":
                triage_query += f" AND h.HIGHEST_COMPONENT_RISK = '{f_risk}'"
            triage_query += " ORDER BY h.MIN_PREDICTED_RUL_DAYS ASC LIMIT 50;"
            df_triage = session.sql(triage_query).to_pandas()
        except Exception:
            df_triage = pd.DataFrame()
    else:
        df_triage = pd.DataFrame([
            {"VIN": "CAR-18391", "MODEL": "Pulse-EV", "HIGHEST_COMPONENT_RISK": "CRITICAL", "CRITICAL_COMPONENT_AT_RISK": "Inverter Phase B", "MIN_PREDICTED_RUL_DAYS": 3, "SERVICE_CODE": "SRV-INV-99", "ESTIMATED_COST": 1850.0, "PRIMARY_DEALER_ID": "DLR-WEST-01", "PART_NUMBER_REQUIRED": "INV-8820-T"},
            {"VIN": "CAR-20412", "MODEL": "Pulse-SUV", "HIGHEST_COMPONENT_RISK": "CRITICAL", "CRITICAL_COMPONENT_AT_RISK": "Brake Actuator", "MIN_PREDICTED_RUL_DAYS": 5, "SERVICE_CODE": "SRV-BRK-04", "ESTIMATED_COST": 420.0, "PRIMARY_DEALER_ID": "DLR-EAST-02", "PART_NUMBER_REQUIRED": "BRK-4001-A"}
        ])

    st.dataframe(df_triage, use_container_width=True, hide_index=True)

    if not df_triage.empty:
        st.markdown("---")
        target_vin = st.selectbox("Select VIN for Dispatch Authorization:", df_triage["VIN"].tolist())
        target_row = df_triage[df_triage["VIN"] == target_vin].iloc[0]

        d1, d2, d3 = st.columns(3)
        d1.write(f"**Target System:** `{target_row['CRITICAL_COMPONENT_AT_RISK']}`")
        d2.write(f"**Service Code:** `{target_row['SERVICE_CODE']}`")
        d3.write(f"**Allocated Node:** `{target_row['PRIMARY_DEALER_ID']}`")

        if st.button("🚀 Authorize Work Order & Reserve Part", type="primary"):
            if session:
                try:
                    sp_sql = f"""
                    CALL AUTOPULSE_DB.SERVICE.SP_AUTHORIZE_REPAIR_AND_RESERVE_INVENTORY(
                        '{target_vin}', '{target_row['PART_NUMBER_REQUIRED']}', '{target_row['PRIMARY_DEALER_ID']}',
                        '{target_row['SERVICE_CODE']}', {float(target_row['ESTIMATED_COST'] or 0.0)}
                    );
                    """
                    out = session.sql(sp_sql).collect()[0][0]
                    st.success(out)
                    st.cache_data.clear()
                except Exception as e:
                    st.error(f"Dispatch failed: {e}")
            else:
                st.success(f"Work order dispatched for {target_vin}. Part {target_row['PART_NUMBER_REQUIRED']} reserved.")

# -------------------------------------------------------------
# 14. SCREEN: INVENTORY & PARTS HUB
# -------------------------------------------------------------
elif active_view == "📦 Inventory & Parts Hub":
    st.markdown("### 📦 **Authorized Dealership Network & Parts Readiness**")
    st.caption("Stock allocation, reservation queues, and stockout alerts.")

    dealers_df = pd.DataFrame([
        {"DEALER_ID": "DLR-WEST-01", "TOTAL_ON_HAND": 482, "TOTAL_RESERVED": 38},
        {"DEALER_ID": "DLR-EAST-02", "TOTAL_ON_HAND": 312, "TOTAL_RESERVED": 19},
        {"DEALER_ID": "DLR-CENTRAL-03", "TOTAL_ON_HAND": 604, "TOTAL_RESERVED": 44}
    ])
    st.dataframe(dealers_df, use_container_width=True, hide_index=True)

# -------------------------------------------------------------
# 15. SCREEN: QUALITY & RELIABILITY LAB
# -------------------------------------------------------------
elif active_view == "📈 Quality & Degradation Lab":
    st.markdown("### 📈 **OEM Reliability Engineering & Sensor Degradation**")
    st.caption("Cross-fleet failure rate patterns, warranty claims exposure, and early warning batch indicators.")

    q1, q2 = st.columns(2, gap="large")
    with q1:
        st.markdown("#### **Component Failure Distribution**")
        mock_comp_df = pd.DataFrame({
            "TARGET_COMPONENT": ["Inverter Phase B", "Brake Actuator", "Battery Thermal Pump", "Steering Rack"],
            "CRITICAL_FAILURES": [18, 14, 8, 3],
            "AVG_RUL_DAYS": [4.2, 6.8, 12.1, 21.0]
        })
        st.dataframe(mock_comp_df, use_container_width=True, hide_index=True)

    with q2:
        st.markdown("#### **Warranty Cost Exposure by Platform (USD)**")
        mock_exposure = pd.DataFrame({
            "EXPOSURE_USD": [142000, 98000, 65000, 32000]
        }, index=["Pulse-EV", "Pulse-SUV", "Pulse-Sedan", "Pulse-GT"])
        st.bar_chart(mock_exposure)

# -------------------------------------------------------------
# 16. SCREEN: VEHICLE 360 & ISO DOSSIER
# -------------------------------------------------------------
elif active_view == "🚗 Vehicle 360 & ISO Dossier":
    st.markdown("### 🚗 **Vehicle 360 Diagnostic Dossier & Technical Report**")
    st.caption("Deep telematics telemetry, rolling sensor graphs, and exportable ISO 26262 ASIL-D certificates.")

    vin_list = ["CAR-18391", "CAR-20412", "CAR-99120", "CAR-33104"]
    if session:
        try:
            db_vins = session.sql("SELECT VIN FROM AUTOPULSE_DB.MART.DIM_VEHICLE_FLEET_HEALTH ORDER BY MIN_PREDICTED_RUL_DAYS ASC LIMIT 50").to_pandas()["VIN"].tolist()
            if db_vins:
                vin_list = db_vins
        except Exception:
            pass

    sel_vin = st.selectbox("Select Target VIN Asset:", vin_list)

    if session:
        try:
            v_meta = session.sql(f"""
                SELECT 
                    m.VIN, m.MODEL, m.VARIANT, m.MODEL_YEAR, m.CURRENT_ODOMETER_KM, m.WARRANTY_STATUS,
                    m.CRITICAL_COMPONENT_AT_RISK, m.HIGHEST_COMPONENT_RISK, m.MIN_PREDICTED_RUL_DAYS,
                    m.PRIMARY_DEALER_ID, f.RECOMMENDED_SERVICE_CODE, f.ESTIMATED_REPAIR_COST,
                    f.PART_NUMBER_REQUIRED, f.DEALER_PARTS_ON_HAND
                FROM AUTOPULSE_DB.MART.DIM_VEHICLE_FLEET_HEALTH m
                LEFT JOIN AUTOPULSE_DB.MART.FACT_SERVICE_MAINTENANCE_ANALYTICS f 
                    ON m.VIN = f.VIN AND f.AGGREGATION_DATE = CURRENT_DATE()
                WHERE m.VIN = '{sel_vin}'
                LIMIT 1;
            """).to_pandas().iloc[0].to_dict()
        except Exception:
            v_meta = {
                "MODEL": "Pulse-EV", "VARIANT": "Performance Dual-Motor", "MODEL_YEAR": "2025",
                "CURRENT_ODOMETER_KM": 42180, "WARRANTY_STATUS": "ACTIVE",
                "CRITICAL_COMPONENT_AT_RISK": "Inverter Phase B", "HIGHEST_COMPONENT_RISK": "CRITICAL",
                "MIN_PREDICTED_RUL_DAYS": 3, "PRIMARY_DEALER_ID": "DLR-WEST-01",
                "RECOMMENDED_SERVICE_CODE": "SRV-INV-99", "ESTIMATED_REPAIR_COST": 1850.0,
                "PART_NUMBER_REQUIRED": "INV-8820-T", "DEALER_PARTS_ON_HAND": 4
            }
    else:
        v_meta = {
            "MODEL": "Pulse-EV", "VARIANT": "Performance Dual-Motor", "MODEL_YEAR": "2025",
            "CURRENT_ODOMETER_KM": 42180, "WARRANTY_STATUS": "ACTIVE",
            "CRITICAL_COMPONENT_AT_RISK": "Inverter Phase B", "HIGHEST_COMPONENT_RISK": "CRITICAL",
            "MIN_PREDICTED_RUL_DAYS": 3, "PRIMARY_DEALER_ID": "DLR-WEST-01",
            "RECOMMENDED_SERVICE_CODE": "SRV-INV-99", "ESTIMATED_REPAIR_COST": 1850.0,
            "PART_NUMBER_REQUIRED": "INV-8820-T", "DEALER_PARTS_ON_HAND": 4
        }

    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Asset Platform", f"{v_meta.get('MODEL_YEAR', '2025')} {v_meta.get('MODEL', 'Pulse-EV')}")
    t2.metric("Odometer", f"{int(v_meta.get('CURRENT_ODOMETER_KM', 42000)):,} km")
    t3.metric("Critical Component", v_meta.get('CRITICAL_COMPONENT_AT_RISK', 'N/A'))
    t4.metric("Forecast RUL", f"{int(v_meta.get('MIN_PREDICTED_RUL_DAYS', 5))} Days", delta="-Critical Alert", delta_color="inverse")

    st.markdown("---")
    g_col, r_col = st.columns([1, 1], gap="large")

    with g_col:
        st.markdown("#### **Sensor Stress Signatures (14-Day Dual-Trace)**")
        loaded_chart = False
        if session:
            try:
                sensor_df = session.sql(f"""
                    SELECT 
                        TO_VARCHAR(FEATURE_DATE, 'YYYY-MM-DD') AS FEATURE_DATE,
                        ROUND(AVG_BRAKE_TEMP_C, 2) AS "Brake Temp (°C)",
                        SEVERE_ROUGHNESS_CYCLES AS "Chassis Vibrations"
                    FROM AUTOPULSE_DB.FEATURES.VEHICLE_TELEMETRY_DAILY_AGG
                    WHERE VIN = '{sel_vin}'
                      AND FEATURE_DATE >= DATEADD('day', -30, CURRENT_DATE())
                      AND FEATURE_DATE <= DATEADD('day', 1, CURRENT_DATE())
                    ORDER BY FEATURE_DATE ASC
                    LIMIT 14;
                """).to_pandas()
                if not sensor_df.empty:
                    st.line_chart(sensor_df.set_index("FEATURE_DATE")[["Brake Temp (°C)", "Chassis Vibrations"]])
                    loaded_chart = True
            except Exception:
                pass
        
        if not loaded_chart:
            mock_trace = pd.DataFrame({
                "Brake Temp (°C)": [42, 45, 51, 68, 72, 85, 94, 91, 88, 97, 102, 108, 115, 122],
                "Chassis Vibrations": [1.1, 1.2, 1.1, 1.4, 1.5, 1.8, 2.1, 2.0, 2.3, 2.7, 3.1, 3.4, 3.8, 4.2]
            }, index=[f"Day -{14 - i}" for i in range(14)])
            st.line_chart(mock_trace)

    with r_col:
        st.markdown("#### **Official ISO 26262 ASIL-D Technical Dossier**")
        st.caption("Generates a signed diagnostic certificate compiled directly from telematics records.")

        if st.button("Generate Diagnostic PDF Dossier", type="primary", use_container_width=True):
            with st.spinner("Compiling technical directives..."):
                prompt = (
                    f"Technical briefing for {sel_vin} ({v_meta.get('MODEL')}). Component at risk: "
                    f"{v_meta.get('CRITICAL_COMPONENT_AT_RISK')} with RUL of {v_meta.get('MIN_PREDICTED_RUL_DAYS')} days. "
                    f"Required Part: {v_meta.get('PART_NUMBER_REQUIRED')}. Service Code: {v_meta.get('RECOMMENDED_SERVICE_CODE')}."
                )
                briefing_text = query_cortex_copilot(prompt, user_role=active_profile)
                pdf_bytes = generate_oem_pdf_report(sel_vin, v_meta, briefing_text)

                st.download_button(
                    label="⬇ Download ISO 26262 ASIL-D Dossier (PDF)",
                    data=pdf_bytes,
                    file_name=f"AutoPulse_Dossier_{sel_vin}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                st.success("ASIL-D Technical Dossier compiled successfully.")