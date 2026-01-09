#!/usr/bin/env python3
"""
PDF Report Generator for MegaDrone Phase 1
Generates comprehensive design documentation

Author: MegaDrone Project
Date: January 8, 2026
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
import numpy as np
from datetime import datetime
import os

# =============================================================================
# DESIGN DATA
# =============================================================================

DESIGN_PARAMS = {
    "mission": {
        "Range": "100 km (round trip)",
        "Cruise Speed": "50 knots (25.7 m/s)",
        "Loiter Time": "15 minutes",
        "Loiter Speed": "29 knots (15.0 m/s)",
        "Cruise Altitude": "150 m AGL",
        "Payload": "0.5 kg camera system",
        "Launch Method": "Hand launch",
    },
    "aircraft": {
        "MTOW": "1.96 kg",
        "Empty Weight": "1.46 kg (est.)",
        "Wing Span": "1.70 m",
        "Wing Area": "0.241 m²",
        "Aspect Ratio": "12.0",
        "Mean Chord": "141.6 mm",
        "Root Chord": "166.6 mm",
        "Tip Chord": "116.6 mm",
        "Taper Ratio": "0.7",
        "Wing Loading": "80 N/m²",
    },
    "performance": {
        "L/D (Cruise)": "21.5",
        "L/D (Max)": "23.2",
        "CL (Cruise)": "0.53",
        "CD (Cruise)": "0.026",
        "Stall Speed": "9.7 m/s (19 kts)",
        "Cruise Power": "66 W",
        "Loiter Power": "21 W",
        "Max Climb Rate": "3.5 m/s (est.)",
    },
    "airfoil": {
        "Type": "Custom NeuralFoil Optimized",
        "Max Thickness": "10.2% at 28% chord",
        "Max Camber": "3.8% at 42% chord",
        "Design Re": "250,000",
        "Design CL": "0.5-0.7",
    },
    "tail": {
        "Horizontal Span": "0.37 m",
        "Horizontal Area": "0.019 m²",
        "Horizontal Volume": "0.55",
        "Vertical Height": "0.12 m",
        "Vertical Area": "0.015 m²",
        "Vertical Volume": "0.045",
        "Tail Arm": "0.50 m",
    },
    "propulsion": {
        "Motor": "SunnySky X2212-980KV (180W)",
        "ESC": "30A BLHeli_S",
        "Propeller": "APC 11x7E",
        "Prop Efficiency (Cruise)": "~75%",
        "Battery": "4S 3300mAh LiPo (117Wh)",
        "System Efficiency": "~70% overall",
    },
    "structure": {
        "Wing Spar": "16mm OD carbon tube",
        "Tail Boom": "12mm OD carbon tube",
        "Wing Construction": "Built-up balsa/foam with film covering",
        "Structure Weight": "667g (over budget by 78g)",
        "Max Wing Deflection": "1.7% of span",
    },
}

WEIGHT_BREAKDOWN = {
    "Wing Structure": 350,
    "Fuselage": 120,
    "Tail": 80,
    "Tail Boom": 50,
    "Motor + ESC": 83,
    "Propeller": 25,
    "Battery": 300,
    "Avionics": 120,
    "Servos (4x)": 20,
    "Wiring/Hardware": 50,
    "Payload": 500,
    "Margin": 62,
}

COST_BREAKDOWN = {
    "Airframe": 228,
    "Propulsion": 73,
    "Battery & Power": 185,
    "Avionics": 233,
    "Hardware": 54,
    "Ground Support": 365,
}


# =============================================================================
# PDF GENERATION
# =============================================================================

def create_title_page(pdf):
    """Create title page."""
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis('off')

    # Title
    ax.text(0.5, 0.75, "MegaDrone Phase 1", fontsize=32, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)
    ax.text(0.5, 0.68, "UAV Design Report", fontsize=24,
            ha='center', va='center', transform=ax.transAxes, color='#555555')

    # Subtitle
    ax.text(0.5, 0.55, "Small Fixed-Wing Electric Surveillance Drone", fontsize=14,
            ha='center', va='center', transform=ax.transAxes, style='italic')

    # Key specs box
    specs = [
        "100 km Range  |  50 knot Cruise  |  1.96 kg MTOW",
        "1.70 m Wingspan  |  L/D = 21.5  |  Hand Launch"
    ]
    for i, spec in enumerate(specs):
        ax.text(0.5, 0.45 - i*0.04, spec, fontsize=11,
                ha='center', va='center', transform=ax.transAxes, color='#333333')

    # Horizontal line
    ax.axhline(y=0.38, xmin=0.15, xmax=0.85, color='#cccccc', linewidth=2)

    # Project info
    ax.text(0.5, 0.30, "Design & Analysis using AeroSandbox + NeuralFoil", fontsize=10,
            ha='center', va='center', transform=ax.transAxes)

    # Date and version
    ax.text(0.5, 0.15, f"Report Date: {datetime.now().strftime('%B %d, %Y')}", fontsize=10,
            ha='center', va='center', transform=ax.transAxes)
    ax.text(0.5, 0.11, "Version 1.0", fontsize=10,
            ha='center', va='center', transform=ax.transAxes)

    # Footer
    ax.text(0.5, 0.03, "DATAWERKES", fontsize=9, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes, color='#888888')

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


def create_toc_page(pdf):
    """Create table of contents."""
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis('off')

    ax.text(0.5, 0.92, "Table of Contents", fontsize=20, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)

    toc = [
        ("1. Executive Summary", 3),
        ("2. Mission Requirements", 4),
        ("3. Aircraft Configuration", 5),
        ("4. Aerodynamic Design", 6),
        ("5. Airfoil Optimization", 7),
        ("6. Structural Design", 8),
        ("7. Propulsion System", 9),
        ("8. Weight & Balance", 10),
        ("9. Performance Summary", 11),
        ("10. Technical Drawings", 12),
        ("11. Bill of Materials", 15),
        ("12. CFD Validation (Future Work)", 16),
        ("13. References", 17),
    ]

    y_start = 0.82
    for i, (title, page) in enumerate(toc):
        y = y_start - i * 0.05
        ax.text(0.15, y, title, fontsize=11, ha='left', va='center', transform=ax.transAxes)
        ax.text(0.85, y, str(page), fontsize=11, ha='right', va='center', transform=ax.transAxes)
        # Dotted line
        ax.plot([0.55, 0.82], [y, y], 'k:', linewidth=0.5, transform=ax.transAxes)

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


def create_text_page(pdf, title, content_dict, page_num):
    """Create a text-based specification page."""
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis('off')

    # Title
    ax.text(0.5, 0.94, title, fontsize=18, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)

    # Content
    y = 0.86
    for section, params in content_dict.items():
        if isinstance(params, dict):
            ax.text(0.08, y, section, fontsize=12, fontweight='bold',
                    ha='left', va='center', transform=ax.transAxes, color='#333333')
            y -= 0.03
            for key, value in params.items():
                ax.text(0.12, y, f"{key}:", fontsize=10,
                        ha='left', va='center', transform=ax.transAxes)
                ax.text(0.55, y, str(value), fontsize=10,
                        ha='left', va='center', transform=ax.transAxes, color='#0066cc')
                y -= 0.025
            y -= 0.02

    # Page number
    ax.text(0.95, 0.02, str(page_num), fontsize=9,
            ha='right', va='bottom', transform=ax.transAxes)

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


def create_executive_summary(pdf):
    """Create executive summary page."""
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis('off')

    ax.text(0.5, 0.94, "1. Executive Summary", fontsize=18, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)

    summary = """
