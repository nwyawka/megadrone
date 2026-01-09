#!/usr/bin/env python3
"""
Bill of Materials Generator for MegaDrone Phase 1
Generates comprehensive parts list with pricing

Author: MegaDrone Project
Date: January 8, 2026
"""

import json
from datetime import datetime

# =============================================================================
# BILL OF MATERIALS
# =============================================================================

BOM = {
    "project": "MegaDrone Phase 1",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "version": "1.0",
    "notes": "Prices are estimates based on typical online suppliers (HobbyKing, Amazon, etc.). Payload not included.",

    "categories": {
        # =====================================================================
        # AIRFRAME STRUCTURE
        # =====================================================================
        "airframe": {
            "name": "Airframe Structure",
            "items": [
                {
                    "part_number": "AF-001",
                    "description": "Carbon Fiber Tube - Wing Spar",
                    "specification": "16mm OD x 14mm ID x 1000mm, pultruded",
                    "quantity": 2,
                    "unit": "pc",
                    "unit_price": 18.00,
                    "supplier": "Rockwest Composites / Amazon",
                    "notes": "Cut to 850mm each for wing panels"
                },
                {
                    "part_number": "AF-002",
                    "description": "Carbon Fiber Tube - Tail Boom",
                    "specification": "12mm OD x 10mm ID x 600mm, pultruded",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 12.00,
                    "supplier": "Rockwest Composites / Amazon",
                    "notes": "Connects fuselage to tail"
                },
                {
                    "part_number": "AF-003",
                    "description": "Balsa Sheet - Ribs",
                    "specification": "3mm x 100mm x 1000mm",
                    "quantity": 4,
                    "unit": "sheet",
                    "unit_price": 4.50,
                    "supplier": "Balsa Central / Amazon",
                    "notes": "For 12 wing ribs and tail ribs"
                },
                {
                    "part_number": "AF-004",
                    "description": "Balsa Sheet - Trailing Edge",
                    "specification": "2mm x 50mm x 1000mm",
                    "quantity": 2,
                    "unit": "sheet",
                    "unit_price": 3.50,
                    "supplier": "Balsa Central / Amazon",
                    "notes": "Wing and tail trailing edges"
                },
                {
                    "part_number": "AF-005",
                    "description": "EPP Foam Block - Leading Edge",
                    "specification": "25mm x 50mm x 1000mm, 30 g/L",
                    "quantity": 2,
                    "unit": "pc",
                    "unit_price": 8.00,
                    "supplier": "RC Foam / Amazon",
                    "notes": "D-box leading edge"
                },
                {
                    "part_number": "AF-006",
                    "description": "Fiberglass Cloth",
                    "specification": "50g/m², 1m x 1m",
                    "quantity": 2,
                    "unit": "m²",
                    "unit_price": 6.00,
                    "supplier": "Amazon / Fibreglast",
                    "notes": "Wing skin and reinforcement"
                },
                {
                    "part_number": "AF-007",
                    "description": "Epoxy Resin System",
                    "specification": "West System 105/206, 600g kit",
                    "quantity": 1,
                    "unit": "kit",
                    "unit_price": 45.00,
                    "supplier": "Amazon / West Marine",
                    "notes": "Laminating and bonding"
                },
                {
                    "part_number": "AF-008",
                    "description": "Heat Shrink Film - Covering",
                    "specification": "Oracover / UltraCote, 2m roll",
                    "quantity": 2,
                    "unit": "roll",
                    "unit_price": 25.00,
                    "supplier": "HobbyKing / Amazon",
                    "notes": "Wing and tail covering"
                },
                {
                    "part_number": "AF-009",
                    "description": "Plywood Sheet - Fuselage/Motor Mount",
                    "specification": "3mm birch ply, 300x300mm",
                    "quantity": 2,
                    "unit": "sheet",
                    "unit_price": 5.00,
                    "supplier": "Hobby Lobby / Amazon",
                    "notes": "Motor mount and fuselage bulkheads"
                },
                {
                    "part_number": "AF-010",
                    "description": "Carbon Fiber Sheet",
                    "specification": "1mm x 200mm x 300mm, 3K weave",
                    "quantity": 1,
                    "unit": "sheet",
                    "unit_price": 22.00,
                    "supplier": "Amazon / Rockwest",
                    "notes": "Fuselage sides and doublers"
                },
            ]
        },

        # =====================================================================
        # PROPULSION SYSTEM
        # =====================================================================
        "propulsion": {
            "name": "Propulsion System",
            "items": [
                {
                    "part_number": "PR-001",
                    "description": "Brushless Motor",
                    "specification": "SunnySky X2212-980KV, 180W, 58g",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 28.00,
                    "supplier": "HobbyKing / Amazon",
                    "notes": "Alternative: T-Motor AT2312-900KV"
                },
                {
                    "part_number": "PR-002",
                    "description": "Electronic Speed Controller (ESC)",
                    "specification": "30A BLHeli_S, 5V/3A BEC",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 18.00,
                    "supplier": "HobbyKing / Amazon",
                    "notes": "With BEC for servos"
                },
                {
                    "part_number": "PR-003",
                    "description": "Propeller - Cruise",
                    "specification": "APC 11x7E Thin Electric",
                    "quantity": 3,
                    "unit": "pc",
                    "unit_price": 6.00,
                    "supplier": "HobbyKing / Amazon",
                    "notes": "Include spares"
                },
                {
                    "part_number": "PR-004",
                    "description": "Propeller Adapter",
                    "specification": "3mm to 6mm collet adapter",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 4.00,
                    "supplier": "HobbyKing / Amazon",
                    "notes": "Match motor shaft"
                },
                {
                    "part_number": "PR-005",
                    "description": "Spinner",
                    "specification": "38mm plastic spinner",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 5.00,
                    "supplier": "HobbyKing / Amazon",
                    "notes": "Aerodynamic nose cone"
                },
            ]
        },

        # =====================================================================
        # BATTERY & POWER
        # =====================================================================
        "power": {
            "name": "Battery & Power",
            "items": [
                {
                    "part_number": "PW-001",
                    "description": "LiPo Battery - Primary",
                    "specification": "4S 3300mAh 30C, XT60",
                    "quantity": 2,
                    "unit": "pc",
                    "unit_price": 45.00,
                    "supplier": "HobbyKing / Amazon",
                    "notes": "117Wh total, one spare"
                },
                {
                    "part_number": "PW-002",
                    "description": "Battery Voltage Monitor",
                    "specification": "1-8S LiPo alarm buzzer",
                    "quantity": 2,
                    "unit": "pc",
                    "unit_price": 3.00,
                    "supplier": "Amazon",
                    "notes": "Low voltage warning"
                },
                {
                    "part_number": "PW-003",
                    "description": "Power Distribution Board",
                    "specification": "Mini PDB with XT60 input",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 8.00,
                    "supplier": "Amazon",
                    "notes": "Clean power distribution"
                },
                {
                    "part_number": "PW-004",
                    "description": "XT60 Connectors",
                    "specification": "Male/Female pair, 5 sets",
                    "quantity": 1,
                    "unit": "pack",
                    "unit_price": 6.00,
                    "supplier": "Amazon",
                    "notes": "Battery connections"
                },
                {
                    "part_number": "PW-005",
                    "description": "Battery Charger",
                    "specification": "ISDT D2 dual charger, 200W",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 75.00,
                    "supplier": "Amazon / HobbyKing",
                    "notes": "Balance charger for 4S"
                },
            ]
        },

        # =====================================================================
        # AVIONICS & CONTROL
        # =====================================================================
        "avionics": {
            "name": "Avionics & Control",
            "items": [
                {
                    "part_number": "AV-001",
                    "description": "Flight Controller",
                    "specification": "Matek F405-Wing, OSD, GPS",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 55.00,
                    "supplier": "Amazon / GetFPV",
                    "notes": "ArduPilot compatible"
                },
                {
                    "part_number": "AV-002",
                    "description": "GPS Module",
                    "specification": "BN-880 GPS/Compass, 10Hz",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 22.00,
                    "supplier": "Amazon",
                    "notes": "M8N chipset with compass"
                },
                {
                    "part_number": "AV-003",
                    "description": "RC Receiver",
                    "specification": "FrSky R-XSR 16ch SBUS",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 28.00,
                    "supplier": "Amazon / GetFPV",
                    "notes": "Requires FrSky transmitter"
                },
                {
                    "part_number": "AV-004",
                    "description": "Telemetry Radio",
                    "specification": "Holybro 433MHz 500mW, pair",
                    "quantity": 1,
                    "unit": "set",
                    "unit_price": 45.00,
                    "supplier": "Amazon / GetFPV",
                    "notes": "For mission planner link"
                },
                {
                    "part_number": "AV-005",
                    "description": "Airspeed Sensor",
                    "specification": "MS4525DO pitot tube kit",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 35.00,
                    "supplier": "Amazon / mRobotics",
                    "notes": "For accurate airspeed"
                },
                {
                    "part_number": "AV-006",
                    "description": "Servo - Aileron",
                    "specification": "Savox SH-0254, 3.9g digital",
                    "quantity": 2,
                    "unit": "pc",
                    "unit_price": 12.00,
                    "supplier": "Amazon / HobbyKing",
                    "notes": "High-speed micro servo"
                },
                {
                    "part_number": "AV-007",
                    "description": "Servo - Elevator",
                    "specification": "Savox SH-0254, 3.9g digital",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 12.00,
                    "supplier": "Amazon / HobbyKing",
                    "notes": "Same as aileron for commonality"
                },
                {
                    "part_number": "AV-008",
                    "description": "Servo - Rudder",
                    "specification": "Savox SH-0254, 3.9g digital",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 12.00,
                    "supplier": "Amazon / HobbyKing",
                    "notes": "Same as aileron for commonality"
                },
            ]
        },

        # =====================================================================
        # HARDWARE & FASTENERS
        # =====================================================================
        "hardware": {
            "name": "Hardware & Fasteners",
            "items": [
                {
                    "part_number": "HW-001",
                    "description": "M3 Screw Assortment",
                    "specification": "Socket head cap, 6-20mm lengths",
                    "quantity": 1,
                    "unit": "kit",
                    "unit_price": 12.00,
                    "supplier": "Amazon",
                    "notes": "Stainless steel"
                },
                {
                    "part_number": "HW-002",
                    "description": "M3 Nylon Lock Nuts",
                    "specification": "Nyloc nuts, 50 pack",
                    "quantity": 1,
                    "unit": "pack",
                    "unit_price": 5.00,
                    "supplier": "Amazon",
                    "notes": "Vibration resistant"
                },
                {
                    "part_number": "HW-003",
                    "description": "Control Horns",
                    "specification": "Nylon micro horns, 10 pack",
                    "quantity": 1,
                    "unit": "pack",
                    "unit_price": 4.00,
                    "supplier": "HobbyKing",
                    "notes": "For control surfaces"
                },
                {
                    "part_number": "HW-004",
                    "description": "Pushrod Set",
                    "specification": "1.5mm carbon rod + clevis",
                    "quantity": 1,
                    "unit": "set",
                    "unit_price": 8.00,
                    "supplier": "HobbyKing",
                    "notes": "Control linkages"
                },
                {
                    "part_number": "HW-005",
                    "description": "Cable Ties",
                    "specification": "100mm assorted, 100 pack",
                    "quantity": 1,
                    "unit": "pack",
                    "unit_price": 4.00,
                    "supplier": "Amazon",
                    "notes": "Wire management"
                },
                {
                    "part_number": "HW-006",
                    "description": "Heat Shrink Tubing",
                    "specification": "Assorted sizes, kit",
                    "quantity": 1,
                    "unit": "kit",
                    "unit_price": 8.00,
                    "supplier": "Amazon",
                    "notes": "Wire insulation"
                },
                {
                    "part_number": "HW-007",
                    "description": "Servo Extension Cables",
                    "specification": "150mm, 300mm lengths, 10 pack",
                    "quantity": 1,
                    "unit": "pack",
                    "unit_price": 8.00,
                    "supplier": "Amazon",
                    "notes": "JR/Futaba compatible"
                },
                {
                    "part_number": "HW-008",
                    "description": "Velcro Straps",
                    "specification": "Battery straps, 200mm, 5 pack",
                    "quantity": 1,
                    "unit": "pack",
                    "unit_price": 5.00,
                    "supplier": "Amazon",
                    "notes": "Battery mounting"
                },
            ]
        },

        # =====================================================================
        # GROUND SUPPORT
        # =====================================================================
        "ground_support": {
            "name": "Ground Support Equipment",
            "items": [
                {
                    "part_number": "GS-001",
                    "description": "RC Transmitter",
                    "specification": "FrSky Taranis X9D Plus SE",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 250.00,
                    "supplier": "Amazon / GetFPV",
                    "notes": "If not already owned"
                },
                {
                    "part_number": "GS-002",
                    "description": "Ground Station Laptop Mount",
                    "specification": "Tripod tablet holder",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 25.00,
                    "supplier": "Amazon",
                    "notes": "For Mission Planner"
                },
                {
                    "part_number": "GS-003",
                    "description": "Field Toolkit",
                    "specification": "Hex drivers, screwdrivers",
                    "quantity": 1,
                    "unit": "kit",
                    "unit_price": 25.00,
                    "supplier": "Amazon",
                    "notes": "Field maintenance"
                },
                {
                    "part_number": "GS-004",
                    "description": "Transport Case",
                    "specification": "Foam-lined hard case, 800x400mm",
                    "quantity": 1,
                    "unit": "pc",
                    "unit_price": 65.00,
                    "supplier": "Amazon / Pelican",
                    "notes": "Wing detaches for transport"
                },
            ]
        },
    }
}


