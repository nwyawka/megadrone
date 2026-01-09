#!/usr/bin/env python3
"""
Technical Drawings for MegaDrone Phase 1
Generates engineering-style drawings with dimensions

Author: MegaDrone Project
Date: January 8, 2026
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Arc
import numpy as np

# =============================================================================
# DESIGN PARAMETERS (from sizing)
# =============================================================================

# Wing
WINGSPAN = 1.700  # m
SEMI_SPAN = WINGSPAN / 2
ROOT_CHORD = 0.167  # m
TIP_CHORD = 0.117  # m
MEAN_CHORD = 0.142  # m
WING_AREA = 0.241  # m²
DIHEDRAL = 3  # degrees
SWEEP = 0  # degrees (straight LE)

# Fuselage
FUSE_LENGTH = 0.450  # m
FUSE_WIDTH = 0.120  # m
FUSE_HEIGHT = 0.100  # m

# Tail
HTAIL_SPAN = 0.387  # m
HTAIL_CHORD = 0.097  # m
VTAIL_HEIGHT = 0.235  # m
VTAIL_CHORD = 0.157  # m
TAIL_ARM = 0.50  # m

# Overall
TOTAL_LENGTH = FUSE_LENGTH + TAIL_ARM + HTAIL_CHORD
SPAR_DIAMETER = 0.016  # m (16mm)


def add_dimension(ax, start, end, offset, text, horizontal=True, fontsize=8):
    """Add dimension line with arrows and text."""

    if horizontal:
        y_line = start[1] + offset
        ax.annotate('', xy=(end[0], y_line), xytext=(start[0], y_line),
                    arrowprops=dict(arrowstyle='<->', color='black', lw=0.8))
        ax.plot([start[0], start[0]], [start[1], y_line], 'k-', lw=0.5)
        ax.plot([end[0], end[0]], [end[1], y_line], 'k-', lw=0.5)
        ax.text((start[0] + end[0])/2, y_line + 0.01, text,
                ha='center', va='bottom', fontsize=fontsize)
    else:
        x_line = start[0] + offset
        ax.annotate('', xy=(x_line, end[1]), xytext=(x_line, start[1]),
                    arrowprops=dict(arrowstyle='<->', color='black', lw=0.8))
        ax.plot([start[0], x_line], [start[1], start[1]], 'k-', lw=0.5)
        ax.plot([end[0], x_line], [end[1], end[1]], 'k-', lw=0.5)
        ax.text(x_line + 0.01, (start[1] + end[1])/2, text,
                ha='left', va='center', fontsize=fontsize, rotation=90)


def draw_three_view():
    """Create three-view engineering drawing."""

    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('MegaDrone Phase 1 - Three View Drawing', fontsize=14, fontweight='bold')

    # Create subplot grid
    gs = fig.add_gridspec(2, 2, width_ratios=[1.5, 1], height_ratios=[1, 1],
                          hspace=0.3, wspace=0.3)

    # ==================== TOP VIEW ====================
    ax_top = fig.add_subplot(gs[0, 0])
    ax_top.set_title('Top View', fontsize=12, fontweight='bold')
    ax_top.set_aspect('equal')
    ax_top.set_xlim(-0.3, 1.2)
    ax_top.set_ylim(-1.0, 1.0)
    ax_top.axis('off')

    # Wing planform (right side)
    wing_x = [0, ROOT_CHORD, TIP_CHORD + (ROOT_CHORD-TIP_CHORD)*0.25, (ROOT_CHORD-TIP_CHORD)*0.25, 0]
    wing_y = [0, 0, SEMI_SPAN, SEMI_SPAN, 0]
    ax_top.fill(wing_x, wing_y, 'lightblue', edgecolor='black', linewidth=1.5)

    # Wing planform (left side - mirror)
    wing_y_left = [-y for y in wing_y]
    ax_top.fill(wing_x, wing_y_left, 'lightblue', edgecolor='black', linewidth=1.5)

    # Fuselage
    fuse_x = [-0.1, FUSE_LENGTH - 0.1]
    fuse_y_top = [FUSE_WIDTH/2 * 0.3, FUSE_WIDTH/2]
    fuse_y_bot = [-FUSE_WIDTH/2 * 0.3, -FUSE_WIDTH/2]

    # Simplified fuselage shape
    fuse_pts = [
        (-0.1, 0),  # nose
        (0.05, FUSE_WIDTH/2 * 0.7),
        (FUSE_LENGTH * 0.4, FUSE_WIDTH/2),
        (FUSE_LENGTH * 0.7, FUSE_WIDTH/2 * 0.6),
        (FUSE_LENGTH - 0.05, FUSE_WIDTH/2 * 0.1),
        (FUSE_LENGTH - 0.05, -FUSE_WIDTH/2 * 0.1),
        (FUSE_LENGTH * 0.7, -FUSE_WIDTH/2 * 0.6),
        (FUSE_LENGTH * 0.4, -FUSE_WIDTH/2),
        (0.05, -FUSE_WIDTH/2 * 0.7),
        (-0.1, 0),
    ]
    fuse_x = [p[0] for p in fuse_pts]
    fuse_y = [p[1] for p in fuse_pts]
    ax_top.fill(fuse_x, fuse_y, 'lightgray', edgecolor='black', linewidth=1.5)

    # Tail boom
    boom_y = 0.006
    ax_top.fill([FUSE_LENGTH-0.05, FUSE_LENGTH + TAIL_ARM, FUSE_LENGTH + TAIL_ARM, FUSE_LENGTH-0.05],
                [boom_y, boom_y, -boom_y, -boom_y], 'gray', edgecolor='black', linewidth=1)

    # Horizontal tail
    htail_x_start = FUSE_LENGTH + TAIL_ARM - HTAIL_CHORD * 0.3
    htail_pts_r = [
        (htail_x_start, 0),
        (htail_x_start + HTAIL_CHORD, 0),
        (htail_x_start + HTAIL_CHORD * 0.9, HTAIL_SPAN/2),
        (htail_x_start + HTAIL_CHORD * 0.1, HTAIL_SPAN/2),
    ]
    htail_x = [p[0] for p in htail_pts_r]
    htail_y = [p[1] for p in htail_pts_r]
    ax_top.fill(htail_x, htail_y, 'lightyellow', edgecolor='black', linewidth=1)
    htail_y_l = [-y for y in htail_y]
    ax_top.fill(htail_x, htail_y_l, 'lightyellow', edgecolor='black', linewidth=1)

    # Dimensions
    add_dimension(ax_top, (0, 0), (ROOT_CHORD, 0), -0.15, f'{ROOT_CHORD*1000:.0f}mm', fontsize=7)
    add_dimension(ax_top, ((ROOT_CHORD-TIP_CHORD)*0.25, SEMI_SPAN),
                  ((ROOT_CHORD-TIP_CHORD)*0.25 + TIP_CHORD, SEMI_SPAN), 0.08, f'{TIP_CHORD*1000:.0f}mm', fontsize=7)
    add_dimension(ax_top, (ROOT_CHORD, 0), (ROOT_CHORD, SEMI_SPAN), 0.15, f'{SEMI_SPAN*1000:.0f}mm', horizontal=False, fontsize=7)
    add_dimension(ax_top, (-0.1, 0), (FUSE_LENGTH + TAIL_ARM + HTAIL_CHORD*0.7, 0), 0.92,
                  f'Total Length: {(FUSE_LENGTH + TAIL_ARM + HTAIL_CHORD*0.7 + 0.1)*1000:.0f}mm', fontsize=8)

    # Wing spar indicator
    ax_top.plot([ROOT_CHORD*0.3, (ROOT_CHORD-TIP_CHORD)*0.25 + TIP_CHORD*0.3], [0, SEMI_SPAN], 'r--', lw=1.5, label='Main Spar')
    ax_top.plot([ROOT_CHORD*0.3, (ROOT_CHORD-TIP_CHORD)*0.25 + TIP_CHORD*0.3], [0, -SEMI_SPAN], 'r--', lw=1.5)

    ax_top.legend(loc='upper right', fontsize=8)

    # ==================== FRONT VIEW ====================
    ax_front = fig.add_subplot(gs[0, 1])
    ax_front.set_title('Front View', fontsize=12, fontweight='bold')
    ax_front.set_aspect('equal')
    ax_front.set_xlim(-1.0, 1.0)
    ax_front.set_ylim(-0.3, 0.5)
    ax_front.axis('off')

    # Wing with dihedral
    dihedral_rise = SEMI_SPAN * np.tan(np.radians(DIHEDRAL))

    # Right wing
    ax_front.plot([0, SEMI_SPAN], [0, dihedral_rise], 'b-', lw=3)
    ax_front.plot([0, SEMI_SPAN], [-0.01, dihedral_rise-0.01], 'b-', lw=1)

    # Left wing
    ax_front.plot([0, -SEMI_SPAN], [0, dihedral_rise], 'b-', lw=3)
    ax_front.plot([0, -SEMI_SPAN], [-0.01, dihedral_rise-0.01], 'b-', lw=1)

    # Fuselage cross-section
    fuse_ellipse = patches.Ellipse((0, -FUSE_HEIGHT*0.3), FUSE_WIDTH, FUSE_HEIGHT,
                                    facecolor='lightgray', edgecolor='black', linewidth=1.5)
    ax_front.add_patch(fuse_ellipse)

    # Vertical tail
    ax_front.fill([0, 0, 0], [-FUSE_HEIGHT*0.3, -FUSE_HEIGHT*0.3 + VTAIL_HEIGHT, -FUSE_HEIGHT*0.3],
                  'lightyellow', edgecolor='black', linewidth=1)
    vtail_x = [-0.01, 0.01, 0.01, -0.01]
    vtail_y = [-FUSE_HEIGHT*0.3, -FUSE_HEIGHT*0.3, -FUSE_HEIGHT*0.3 + VTAIL_HEIGHT*0.8, -FUSE_HEIGHT*0.3 + VTAIL_HEIGHT*0.8]
    ax_front.fill(vtail_x, vtail_y, 'lightyellow', edgecolor='black', linewidth=1)

    # Propeller disk
    prop_circle = patches.Circle((0, -FUSE_HEIGHT*0.3), 0.14, fill=False,
                                   edgecolor='green', linewidth=1.5, linestyle='--')
    ax_front.add_patch(prop_circle)
    ax_front.text(0, -FUSE_HEIGHT*0.3 - 0.18, 'Prop Disk\n280mm', ha='center', fontsize=7)

    # Dimensions
    add_dimension(ax_front, (-SEMI_SPAN, dihedral_rise), (SEMI_SPAN, dihedral_rise), 0.12,
                  f'Wingspan: {WINGSPAN*1000:.0f}mm', fontsize=8)

    # Dihedral angle
    ax_front.annotate(f'{DIHEDRAL}° Dihedral', xy=(SEMI_SPAN*0.5, dihedral_rise*0.5), fontsize=7)

    # ==================== SIDE VIEW ====================
    ax_side = fig.add_subplot(gs[1, 0])
    ax_side.set_title('Side View', fontsize=12, fontweight='bold')
    ax_side.set_aspect('equal')
    ax_side.set_xlim(-0.3, 1.2)
    ax_side.set_ylim(-0.25, 0.35)
    ax_side.axis('off')

    # Wing profile (airfoil shape simplified)
    wing_x = [0, ROOT_CHORD*0.05, ROOT_CHORD*0.3, ROOT_CHORD, ROOT_CHORD*0.95, ROOT_CHORD*0.3, 0]
    wing_y = [0, 0.012, 0.015, 0.002, -0.005, -0.008, 0]
    ax_side.fill(wing_x, wing_y, 'lightblue', edgecolor='black', linewidth=1.5)

    # Fuselage
    fuse_pts = [
        (-0.1, 0),
        (-0.05, FUSE_HEIGHT*0.4),
        (FUSE_LENGTH*0.3, FUSE_HEIGHT*0.5),
        (FUSE_LENGTH*0.5, FUSE_HEIGHT*0.5),
        (FUSE_LENGTH*0.8, FUSE_HEIGHT*0.3),
        (FUSE_LENGTH, 0),
        (FUSE_LENGTH*0.8, -FUSE_HEIGHT*0.5),
        (FUSE_LENGTH*0.3, -FUSE_HEIGHT*0.6),
        (-0.05, -FUSE_HEIGHT*0.3),
        (-0.1, 0),
    ]
    fuse_x = [p[0] for p in fuse_pts]
    fuse_y = [p[1] for p in fuse_pts]
    ax_side.fill(fuse_x, fuse_y, 'lightgray', edgecolor='black', linewidth=1.5)

    # Tail boom
    ax_side.fill([FUSE_LENGTH, FUSE_LENGTH + TAIL_ARM, FUSE_LENGTH + TAIL_ARM, FUSE_LENGTH],
                 [0.006, 0.006, -0.006, -0.006], 'gray', edgecolor='black', linewidth=1)

    # Horizontal tail
    htail_x_start = FUSE_LENGTH + TAIL_ARM - HTAIL_CHORD * 0.3
    htail_profile = [
        (htail_x_start, 0),
        (htail_x_start + HTAIL_CHORD*0.05, 0.005),
        (htail_x_start + HTAIL_CHORD, 0.002),
        (htail_x_start + HTAIL_CHORD*0.95, -0.002),
        (htail_x_start, 0),
    ]
    ax_side.fill([p[0] for p in htail_profile], [p[1] for p in htail_profile],
                 'lightyellow', edgecolor='black', linewidth=1)

    # Vertical tail
    vtail_x_start = FUSE_LENGTH + TAIL_ARM - VTAIL_CHORD * 0.4
    vtail_pts = [
        (vtail_x_start, 0),
        (vtail_x_start + VTAIL_CHORD, 0),
        (vtail_x_start + VTAIL_CHORD * 0.7, VTAIL_HEIGHT),
        (vtail_x_start + VTAIL_CHORD * 0.1, VTAIL_HEIGHT * 0.8),
        (vtail_x_start, 0),
    ]
    ax_side.fill([p[0] for p in vtail_pts], [p[1] for p in vtail_pts],
                 'lightyellow', edgecolor='black', linewidth=1)

    # Propeller
    ax_side.plot([-0.1, -0.1], [-0.14, 0.14], 'g-', lw=2)
    ax_side.plot([-0.12, -0.08], [0.14, 0.14], 'g-', lw=2)
    ax_side.plot([-0.12, -0.08], [-0.14, -0.14], 'g-', lw=2)

    # Landing skid
    ax_side.plot([FUSE_LENGTH*0.2, FUSE_LENGTH*0.7], [-FUSE_HEIGHT*0.65, -FUSE_HEIGHT*0.65], 'k-', lw=2)

    # Dimensions
    add_dimension(ax_side, (-0.1, 0), (FUSE_LENGTH, 0), -0.18, f'Fuselage: {FUSE_LENGTH*1000:.0f}mm', fontsize=7)
    add_dimension(ax_side, (FUSE_LENGTH, 0), (FUSE_LENGTH + TAIL_ARM, 0), -0.12, f'Boom: {TAIL_ARM*1000:.0f}mm', fontsize=7)
    add_dimension(ax_side, (vtail_x_start, 0), (vtail_x_start, VTAIL_HEIGHT), -0.08,
                  f'{VTAIL_HEIGHT*1000:.0f}mm', horizontal=False, fontsize=7)

    # CG location
    cg_x = ROOT_CHORD * 0.25
    ax_side.plot(cg_x, 0, 'ro', markersize=8)
    ax_side.annotate('CG', xy=(cg_x, 0), xytext=(cg_x+0.05, 0.05),
                     arrowprops=dict(arrowstyle='->', color='red'), fontsize=8, color='red')

    # ==================== SPECIFICATIONS ====================
    ax_specs = fig.add_subplot(gs[1, 1])
    ax_specs.set_title('Specifications', fontsize=12, fontweight='bold')
    ax_specs.axis('off')

    specs_text = """
    AIRCRAFT SPECIFICATIONS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    GENERAL
    Total Weight:      1.96 kg (4.3 lb)
    Wingspan:          1,700 mm (67 in)
    Wing Area:         0.241 m² (374 in²)
    Aspect Ratio:      12.0
    Wing Loading:      80 N/m² (1.67 lb/ft²)

    WING
    Root Chord:        167 mm
    Tip Chord:         117 mm
    Taper Ratio:       0.70
    Dihedral:          3°
    Airfoil:           Custom (NeuralFoil opt.)
    Main Spar:         16mm OD Carbon Tube

    FUSELAGE
    Length:            450 mm
    Width:             120 mm
    Height:            100 mm
    Tail Boom:         12mm Carbon Tube

    TAIL
    H-Tail Span:       387 mm
    H-Tail Area:       0.038 m²
    V-Tail Height:     235 mm
    V-Tail Area:       0.037 m²

    PERFORMANCE
    Cruise Speed:      25.7 m/s (50 kt)
    Stall Speed:       9.7 m/s (19 kt)
    L/D (cruise):      21.5
    Cruise Power:      66 W
    Flight Time:       81 min
    Range:             100 km (round trip)

    PROPULSION
    Motor:             150-200W BLDC
    Propeller:         11x7 inch
    Battery:           4S 3300mAh LiPo
    """

    ax_specs.text(0.05, 0.95, specs_text, transform=ax_specs.transAxes,
                  fontsize=8, fontfamily='monospace', verticalalignment='top')

    plt.tight_layout()
    plt.savefig('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/three_view_drawing.png',
                dpi=200, bbox_inches='tight', facecolor='white')
    print("Saved: designs/three_view_drawing.png")

    plt.show()
    return fig


def draw_wing_detail():
    """Create detailed wing drawing with structure."""

    fig, axes = plt.subplots(1, 2, figsize=(14, 8))
    fig.suptitle('MegaDrone Phase 1 - Wing Structure Detail', fontsize=14, fontweight='bold')

    # ==================== WING PLANFORM ====================
    ax = axes[0]
    ax.set_title('Wing Planform (Right Half)', fontsize=11)
    ax.set_aspect('equal')

    # Scale for drawing (multiply by 1000 for mm)
    scale = 1000

    # Wing outline
    wing_x = np.array([0, ROOT_CHORD, TIP_CHORD + (ROOT_CHORD-TIP_CHORD)*0.25, (ROOT_CHORD-TIP_CHORD)*0.25, 0]) * scale
    wing_y = np.array([0, 0, SEMI_SPAN, SEMI_SPAN, 0]) * scale
    ax.fill(wing_x, wing_y, 'lightblue', edgecolor='black', linewidth=2, alpha=0.5)

    # Spar location (30% chord)
    spar_x_root = ROOT_CHORD * 0.3 * scale
    spar_x_tip = ((ROOT_CHORD-TIP_CHORD)*0.25 + TIP_CHORD * 0.3) * scale
    ax.plot([spar_x_root, spar_x_tip], [0, SEMI_SPAN * scale], 'r-', lw=3, label='Main Spar (16mm)')

    # Ribs
    n_ribs = 8
    for i in range(n_ribs + 1):
        y = i * SEMI_SPAN / n_ribs * scale
        # Interpolate chord at this station
        chord = ROOT_CHORD - (ROOT_CHORD - TIP_CHORD) * (i / n_ribs)
        x_le = (ROOT_CHORD - TIP_CHORD) * 0.25 * (i / n_ribs) * scale
        x_te = x_le + chord * scale
        ax.plot([x_le, x_te], [y, y], 'g-', lw=1.5)
        ax.text(x_te + 10, y, f'Rib {i+1}', fontsize=7, va='center')

    # Aileron
    aileron_start = SEMI_SPAN * 0.6 * scale
    aileron_end = SEMI_SPAN * 0.95 * scale
    chord_at_ail_start = ROOT_CHORD - (ROOT_CHORD - TIP_CHORD) * 0.6
    chord_at_ail_end = ROOT_CHORD - (ROOT_CHORD - TIP_CHORD) * 0.95
    x_le_start = (ROOT_CHORD - TIP_CHORD) * 0.25 * 0.6 * scale
    x_le_end = (ROOT_CHORD - TIP_CHORD) * 0.25 * 0.95 * scale

    ail_pts = [
        (x_le_start + chord_at_ail_start * 0.75 * scale, aileron_start),
        (x_le_start + chord_at_ail_start * scale, aileron_start),
        (x_le_end + chord_at_ail_end * scale, aileron_end),
        (x_le_end + chord_at_ail_end * 0.75 * scale, aileron_end),
    ]
    ax.fill([p[0] for p in ail_pts], [p[1] for p in ail_pts],
            'orange', alpha=0.5, edgecolor='black', linewidth=1)
    ax.text(x_le_start + chord_at_ail_start * 0.87 * scale, (aileron_start + aileron_end)/2,
            'Aileron\n25% chord', fontsize=7, ha='center', va='center')

    # Dimensions
    ax.annotate('', xy=(ROOT_CHORD * scale, -50), xytext=(0, -50),
                arrowprops=dict(arrowstyle='<->', color='black'))
    ax.text(ROOT_CHORD * scale / 2, -70, f'{ROOT_CHORD*1000:.0f}mm Root', ha='center', fontsize=8)

    ax.annotate('', xy=(spar_x_tip + 50, SEMI_SPAN * scale), xytext=(spar_x_tip + 50, 0),
                arrowprops=dict(arrowstyle='<->', color='black'))
    ax.text(spar_x_tip + 70, SEMI_SPAN * scale / 2, f'{SEMI_SPAN*1000:.0f}mm\nSemi-span',
            ha='left', va='center', fontsize=8)

    ax.set_xlabel('Chord Direction (mm)')
    ax.set_ylabel('Span Direction (mm)')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    # ==================== WING SECTION ====================
    ax = axes[1]
    ax.set_title('Wing Section at Root (not to scale)', fontsize=11)
    ax.set_aspect('equal')

    # Airfoil shape (simplified)
    x = np.linspace(0, 1, 100)
    # NACA 4-digit thickness distribution
    t = 0.12  # 12% thick
    yt = 5 * t * (0.2969*np.sqrt(x) - 0.1260*x - 0.3516*x**2 + 0.2843*x**3 - 0.1015*x**4)

    # Camber (2% at 40%)
    m = 0.02
    p = 0.4
    yc = np.where(x < p, m/p**2 * (2*p*x - x**2), m/(1-p)**2 * ((1-2*p) + 2*p*x - x**2))

    upper = yc + yt
    lower = yc - yt

    # Scale to chord
    chord_mm = ROOT_CHORD * 1000
    x_mm = x * chord_mm
    upper_mm = upper * chord_mm
    lower_mm = lower * chord_mm

    ax.fill_between(x_mm, lower_mm, upper_mm, color='lightblue', alpha=0.5)
    ax.plot(x_mm, upper_mm, 'b-', lw=2)
    ax.plot(x_mm, lower_mm, 'b-', lw=2)

    # Spar (at 30% chord)
    spar_x = 0.3 * chord_mm
    spar_y_upper = np.interp(spar_x, x_mm, upper_mm)
    spar_y_lower = np.interp(spar_x, x_mm, lower_mm)

    # Draw spar as circle (cross-section)
    spar_center = (spar_x, (spar_y_upper + spar_y_lower) / 2)
    spar_radius = SPAR_DIAMETER * 1000 / 2
    spar_circle = patches.Circle(spar_center, spar_radius, facecolor='red',
                                  edgecolor='darkred', linewidth=2, alpha=0.7)
    ax.add_patch(spar_circle)
    ax.text(spar_x, spar_center[1] - 15, f'Spar\n{SPAR_DIAMETER*1000:.0f}mm OD',
            ha='center', fontsize=8)

    # Leading edge foam
    le_x = x_mm[x_mm < 0.15 * chord_mm]
    le_upper = np.interp(le_x, x_mm, upper_mm)
    le_lower = np.interp(le_x, x_mm, lower_mm)
    ax.fill_between(le_x, le_lower, le_upper, color='yellow', alpha=0.5)
    ax.text(0.075 * chord_mm, 0, 'EPP\nFoam', ha='center', va='center', fontsize=7)

    # Film covering indication
    ax.plot(x_mm, upper_mm + 0.5, 'purple', lw=1, linestyle='--', label='Film Covering')
    ax.plot(x_mm, lower_mm - 0.5, 'purple', lw=1, linestyle='--')

    # Rib indication
    for rx in [0.15, 0.5, 0.85]:
        rib_x = rx * chord_mm
        rib_upper = np.interp(rib_x, x_mm, upper_mm)
        rib_lower = np.interp(rib_x, x_mm, lower_mm)
        ax.plot([rib_x, rib_x], [rib_lower, rib_upper], 'g-', lw=2)
    ax.text(0.5 * chord_mm, -15, 'Ribs (3D printed)', ha='center', fontsize=8, color='green')

    ax.set_xlabel('Chord (mm)')
    ax.set_ylabel('Thickness (mm)')
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-10, chord_mm + 20)
    ax.set_ylim(-25, 25)

    plt.tight_layout()
    plt.savefig('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/wing_detail.png',
                dpi=200, bbox_inches='tight', facecolor='white')
    print("Saved: designs/wing_detail.png")

    plt.show()
    return fig


def draw_assembly():
    """Create assembly/exploded view."""

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_title('MegaDrone Phase 1 - Component Layout', fontsize=14, fontweight='bold')
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw aircraft outline (side view)
    # Fuselage
    fuse_x = -0.1
    fuse_y = 0
    fuse_rect = patches.FancyBboxPatch((fuse_x, fuse_y - FUSE_HEIGHT/2), FUSE_LENGTH, FUSE_HEIGHT,
                                        boxstyle="round,pad=0.02", facecolor='lightgray',
                                        edgecolor='black', linewidth=2)
    ax.add_patch(fuse_rect)

    # Wing attachment point
    ax.plot([ROOT_CHORD*0.25, ROOT_CHORD*0.25], [-0.05, 0.05], 'k-', lw=3)
    ax.annotate('Wing Attach', xy=(ROOT_CHORD*0.25, 0.05), xytext=(ROOT_CHORD*0.25, 0.15),
                arrowprops=dict(arrowstyle='->', color='blue'), fontsize=9, color='blue', ha='center')

    # Tail boom
    ax.add_patch(patches.Rectangle((FUSE_LENGTH - 0.05, -0.006), TAIL_ARM + 0.05, 0.012,
                                    facecolor='gray', edgecolor='black', linewidth=1))

    # Component callouts with boxes
    components = [
        ((-0.08, 0), 'Motor\n150-200W', 'left'),
        ((0.05, -0.04), 'Battery\n4S 3300mAh', 'center'),
        ((0.20, 0.03), 'Flight Controller\n+ GPS', 'center'),
        ((0.32, -0.04), 'Camera\nPayload', 'center'),
        ((FUSE_LENGTH + TAIL_ARM * 0.5, 0.08), 'Tail Boom\n12mm Carbon', 'center'),
        ((FUSE_LENGTH + TAIL_ARM, 0.15), 'H-Tail', 'center'),
        ((FUSE_LENGTH + TAIL_ARM, -0.08), 'V-Tail', 'center'),
    ]

    for pos, label, ha in components:
        ax.annotate(label, xy=pos, fontsize=9, ha=ha, va='center',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Weight distribution bar
    bar_y = -0.25
    bar_height = 0.03
    weights = [
        ('Motor\n53g', 0.053/1.96, 'red'),
        ('Battery\n651g', 0.651/1.96, 'green'),
        ('Avionics\n150g', 0.150/1.96, 'blue'),
        ('Payload\n500g', 0.500/1.96, 'orange'),
        ('Structure\n606g', 0.606/1.96, 'gray'),
    ]

    ax.text(-0.15, bar_y, 'Weight\nDistribution:', fontsize=9, ha='right', va='center')

    x_start = -0.1
    total_width = 0.8
    for label, frac, color in weights:
        width = frac * total_width
        ax.add_patch(patches.Rectangle((x_start, bar_y - bar_height/2), width, bar_height,
                                        facecolor=color, edgecolor='black', alpha=0.7))
        if width > 0.05:
            ax.text(x_start + width/2, bar_y, label, fontsize=7, ha='center', va='center')
        x_start += width

    ax.set_xlim(-0.25, 1.1)
    ax.set_ylim(-0.4, 0.3)

    # Add title block
    title_text = """
    ┌─────────────────────────────────────────┐
    │  MegaDrone Phase 1 UAV                  │
    │  Component Layout                        │
    │  MTOW: 1.96 kg  |  Wingspan: 1.70m      │
    │  Date: January 2026                      │
    └─────────────────────────────────────────┘
    """
    ax.text(0.75, -0.35, title_text, fontsize=8, fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='black'))

    plt.tight_layout()
    plt.savefig('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/component_layout.png',
                dpi=200, bbox_inches='tight', facecolor='white')
    print("Saved: designs/component_layout.png")

    plt.show()
    return fig


def main():
    """Generate all technical drawings."""

    print("=" * 60)
    print("Generating Technical Drawings")
    print("=" * 60)

    # Three-view drawing
    print("\n1. Creating three-view drawing...")
    draw_three_view()

    # Wing detail
    print("\n2. Creating wing detail drawing...")
    draw_wing_detail()

    # Component layout
    print("\n3. Creating component layout...")
    draw_assembly()

    print("\n" + "=" * 60)
    print("All drawings generated successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