The MegaDrone Phase 1 is a small fixed-wing electric UAV designed for surveillance
and reconnaissance missions with a 0.5 kg camera payload. The aircraft is optimized
for a 100 km round-trip mission profile with 15 minutes loiter time.

KEY DESIGN HIGHLIGHTS:

• High Efficiency: L/D ratio of 21.5 achieved through custom airfoil optimization
  using NeuralFoil neural network analysis

• Long Endurance: 117 Wh battery provides sufficient energy for 100+ km range
  with 20% reserve margin

• Hand Launch Capable: Stall speed of 9.7 m/s enables safe hand launch
  without catapult or runway

• Lightweight Construction: 1.96 kg MTOW with composite/balsa structure

• Autonomous Capability: ArduPilot-compatible avionics with GPS waypoint navigation

DESIGN METHODOLOGY:

The aircraft was designed using AeroSandbox, an open-source MDO framework,
with NeuralFoil for airfoil optimization. Vortex Lattice Method (VLM) analysis
provided aerodynamic coefficients, while beam theory was used for structural
sizing. The propulsion system was matched using blade element momentum theory.

FUTURE WORK:

CFD validation using SU2 or OpenFOAM is recommended to verify VLM predictions
and refine the design before prototype construction. Key areas for validation
include drag prediction and stall behavior.