def calculate_totals(bom):
    """Calculate category and grand totals."""

    category_totals = {}
    grand_total = 0

    for cat_key, category in bom["categories"].items():
        cat_total = 0
        for item in category["items"]:
            item["extended_price"] = item["quantity"] * item["unit_price"]
            cat_total += item["extended_price"]
        category_totals[cat_key] = cat_total
        grand_total += cat_total

    return category_totals, grand_total


def print_bom(bom):
    """Print formatted BOM to console."""

    category_totals, grand_total = calculate_totals(bom)

    print("=" * 100)
    print(f"BILL OF MATERIALS - {bom['project']}")
    print(f"Date: {bom['date']} | Version: {bom['version']}")
    print("=" * 100)
    print(f"\nNote: {bom['notes']}\n")

    for cat_key, category in bom["categories"].items():
        print("\n" + "-" * 100)
        print(f"{category['name'].upper()}")
        print("-" * 100)
        print(f"{'Part #':<10} {'Description':<35} {'Qty':>5} {'Unit':>6} {'Unit $':>8} {'Ext $':>10}")
        print("-" * 100)

        for item in category["items"]:
            print(f"{item['part_number']:<10} {item['description'][:35]:<35} "
                  f"{item['quantity']:>5} {item['unit']:>6} "
                  f"${item['unit_price']:>7.2f} ${item['extended_price']:>9.2f}")

        print(f"{'':>66} Subtotal: ${category_totals[cat_key]:>9.2f}")

    print("\n" + "=" * 100)
    print(f"{'GRAND TOTAL (excluding payload)':>76}: ${grand_total:>9.2f}")
    print("=" * 100)

    # Summary by category
    print("\n\nCOST SUMMARY BY CATEGORY")
    print("-" * 50)
    for cat_key, category in bom["categories"].items():
        pct = (category_totals[cat_key] / grand_total) * 100
        print(f"  {category['name']:<30} ${category_totals[cat_key]:>8.2f}  ({pct:>5.1f}%)")
    print("-" * 50)
    print(f"  {'TOTAL':<30} ${grand_total:>8.2f}  (100.0%)")

    return category_totals, grand_total


