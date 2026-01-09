"""Company profiles and fundamental data for semiconductor stocks."""

from typing import Dict, List
from pydantic import BaseModel


class CompanyProfile(BaseModel):
    """Profile information for a semiconductor company."""

    symbol: str
    name: str
    focus_area: str
    market_cap_tier: str  # "mega", "large", "mid"
    ai_exposure: str  # "high", "medium", "low"
    key_products: List[str]
    growth_drivers: List[str]
    analyst_rating: str  # "Strong Buy", "Buy", "Hold", "Sell"
    key_metrics: Dict[str, str]


# Deep research compiled from web search as of January 2026
COMPANY_PROFILES: Dict[str, CompanyProfile] = {
    "NVDA": CompanyProfile(
        symbol="NVDA",
        name="NVIDIA Corporation",
        focus_area="AI GPUs, Data Centers",
        market_cap_tier="mega",
        ai_exposure="high",
        key_products=["Blackwell GPUs", "Hopper GPUs", "CUDA Platform", "Rubin (announced)"],
        growth_drivers=[
            "92% discrete GPU market share",
            "Data center revenue $51.2B in Q3 FY2026",
            "FY2026 revenue projected to grow 63% YoY",
            "AI capex expected to grow 50-60% in 2026",
        ],
        analyst_rating="Strong Buy",
        key_metrics={
            "Q3 FY2026 Revenue": "$57.0B",
            "Data Center Revenue": "$51.2B (90% of total)",
            "FY2026 Revenue Growth": "+63% YoY",
            "2026 Revenue Forecast": "$321.2B",
        },
    ),
    "TSM": CompanyProfile(
        symbol="TSM",
        name="Taiwan Semiconductor Manufacturing",
        focus_area="Contract Chip Manufacturing",
        market_cap_tier="mega",
        ai_exposure="high",
        key_products=["3nm Process (N3)", "2nm Process (N2)", "Advanced Packaging (CoWoS)"],
        growth_drivers=[
            "2nm production started Q4 2025",
            "2nm capacity fully booked by Apple/Nvidia through 2026",
            "AI chip sales ~30% of 2025 revenue (Company Guidance)",
            "Revenue growth 35-37% in 2025",
        ],
        analyst_rating="Strong Buy",
        key_metrics={
            "2025 Revenue Growth": "+35-37%",
            "AI Revenue Share": "~30%",
            "2026 Revenue Growth": "+20.8% YoY forecast",
            "2025 CapEx": "$40-42B",
        },
    ),
    "AVGO": CompanyProfile(
        symbol="AVGO",
        name="Broadcom Inc.",
        focus_area="Networking, Custom AI Silicon",
        market_cap_tier="mega",
        ai_exposure="high",
        key_products=["Custom AI Accelerators (XPUs)", "Networking ASICs", "VMware Software"],
        growth_drivers=[
            "AI semiconductor revenue +74% YoY to $6.5B (Q4 Earnings)",
            "Next quarter AI revenue guidance $8.2B",
            "Backlog surged to $162B (73B AI + 73B Software)",
            "FY2026 revenue forecast 50% growth to $96B",
        ],
        analyst_rating="Strong Buy",
        key_metrics={
            "AI Revenue (Q)": "$6.5B (+74% YoY)",
            "Next Q AI Guidance": "$8.2B",
            "Total Backlog": "$162B",
            "FY2026 Revenue Forecast": "$96B (+50%)",
        },
    ),
    "ASML": CompanyProfile(
        symbol="ASML",
        name="ASML Holding N.V.",
        focus_area="Lithography Equipment",
        market_cap_tier="mega",
        ai_exposure="high",
        key_products=["EUV Lithography (Twinscan NXE)", "High-NA EUV", "DUV Systems"],
        growth_drivers=[
            "Sole provider of advanced EUV equipment",
            "2025 earnings +28% on +15% revenue",
            "TSMC capex boost drives demand",
            "Chiplet adoption for AI increases EUV need",
        ],
        analyst_rating="Buy",
        key_metrics={
            "2025 Earnings Growth": "+28%",
            "2025 Revenue Growth": "+15%",
            "Price Target (Aletheia)": "$1,500",
            "Market Position": "Monopoly in EUV",
        },
    ),
    "QCOM": CompanyProfile(
        symbol="QCOM",
        name="Qualcomm Incorporated",
        focus_area="Mobile Processors, IoT, AI",
        market_cap_tier="large",
        ai_exposure="medium",
        key_products=["Snapdragon Mobile Platforms", "Snapdragon X Elite (PC)", "Automotive Chips"],
        growth_drivers=[
            "AI PC processors gaining traction",
            "Automotive chip business expanding",
            "IoT and edge AI applications",
            "5G modem leadership",
        ],
        analyst_rating="Buy",
        key_metrics={
            "Key Customer": "Apple, Samsung",
            "Growth Segment": "Automotive, IoT",
            "AI Strategy": "On-device AI inference",
            "Market Position": "Mobile SoC leader",
        },
    ),
    "AMD": CompanyProfile(
        symbol="AMD",
        name="Advanced Micro Devices",
        focus_area="CPUs, GPUs, Data Center",
        market_cap_tier="large",
        ai_exposure="high",
        key_products=["EPYC Server CPUs", "MI300X/MI325X AI GPUs", "Ryzen CPUs", "Radeon GPUs"],
        growth_drivers=[
            "2025 AI revenue forecast $9.5B (up from $5.2B)",
            "Revenue +25% YoY projected for 2025",
            "Data center market share gains",
            "MI325X GPU competing with NVIDIA",
        ],
        analyst_rating="Buy",
        key_metrics={
            "2025 AI Revenue": "$9.5B forecast",
            "2025 Revenue Growth": "+25% YoY",
            "Stock Performance 2025": "+70%",
            "Analyst Rating Count": "16 Buy, 0 Sell",
        },
    ),
    "INTC": CompanyProfile(
        symbol="INTC",
        name="Intel Corporation",
        focus_area="CPUs, Foundry Services",
        market_cap_tier="large",
        ai_exposure="medium",
        key_products=["Core Ultra CPUs", "Xeon Data Center CPUs", "Intel Foundry Services", "Gaudi AI Accelerators"],
        growth_drivers=[
            "IDM 2.0 foundry strategy",
            "Intel 18A process development",
            "Gaudi 3 AI accelerator",
            "US CHIPS Act funding recipient",
        ],
        analyst_rating="Hold",
        key_metrics={
            "Strategy": "IDM 2.0 Foundry",
            "2025 CapEx Target": "$18B (down from >$20B)",
            "Key Risk": "Execution on foundry",
            "AI Product": "Gaudi 3 accelerator",
        },
    ),
    "LRCX": CompanyProfile(
        symbol="LRCX",
        name="Lam Research Corporation",
        focus_area="Wafer Fabrication Equipment",
        market_cap_tier="large",
        ai_exposure="high",
        key_products=["Etch Systems", "Deposition Systems", "Clean Systems"],
        growth_drivers=[
            "HBM and 3D NAND manufacturing demand",
            "Strong China demand",
            "AI chip production expansion",
            "Equipment market to hit $133B in 2025",
        ],
        analyst_rating="Buy",
        key_metrics={
            "2026-2028 Revenue CAGR": "10.39%",
            "2026 Revenue Forecast": "$27.24B",
            "Analyst Consensus": "Moderate Buy",
            "Key Driver": "HBM/3D NAND demand",
        },
    ),
    "ADI": CompanyProfile(
        symbol="ADI",
        name="Analog Devices, Inc.",
        focus_area="Industrial Semiconductors",
        market_cap_tier="large",
        ai_exposure="medium",
        key_products=["Analog ICs", "Mixed-Signal ICs", "Power Management", "RF/Microwave"],
        growth_drivers=[
            "FY2026 broad-based growth expected",
            "Datacenter and industrial demand",
            "FY2025 revenue +13% to $10.6B forecast",
            "Recovery from 2024 cyclical downturn",
        ],
        analyst_rating="Buy",
        key_metrics={
            "FY2025 Revenue Forecast": "$10.6B (+13%)",
            "FY2025 EPS Forecast": "$4.35",
            "Earnings Growth": "+12%",
            "Q4 FY2025 Revenue": "$3.08B",
        },
    ),
    "MU": CompanyProfile(
        symbol="MU",
        name="Micron Technology, Inc.",
        focus_area="Memory (DRAM, HBM, NAND)",
        market_cap_tier="large",
        ai_exposure="high",
        key_products=["HBM3E", "HBM4 (development)", "DDR5", "NAND Flash"],
        growth_drivers=[
            "HBM capacity sold out for 2025 and 2026 (Earnings Call)",
            "Core HBM supplier for NVIDIA RTX 50 and Blackwell",
            "Gross margin reached 68%",
            "FY2026 revenue to nearly double vs FY2025",
        ],
        analyst_rating="Strong Buy",
        key_metrics={
            "HBM Capacity": "Sold out 2025-2026",
            "Gross Margin": "68%",
            "FY2026 Revenue": "$70B+ forecast",
            "Key Customer": "NVIDIA (RTX 50 Blackwell)",
        },
    ),
}


def get_company_profile(symbol: str) -> CompanyProfile | None:
    """Get the profile for a given stock symbol."""
    return COMPANY_PROFILES.get(symbol.upper())


def get_all_profiles() -> Dict[str, CompanyProfile]:
    """Get all company profiles."""
    return COMPANY_PROFILES