ESTIMATED COST:

Aircraft (no payload): $773
Ground Support Equipment: $365
Total Project: $1,138
    """

    ax.text(0.08, 0.85, summary, fontsize=9, ha='left', va='top',
            transform=ax.transAxes, family='monospace', linespacing=1.4)

    ax.text(0.95, 0.02, "3", fontsize=9, ha='right', va='bottom', transform=ax.transAxes)

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


def create_mission_page(pdf):
    """Create mission requirements page."""
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis('off')

    ax.text(0.5, 0.94, "2. Mission Requirements", fontsize=18, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)

    # Mission profile diagram (simple text representation)
    ax.text(0.08, 0.86, "MISSION PROFILE:", fontsize=12, fontweight='bold',
            ha='left', va='center', transform=ax.transAxes)

    profile = """
    ┌─────────────────────────────────────────────────────────────┐
    │                    MISSION PROFILE                          │
    │                                                             │
    │        Cruise 50 km ──────►  Loiter  ◄────── Cruise 50 km  │
    │           (50 kts)          15 min           (50 kts)       │
    │     ↗                          │                        ↘   │
    │  Climb                     150m AGL                   Descent│
    │    │                                                     │   │
    │ Launch ──────────────────────────────────────────── Landing │
    └─────────────────────────────────────────────────────────────┘
    """

    ax.text(0.08, 0.72, profile, fontsize=8, ha='left', va='top',
            transform=ax.transAxes, family='monospace')

    # Requirements table
    y = 0.52
    ax.text(0.08, y, "PERFORMANCE REQUIREMENTS:", fontsize=12, fontweight='bold',
            ha='left', va='center', transform=ax.transAxes)

    reqs = [
        ("Total Range", "100 km (50 km out + 50 km return)"),
        ("Cruise Speed", "50 knots (25.7 m/s)"),
        ("Loiter Duration", "15 minutes minimum"),
        ("Loiter Speed", "29 knots (15.0 m/s) for best endurance"),
        ("Operating Altitude", "150 m AGL (nominal)"),
        ("Maximum Altitude", "400 m AGL (regulatory limit)"),
        ("Payload Mass", "0.5 kg camera/sensor package"),
        ("Launch Method", "Hand launch (no catapult/runway)"),
        ("Recovery", "Belly landing on grass/dirt"),
        ("Weather", "Light winds < 10 m/s, no precipitation"),
    ]

    y -= 0.04
    for key, value in reqs:
        ax.text(0.12, y, f"• {key}:", fontsize=10, ha='left', va='center', transform=ax.transAxes)
        ax.text(0.45, y, value, fontsize=10, ha='left', va='center',
                transform=ax.transAxes, color='#0066cc')
        y -= 0.03

    # Energy budget
    y -= 0.04
    ax.text(0.08, y, "ENERGY BUDGET:", fontsize=12, fontweight='bold',
            ha='left', va='center', transform=ax.transAxes)

    energy = [
        ("Cruise (100 km @ 66W)", "71.4 Wh"),
        ("Loiter (15 min @ 21W)", "5.3 Wh"),
        ("Climb + Descent", "~3 Wh"),
        ("Avionics", "~5 Wh"),
        ("Total Required", "~85 Wh"),
        ("Battery Capacity", "117 Wh (4S 3300mAh)"),
        ("Reserve Margin", "27% (above 20% minimum)"),
    ]

    y -= 0.04
    for key, value in energy:
        ax.text(0.12, y, f"• {key}:", fontsize=10, ha='left', va='center', transform=ax.transAxes)
        ax.text(0.50, y, value, fontsize=10, ha='left', va='center',
                transform=ax.transAxes, color='#0066cc')
        y -= 0.03

    ax.text(0.95, 0.02, "4", fontsize=9, ha='right', va='bottom', transform=ax.transAxes)

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


def create_config_page(pdf):
    """Create aircraft configuration page."""
    content = {
        "General Configuration": DESIGN_PARAMS["aircraft"],
        "Tail Surfaces": DESIGN_PARAMS["tail"],
    }
    create_text_page(pdf, "3. Aircraft Configuration", content, 5)


def create_aero_page(pdf):
    """Create aerodynamic design page."""
    content = {
        "Performance Coefficients": DESIGN_PARAMS["performance"],
        "Airfoil Characteristics": DESIGN_PARAMS["airfoil"],
    }
    create_text_page(pdf, "4. Aerodynamic Design", content, 6)


def create_airfoil_page(pdf):
    """Create airfoil optimization page."""
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis('off')

    ax.text(0.5, 0.94, "5. Airfoil Optimization", fontsize=18, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)

    # Try to load airfoil image
    airfoil_img_path = '/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/optimized_airfoil.png'
    if os.path.exists(airfoil_img_path):
        img = mpimg.imread(airfoil_img_path)
        ax_img = fig.add_axes([0.1, 0.55, 0.8, 0.35])
        ax_img.imshow(img)
        ax_img.axis('off')
        ax_img.set_title('Optimized Airfoil Shape', fontsize=10)

    # Optimization details
    details = """