def export_to_csv(bom, filename):
    """Export BOM to CSV file."""

    calculate_totals(bom)

    with open(filename, 'w') as f:
        # Header
        f.write("Part Number,Description,Specification,Quantity,Unit,Unit Price,Extended Price,Supplier,Notes\n")

        for cat_key, category in bom["categories"].items():
            # Category header
            f.write(f"\n{category['name']},,,,,,,\n")

            for item in category["items"]:
                f.write(f"{item['part_number']},"
                        f"\"{item['description']}\","
                        f"\"{item['specification']}\","
                        f"{item['quantity']},"
                        f"{item['unit']},"
                        f"{item['unit_price']:.2f},"
                        f"{item['extended_price']:.2f},"
                        f"\"{item['supplier']}\","
                        f"\"{item['notes']}\"\n")

    print(f"\nExported to: {filename}")


def export_to_json(bom, filename):
    """Export BOM to JSON file."""

    calculate_totals(bom)

    with open(filename, 'w') as f:
        json.dump(bom, f, indent=2)

    print(f"Exported to: {filename}")


def generate_bom_markdown(bom):
    """Generate markdown format for PDF report."""

    category_totals, grand_total = calculate_totals(bom)

    md = []
    md.append(f"# Bill of Materials - {bom['project']}\n")
    md.append(f"**Date:** {bom['date']} | **Version:** {bom['version']}\n")
    md.append(f"\n> {bom['notes']}\n")

    for cat_key, category in bom["categories"].items():
        md.append(f"\n## {category['name']}\n")
        md.append("| Part # | Description | Spec | Qty | Unit $ | Ext $ |")
        md.append("|--------|-------------|------|-----|--------|-------|")

        for item in category["items"]:
            md.append(f"| {item['part_number']} | {item['description']} | "
                     f"{item['specification'][:30]}... | {item['quantity']} | "
                     f"${item['unit_price']:.2f} | ${item['extended_price']:.2f} |")

        md.append(f"| | | | **Subtotal:** | | **${category_totals[cat_key]:.2f}** |")

    md.append(f"\n## Cost Summary\n")
    md.append("| Category | Cost | Percentage |")
    md.append("|----------|------|------------|")
    for cat_key, category in bom["categories"].items():
        pct = (category_totals[cat_key] / grand_total) * 100
        md.append(f"| {category['name']} | ${category_totals[cat_key]:.2f} | {pct:.1f}% |")
    md.append(f"| **TOTAL** | **${grand_total:.2f}** | **100%** |")

    return "\n".join(md)


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Generate and export BOM."""

    print("\n" + "=" * 100)
    print("MegaDrone Phase 1 - Bill of Materials Generator")
    print("=" * 100)

    # Print formatted BOM
    category_totals, grand_total = print_bom(BOM)

    # Export to CSV
    export_to_csv(BOM, '/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/bill_of_materials.csv')

    # Export to JSON
    export_to_json(BOM, '/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/bill_of_materials.json')

    # Generate markdown
    md = generate_bom_markdown(BOM)
    with open('/Users/matthewoneil/Desktop/Datawerkes/MegaDrone/designs/bill_of_materials.md', 'w') as f:
        f.write(md)
    print("Exported to: designs/bill_of_materials.md")

    # Summary statistics
    print("\n" + "=" * 100)
    print("BOM STATISTICS")
    print("=" * 100)
    total_items = sum(len(cat["items"]) for cat in BOM["categories"].values())
    print(f"  Total unique parts:     {total_items}")
    print(f"  Categories:             {len(BOM['categories'])}")
    print(f"  Total cost:             ${grand_total:.2f}")
    print(f"  Avg cost per category:  ${grand_total/len(BOM['categories']):.2f}")

    # Cost breakdown insights
    print("\n  COST INSIGHTS:")
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    print(f"  - Highest cost: {BOM['categories'][sorted_cats[0][0]]['name']} (${sorted_cats[0][1]:.2f})")
    print(f"  - Lowest cost:  {BOM['categories'][sorted_cats[-1][0]]['name']} (${sorted_cats[-1][1]:.2f})")

    # Note on ground support
    gs_total = category_totals.get('ground_support', 0)
    aircraft_only = grand_total - gs_total
    print(f"\n  Aircraft only (no GSE): ${aircraft_only:.2f}")
    print(f"  Ground Support Equipment: ${gs_total:.2f}")

    return BOM, grand_total


if __name__ == "__main__":
    bom, total = main()