OPTIMIZATION METHOD: NeuralFoil + Gradient-Based Optimization

NeuralFoil is a neural network trained on XFoil data that provides
C∞-continuous gradients for airfoil performance prediction. This enables
efficient gradient-based optimization of airfoil shape.

DESIGN VARIABLES:
• 8 upper surface CST parameters
• 8 lower surface CST parameters
• Leading edge class function parameter
• Trailing edge boat-tail angle

OBJECTIVE: Maximize L/D at Re = 250,000, CL = 0.5-0.7

CONSTRAINTS:
• Minimum thickness: 8% chord (for structure)
• Maximum thickness: 12% chord (drag limit)
• Pitching moment: CM > -0.10 (stability)

RESULTS:
• Achieved L/D = 106.3 at optimum CL (2D, inviscid baseline)
• 3D aircraft L/D = 21.5 including induced drag and parasite drag
• Smooth pressure distribution with delayed separation
• Benign stall characteristics (gradual lift loss)

VALIDATION REQUIRED:
• XFOIL viscous analysis at design Reynolds number
• SU2 CFD for 3D flow effects near stall
• Wind tunnel testing (if available)
    """

    ax.text(0.08, 0.48, details, fontsize=9, ha='left', va='top',
            transform=ax.transAxes, family='monospace', linespacing=1.3)

    ax.text(0.95, 0.02, "7", fontsize=9, ha='right', va='bottom', transform=ax.transAxes)

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


def create_structure_page(pdf):
    """Create structural design page."""
    content = {
        "Structural Components": DESIGN_PARAMS["structure"],
        "Construction Method": {
            "Wing": "Built-up balsa ribs with EPP foam LE, film covering",
            "Fuselage": "Carbon/plywood composite pod",
            "Tail Boom": "12mm carbon tube with internal routing",
            "Control Surfaces": "Balsa frame with film covering",
        },
    }
    create_text_page(pdf, "6. Structural Design", content, 8)


def create_propulsion_page(pdf):
    """Create propulsion system page."""
    content = {
        "Propulsion Components": DESIGN_PARAMS["propulsion"],
        "Operating Points": {
            "Cruise RPM": "~7,500 RPM",
            "Cruise Current": "~5A",
            "Loiter RPM": "~5,000 RPM",
            "Loiter Current": "~2A",
            "Max Power (Climb)": "~150W",
        },
    }
    create_text_page(pdf, "7. Propulsion System", content, 9)


def create_weight_page(pdf):
    """Create weight and balance page with pie chart."""
    fig = plt.figure(figsize=(8.5, 11))

    # Title
    ax_title = fig.add_axes([0, 0.9, 1, 0.1])
    ax_title.axis('off')
    ax_title.text(0.5, 0.5, "8. Weight & Balance", fontsize=18, fontweight='bold',
                  ha='center', va='center', transform=ax_title.transAxes)

    # Pie chart
    ax_pie = fig.add_axes([0.15, 0.45, 0.7, 0.4])

    labels = list(WEIGHT_BREAKDOWN.keys())
    sizes = list(WEIGHT_BREAKDOWN.values())
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

    wedges, texts, autotexts = ax_pie.pie(sizes, labels=labels, autopct='%1.0f%%',
                                           colors=colors, pctdistance=0.8)
    ax_pie.set_title('Weight Breakdown (grams)', fontsize=12, pad=10)

    # Make percentage labels smaller
    for autotext in autotexts:
        autotext.set_fontsize(8)
    for text in texts:
        text.set_fontsize(8)

    # Weight table
    ax_table = fig.add_axes([0.1, 0.08, 0.8, 0.32])
    ax_table.axis('off')

    y = 0.95
    ax_table.text(0.0, y, "WEIGHT SUMMARY", fontsize=11, fontweight='bold',
                  ha='left', va='center', transform=ax_table.transAxes)

    y -= 0.1
    total = sum(WEIGHT_BREAKDOWN.values())
    for component, weight in WEIGHT_BREAKDOWN.items():
        pct = weight / total * 100
        ax_table.text(0.05, y, f"{component}:", fontsize=9,
                      ha='left', va='center', transform=ax_table.transAxes)
        ax_table.text(0.55, y, f"{weight:4d} g", fontsize=9,
                      ha='right', va='center', transform=ax_table.transAxes)
        ax_table.text(0.70, y, f"({pct:4.1f}%)", fontsize=9,
                      ha='right', va='center', transform=ax_table.transAxes, color='#666666')
        y -= 0.065

    ax_table.axhline(y=y+0.03, xmin=0.05, xmax=0.70, color='black', linewidth=0.5)
    y -= 0.02
    ax_table.text(0.05, y, "TOTAL (MTOW):", fontsize=10, fontweight='bold',
                  ha='left', va='center', transform=ax_table.transAxes)
    ax_table.text(0.55, y, f"{total:4d} g", fontsize=10, fontweight='bold',
                  ha='right', va='center', transform=ax_table.transAxes)

    # Page number
    fig.text(0.95, 0.02, "10", fontsize=9, ha='right', va='bottom')

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


def create_performance_page(pdf):
    """Create performance summary page."""
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis('off')

    ax.text(0.5, 0.94, "9. Performance Summary", fontsize=18, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)

    performance = """
CRUISE PERFORMANCE (50 knots, 150m altitude)
─────────────────────────────────────────────
  Lift Coefficient (CL):        0.53
  Drag Coefficient (CD):        0.026
  Lift-to-Drag Ratio:           21.5
  Required Thrust:              2.57 N
  Required Power (shaft):       66 W
  Propeller Efficiency:         ~75%
  System Power (electrical):    88 W
  Cruise Endurance:             1.3 hours (with 117 Wh battery)

LOITER PERFORMANCE (29 knots, 150m altitude)
─────────────────────────────────────────────
  Lift Coefficient (CL):        0.80
  Drag Coefficient (CD):        0.035
  Lift-to-Drag Ratio:           22.8
  Required Thrust:              0.84 N
  Required Power (shaft):       21 W
  System Power (electrical):    30 W
  Loiter Endurance:             3.9 hours (max)

STALL CHARACTERISTICS
─────────────────────────────────────────────
  Stall Speed (level flight):   9.7 m/s (19 kts)
  Stall Angle:                  ~12° (estimated)
  Stall Behavior:               Gradual (optimized airfoil)

CLIMB PERFORMANCE (estimated)
─────────────────────────────────────────────
  Max Climb Rate:               3.5 m/s (700 ft/min)
  Best Climb Speed:             15 m/s
  Climb Power:                  150 W (motor max continuous)

DESIGN POINT VERIFICATION
─────────────────────────────────────────────
  Mission Energy Required:      85 Wh
  Battery Capacity:             117 Wh
  Reserve Margin:               27% (>20% requirement)
  Weight Budget:                1.96 kg (on target)
  Wing Loading:                 80 N/m² (within limits)

PERFORMANCE MARGINS
─────────────────────────────────────────────
  Range Margin:                 +27% beyond 100 km
  Stall Margin at Launch:       +8 m/s above stall
  Power Margin at Cruise:       56% (150W available, 66W required)
    """

    ax.text(0.08, 0.88, performance, fontsize=9, ha='left', va='top',
            transform=ax.transAxes, family='monospace', linespacing=1.2)

    ax.text(0.95, 0.02, "11", fontsize=9, ha='right', va='bottom', transform=ax.transAxes)

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


def create_drawing_page(pdf, image_path, title, page_num):
    """Create a page with a technical drawing."""
    fig = plt.figure(figsize=(8.5, 11))

    # Title
    ax_title = fig.add_axes([0, 0.92, 1, 0.08])
    ax_title.axis('off')
    ax_title.text(0.5, 0.5, title, fontsize=14, fontweight='bold',
                  ha='center', va='center', transform=ax_title.transAxes)

    # Image
    if os.path.exists(image_path):
        img = mpimg.imread(image_path)
        ax_img = fig.add_axes([0.02, 0.05, 0.96, 0.85])
        ax_img.imshow(img)
        ax_img.axis('off')
    else:
        ax_img = fig.add_axes([0.1, 0.1, 0.8, 0.8])
        ax_img.text(0.5, 0.5, f"Image not found:\n{image_path}",
                    ha='center', va='center', transform=ax_img.transAxes)
        ax_img.axis('off')

    # Page number
    fig.text(0.95, 0.02, str(page_num), fontsize=9, ha='right', va='bottom')

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


def create_bom_page(pdf):
    """Create bill of materials summary page."""
    fig = plt.figure(figsize=(8.5, 11))

    # Title
    ax_title = fig.add_axes([0, 0.9, 1, 0.1])
    ax_title.axis('off')
    ax_title.text(0.5, 0.5, "11. Bill of Materials Summary", fontsize=18, fontweight='bold',
                  ha='center', va='center', transform=ax_title.transAxes)

    # Cost pie chart
    ax_pie = fig.add_axes([0.1, 0.5, 0.5, 0.38])

    labels = list(COST_BREAKDOWN.keys())
    sizes = list(COST_BREAKDOWN.values())
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(labels)))

    wedges, texts, autotexts = ax_pie.pie(sizes, labels=labels, autopct='$%1.0f',
                                           colors=colors, pctdistance=0.75)
    ax_pie.set_title('Cost by Category', fontsize=11)

    for autotext in autotexts:
        autotext.set_fontsize(9)
    for text in texts:
        text.set_fontsize(9)

    # Cost summary
    ax_summary = fig.add_axes([0.55, 0.5, 0.4, 0.38])
    ax_summary.axis('off')

    ax_summary.text(0.0, 0.95, "COST SUMMARY", fontsize=11, fontweight='bold',
                    ha='left', va='center', transform=ax_summary.transAxes)

    y = 0.85
    total = sum(COST_BREAKDOWN.values())
    for category, cost in COST_BREAKDOWN.items():
        ax_summary.text(0.05, y, f"{category}:", fontsize=9,
                        ha='left', va='center', transform=ax_summary.transAxes)
        ax_summary.text(0.95, y, f"${cost}", fontsize=9,
                        ha='right', va='center', transform=ax_summary.transAxes)
        y -= 0.10

    ax_summary.axhline(y=y+0.05, xmin=0.05, xmax=0.95, color='black', linewidth=0.5)
    y -= 0.05
    ax_summary.text(0.05, y, "TOTAL:", fontsize=10, fontweight='bold',
                    ha='left', va='center', transform=ax_summary.transAxes)
    ax_summary.text(0.95, y, f"${total}", fontsize=10, fontweight='bold',
                    ha='right', va='center', transform=ax_summary.transAxes)

    # Notes
    ax_notes = fig.add_axes([0.08, 0.08, 0.84, 0.38])
    ax_notes.axis('off')

    notes = """
KEY COMPONENTS:
───────────────────────────────────────────────────────────────────────────────
• Motor: SunnySky X2212-980KV ($28) - 180W continuous, 58g
• ESC: 30A BLHeli_S ($18) - with 5V BEC for servos
• Battery: 4S 3300mAh 30C LiPo ($45 x2) - 117Wh, ~300g each
• Flight Controller: Matek F405-Wing ($55) - ArduPilot compatible
• GPS: BN-880 ($22) - 10Hz update rate with compass
• Servos: Savox SH-0254 ($12 x4) - 3.9g digital micro servos
• Propeller: APC 11x7E ($6 x3) - thin electric, includes spares

COST NOTES:
───────────────────────────────────────────────────────────────────────────────
• All prices are estimates from typical online suppliers
• Payload (camera system) NOT included in BOM
• Ground support includes RC transmitter ($250) - may be owned
• Aircraft-only cost (no GSE): $773
• Prices may vary by supplier and region
• Consider 10-15% contingency for shipping and misc items

See designs/bill_of_materials.csv for complete itemized list.
    """

    ax_notes.text(0.0, 0.95, notes, fontsize=9, ha='left', va='top',
                  transform=ax_notes.transAxes, family='monospace', linespacing=1.3)

    # Page number
    fig.text(0.95, 0.02, "15", fontsize=9, ha='right', va='bottom')

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


def create_cfd_page(pdf):
    """Create CFD validation future work page."""
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis('off')

    ax.text(0.5, 0.94, "12. CFD Validation (Future Work)", fontsize=18, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)

    content = """
PURPOSE OF CFD VALIDATION
─────────────────────────────────────────────────────────────────────────
The VLM (Vortex Lattice Method) analysis provides good preliminary estimates
but has limitations. CFD validation is recommended to:

• Verify viscous drag predictions (VLM excludes boundary layer effects)
• Confirm stall angle and post-stall behavior
• Validate pressure distributions for structural loading
• Identify any flow separation or adverse interactions

RECOMMENDED APPROACH: TIERED VALIDATION
─────────────────────────────────────────────────────────────────────────

TIER 1: XFOIL/XFLR5 (Airfoil Validation)
• Complexity: Low | Cost: Free | Time: Hours
• Validate 2D airfoil performance at Re = 250,000
• Compare CL, CD, CM with NeuralFoil predictions
• Installation: brew install xfoil (macOS)

TIER 2: SU2 (3D CFD - Recommended)
• Complexity: Medium | Cost: Free | Time: Days
• Stanford University's open-source CFD solver
• Excellent for aerodynamic applications
• RANS with SA or k-ω SST turbulence model
• Installation: brew install su2 (macOS, including Apple Silicon)
• Website: https://su2code.github.io/

TIER 3: OpenFOAM (Advanced)
• Complexity: High | Cost: Free | Time: Week+
• Most powerful open-source CFD
• Overkill for this application unless learning CFD

VALIDATION TARGETS
─────────────────────────────────────────────────────────────────────────
Parameter        | VLM Value | CFD Target Accuracy
─────────────────|───────────|─────────────────────
CL (cruise)      | 0.53      | ±5%
CD (total)       | 0.026     | ±10%
L/D              | 21.5      | ±10%
CM               | -0.02     | ±20%
Stall angle      | ~12°      | ±2°

SU2 ON APPLE SILICON MACS
─────────────────────────────────────────────────────────────────────────
Yes, SU2 runs natively on Apple Silicon (M1/M2/M3/M4) Macs.
Install via Homebrew: brew install su2
Performance is excellent due to unified memory architecture.

WORKFLOW SUMMARY
─────────────────────────────────────────────────────────────────────────
1. Export geometry to STL from OpenVSP model
2. Generate mesh using Gmsh or SU2 built-in tools
3. Configure RANS simulation at cruise conditions
4. Run SU2_CFD and post-process with ParaView
5. Compare results with VLM predictions
6. Iterate design if significant discrepancies found

See docs/CFD_VALIDATION_GUIDE.md for detailed instructions.
    """

    ax.text(0.08, 0.88, content, fontsize=9, ha='left', va='top',
            transform=ax.transAxes, family='monospace', linespacing=1.2)

    ax.text(0.95, 0.02, "16", fontsize=9, ha='right', va='bottom', transform=ax.transAxes)

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


def create_references_page(pdf):
    """Create references page."""
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.axis('off')

    ax.text(0.5, 0.94, "13. References", fontsize=18, fontweight='bold',
            ha='center', va='center', transform=ax.transAxes)

    references = """
DESIGN TOOLS
─────────────────────────────────────────────────────────────────────────
[1] AeroSandbox - Open-source aircraft design optimization
    https://github.com/peterdsharpe/AeroSandbox

[2] NeuralFoil - Neural network airfoil analysis
    https://github.com/peterdsharpe/NeuralFoil

[3] OpenVSP - NASA parametric aircraft geometry tool
    https://openvsp.org/

CFD TOOLS
─────────────────────────────────────────────────────────────────────────
[4] SU2 - Stanford University Unstructured CFD solver
    https://su2code.github.io/

[5] OpenFOAM - Open-source CFD toolkit
    https://www.openfoam.com/

[6] XFOIL - Subsonic airfoil development system
    https://web.mit.edu/drela/Public/web/xfoil/

[7] ParaView - Open-source scientific visualization
    https://www.paraview.org/

FLIGHT CONTROL
─────────────────────────────────────────────────────────────────────────
[8] ArduPilot - Open-source autopilot software
    https://ardupilot.org/

[9] Mission Planner - Ground control station
    https://ardupilot.org/planner/

TEXTBOOKS & REFERENCES
─────────────────────────────────────────────────────────────────────────
[10] Raymer, D.P. "Aircraft Design: A Conceptual Approach"
     AIAA Education Series

[11] Anderson, J.D. "Fundamentals of Aerodynamics"
     McGraw-Hill

[12] Drela, M. "Flight Vehicle Aerodynamics"
     MIT Press

PROJECT FILES
─────────────────────────────────────────────────────────────────────────
• Aircraft Model:     scripts/aerosandbox_model_v2.py
• Sizing Analysis:    scripts/drone_sizing.py
• Airfoil Design:     scripts/airfoil_optimization.py
• Structural:         scripts/structural_analysis.py
• Propulsion:         scripts/propeller_design.py
• Technical Drawings: scripts/technical_drawings.py
• Bill of Materials:  scripts/bill_of_materials.py
• CFD Guide:          docs/CFD_VALIDATION_GUIDE.md
    """

    ax.text(0.08, 0.88, references, fontsize=9, ha='left', va='top',
            transform=ax.transAxes, family='monospace', linespacing=1.3)

    ax.text(0.95, 0.02, "17", fontsize=9, ha='right', va='bottom', transform=ax.transAxes)

    pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Generate complete PDF report."""

    output_path = '/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/MegaDrone_Design_Report.pdf'

    print("=" * 70)
    print("Generating MegaDrone Phase 1 Design Report")
    print("=" * 70)

    with PdfPages(output_path) as pdf:
        print("  Creating title page...")
        create_title_page(pdf)

        print("  Creating table of contents...")
        create_toc_page(pdf)

        print("  Creating executive summary...")
        create_executive_summary(pdf)

        print("  Creating mission requirements...")
        create_mission_page(pdf)

        print("  Creating aircraft configuration...")
        create_config_page(pdf)

        print("  Creating aerodynamic design...")
        create_aero_page(pdf)

        print("  Creating airfoil optimization...")
        create_airfoil_page(pdf)

        print("  Creating structural design...")
        create_structure_page(pdf)

        print("  Creating propulsion system...")
        create_propulsion_page(pdf)

        print("  Creating weight & balance...")
        create_weight_page(pdf)

        print("  Creating performance summary...")
        create_performance_page(pdf)

        # Technical drawings
        print("  Adding technical drawings...")
        drawings = [
            ('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/three_view_drawing.png',
             "10. Technical Drawings - Three View", 12),
            ('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/wing_detail.png',
             "10. Technical Drawings - Wing Detail", 13),
            ('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/component_layout.png',
             "10. Technical Drawings - Component Layout", 14),
        ]

        for img_path, title, page in drawings:
            create_drawing_page(pdf, img_path, title, page)

        print("  Creating bill of materials...")
        create_bom_page(pdf)

        print("  Creating CFD validation section...")
        create_cfd_page(pdf)

        print("  Creating references...")
        create_references_page(pdf)

    print(f"\n{'=' * 70}")
    print(f"Report generated: {output_path}")
    print(f"{'=' * 70}")

    return output_path


if __name__ == "__main__":
    pdf_path = main()
