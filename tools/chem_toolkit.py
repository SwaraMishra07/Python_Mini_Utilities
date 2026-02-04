#!/usr/bin/env python3
"""
chem_toolkit.py - A comprehensive chemistry calculation toolkit
Zero dependencies - uses only Python standard library
"""

import re
import sys
import argparse
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


# ============================================================================
# PERIODIC TABLE DATA
# ============================================================================

PERIODIC_TABLE = {
    'H': {'number': 1, 'weight': 1.008, 'name': 'Hydrogen', 'group': 1, 'phase': 'gas'},
    'He': {'number': 2, 'weight': 4.003, 'name': 'Helium', 'group': 18, 'phase': 'gas'},
    'Li': {'number': 3, 'weight': 6.941, 'name': 'Lithium', 'group': 1, 'phase': 'solid'},
    'Be': {'number': 4, 'weight': 9.012, 'name': 'Beryllium', 'group': 2, 'phase': 'solid'},
    'B': {'number': 5, 'weight': 10.811, 'name': 'Boron', 'group': 13, 'phase': 'solid'},
    'C': {'number': 6, 'weight': 12.011, 'name': 'Carbon', 'group': 14, 'phase': 'solid'},
    'N': {'number': 7, 'weight': 14.007, 'name': 'Nitrogen', 'group': 15, 'phase': 'gas'},
    'O': {'number': 8, 'weight': 15.999, 'name': 'Oxygen', 'group': 16, 'phase': 'gas'},
    'F': {'number': 9, 'weight': 18.998, 'name': 'Fluorine', 'group': 17, 'phase': 'gas'},
    'Ne': {'number': 10, 'weight': 20.180, 'name': 'Neon', 'group': 18, 'phase': 'gas'},
    'Na': {'number': 11, 'weight': 22.990, 'name': 'Sodium', 'group': 1, 'phase': 'solid'},
    'Mg': {'number': 12, 'weight': 24.305, 'name': 'Magnesium', 'group': 2, 'phase': 'solid'},
    'Al': {'number': 13, 'weight': 26.982, 'name': 'Aluminum', 'group': 13, 'phase': 'solid'},
    'Si': {'number': 14, 'weight': 28.086, 'name': 'Silicon', 'group': 14, 'phase': 'solid'},
    'P': {'number': 15, 'weight': 30.974, 'name': 'Phosphorus', 'group': 15, 'phase': 'solid'},
    'S': {'number': 16, 'weight': 32.065, 'name': 'Sulfur', 'group': 16, 'phase': 'solid'},
    'Cl': {'number': 17, 'weight': 35.453, 'name': 'Chlorine', 'group': 17, 'phase': 'gas'},
    'Ar': {'number': 18, 'weight': 39.948, 'name': 'Argon', 'group': 18, 'phase': 'gas'},
    'K': {'number': 19, 'weight': 39.098, 'name': 'Potassium', 'group': 1, 'phase': 'solid'},
    'Ca': {'number': 20, 'weight': 40.078, 'name': 'Calcium', 'group': 2, 'phase': 'solid'},
    'Sc': {'number': 21, 'weight': 44.956, 'name': 'Scandium', 'group': 3, 'phase': 'solid'},
    'Ti': {'number': 22, 'weight': 47.867, 'name': 'Titanium', 'group': 4, 'phase': 'solid'},
    'V': {'number': 23, 'weight': 50.942, 'name': 'Vanadium', 'group': 5, 'phase': 'solid'},
    'Cr': {'number': 24, 'weight': 51.996, 'name': 'Chromium', 'group': 6, 'phase': 'solid'},
    'Mn': {'number': 25, 'weight': 54.938, 'name': 'Manganese', 'group': 7, 'phase': 'solid'},
    'Fe': {'number': 26, 'weight': 55.845, 'name': 'Iron', 'group': 8, 'phase': 'solid'},
    'Co': {'number': 27, 'weight': 58.933, 'name': 'Cobalt', 'group': 9, 'phase': 'solid'},
    'Ni': {'number': 28, 'weight': 58.693, 'name': 'Nickel', 'group': 10, 'phase': 'solid'},
    'Cu': {'number': 29, 'weight': 63.546, 'name': 'Copper', 'group': 11, 'phase': 'solid'},
    'Zn': {'number': 30, 'weight': 65.380, 'name': 'Zinc', 'group': 12, 'phase': 'solid'},
    'Ga': {'number': 31, 'weight': 69.723, 'name': 'Gallium', 'group': 13, 'phase': 'solid'},
    'Ge': {'number': 32, 'weight': 72.640, 'name': 'Germanium', 'group': 14, 'phase': 'solid'},
    'As': {'number': 33, 'weight': 74.922, 'name': 'Arsenic', 'group': 15, 'phase': 'solid'},
    'Se': {'number': 34, 'weight': 78.960, 'name': 'Selenium', 'group': 16, 'phase': 'solid'},
    'Br': {'number': 35, 'weight': 79.904, 'name': 'Bromine', 'group': 17, 'phase': 'liquid'},
    'Kr': {'number': 36, 'weight': 83.798, 'name': 'Krypton', 'group': 18, 'phase': 'gas'},
    'Rb': {'number': 37, 'weight': 85.468, 'name': 'Rubidium', 'group': 1, 'phase': 'solid'},
    'Sr': {'number': 38, 'weight': 87.620, 'name': 'Strontium', 'group': 2, 'phase': 'solid'},
    'Y': {'number': 39, 'weight': 88.906, 'name': 'Yttrium', 'group': 3, 'phase': 'solid'},
    'Zr': {'number': 40, 'weight': 91.224, 'name': 'Zirconium', 'group': 4, 'phase': 'solid'},
    'Nb': {'number': 41, 'weight': 92.906, 'name': 'Niobium', 'group': 5, 'phase': 'solid'},
    'Mo': {'number': 42, 'weight': 95.960, 'name': 'Molybdenum', 'group': 6, 'phase': 'solid'},
    'Tc': {'number': 43, 'weight': 98.000, 'name': 'Technetium', 'group': 7, 'phase': 'solid'},
    'Ru': {'number': 44, 'weight': 101.070, 'name': 'Ruthenium', 'group': 8, 'phase': 'solid'},
    'Rh': {'number': 45, 'weight': 102.906, 'name': 'Rhodium', 'group': 9, 'phase': 'solid'},
    'Pd': {'number': 46, 'weight': 106.420, 'name': 'Palladium', 'group': 10, 'phase': 'solid'},
    'Ag': {'number': 47, 'weight': 107.868, 'name': 'Silver', 'group': 11, 'phase': 'solid'},
    'Cd': {'number': 48, 'weight': 112.411, 'name': 'Cadmium', 'group': 12, 'phase': 'solid'},
    'In': {'number': 49, 'weight': 114.818, 'name': 'Indium', 'group': 13, 'phase': 'solid'},
    'Sn': {'number': 50, 'weight': 118.710, 'name': 'Tin', 'group': 14, 'phase': 'solid'},
    'Sb': {'number': 51, 'weight': 121.760, 'name': 'Antimony', 'group': 15, 'phase': 'solid'},
    'Te': {'number': 52, 'weight': 127.600, 'name': 'Tellurium', 'group': 16, 'phase': 'solid'},
    'I': {'number': 53, 'weight': 126.904, 'name': 'Iodine', 'group': 17, 'phase': 'solid'},
    'Xe': {'number': 54, 'weight': 131.293, 'name': 'Xenon', 'group': 18, 'phase': 'gas'},
    'Cs': {'number': 55, 'weight': 132.905, 'name': 'Cesium', 'group': 1, 'phase': 'solid'},
    'Ba': {'number': 56, 'weight': 137.327, 'name': 'Barium', 'group': 2, 'phase': 'solid'},
    'La': {'number': 57, 'weight': 138.905, 'name': 'Lanthanum', 'group': 3, 'phase': 'solid'},
    'Ce': {'number': 58, 'weight': 140.116, 'name': 'Cerium', 'group': 3, 'phase': 'solid'},
    'Pr': {'number': 59, 'weight': 140.908, 'name': 'Praseodymium', 'group': 3, 'phase': 'solid'},
    'Nd': {'number': 60, 'weight': 144.242, 'name': 'Neodymium', 'group': 3, 'phase': 'solid'},
    'Pm': {'number': 61, 'weight': 145.000, 'name': 'Promethium', 'group': 3, 'phase': 'solid'},
    'Sm': {'number': 62, 'weight': 150.360, 'name': 'Samarium', 'group': 3, 'phase': 'solid'},
    'Eu': {'number': 63, 'weight': 151.964, 'name': 'Europium', 'group': 3, 'phase': 'solid'},
    'Gd': {'number': 64, 'weight': 157.250, 'name': 'Gadolinium', 'group': 3, 'phase': 'solid'},
    'Tb': {'number': 65, 'weight': 158.925, 'name': 'Terbium', 'group': 3, 'phase': 'solid'},
    'Dy': {'number': 66, 'weight': 162.500, 'name': 'Dysprosium', 'group': 3, 'phase': 'solid'},
    'Ho': {'number': 67, 'weight': 164.930, 'name': 'Holmium', 'group': 3, 'phase': 'solid'},
    'Er': {'number': 68, 'weight': 167.259, 'name': 'Erbium', 'group': 3, 'phase': 'solid'},
    'Tm': {'number': 69, 'weight': 168.934, 'name': 'Thulium', 'group': 3, 'phase': 'solid'},
    'Yb': {'number': 70, 'weight': 173.054, 'name': 'Ytterbium', 'group': 3, 'phase': 'solid'},
    'Lu': {'number': 71, 'weight': 174.967, 'name': 'Lutetium', 'group': 3, 'phase': 'solid'},
    'Hf': {'number': 72, 'weight': 178.490, 'name': 'Hafnium', 'group': 4, 'phase': 'solid'},
    'Ta': {'number': 73, 'weight': 180.948, 'name': 'Tantalum', 'group': 5, 'phase': 'solid'},
    'W': {'number': 74, 'weight': 183.840, 'name': 'Tungsten', 'group': 6, 'phase': 'solid'},
    'Re': {'number': 75, 'weight': 186.207, 'name': 'Rhenium', 'group': 7, 'phase': 'solid'},
    'Os': {'number': 76, 'weight': 190.230, 'name': 'Osmium', 'group': 8, 'phase': 'solid'},
    'Ir': {'number': 77, 'weight': 192.217, 'name': 'Iridium', 'group': 9, 'phase': 'solid'},
    'Pt': {'number': 78, 'weight': 195.084, 'name': 'Platinum', 'group': 10, 'phase': 'solid'},
    'Au': {'number': 79, 'weight': 196.967, 'name': 'Gold', 'group': 11, 'phase': 'solid'},
    'Hg': {'number': 80, 'weight': 200.590, 'name': 'Mercury', 'group': 12, 'phase': 'liquid'},
    'Tl': {'number': 81, 'weight': 204.383, 'name': 'Thallium', 'group': 13, 'phase': 'solid'},
    'Pb': {'number': 82, 'weight': 207.200, 'name': 'Lead', 'group': 14, 'phase': 'solid'},
    'Bi': {'number': 83, 'weight': 208.980, 'name': 'Bismuth', 'group': 15, 'phase': 'solid'},
    'Po': {'number': 84, 'weight': 209.000, 'name': 'Polonium', 'group': 16, 'phase': 'solid'},
    'At': {'number': 85, 'weight': 210.000, 'name': 'Astatine', 'group': 17, 'phase': 'solid'},
    'Rn': {'number': 86, 'weight': 222.000, 'name': 'Radon', 'group': 18, 'phase': 'gas'},
    'Fr': {'number': 87, 'weight': 223.000, 'name': 'Francium', 'group': 1, 'phase': 'solid'},
    'Ra': {'number': 88, 'weight': 226.000, 'name': 'Radium', 'group': 2, 'phase': 'solid'},
    'Ac': {'number': 89, 'weight': 227.000, 'name': 'Actinium', 'group': 3, 'phase': 'solid'},
    'Th': {'number': 90, 'weight': 232.038, 'name': 'Thorium', 'group': 3, 'phase': 'solid'},
    'Pa': {'number': 91, 'weight': 231.036, 'name': 'Protactinium', 'group': 3, 'phase': 'solid'},
    'U': {'number': 92, 'weight': 238.029, 'name': 'Uranium', 'group': 3, 'phase': 'solid'},
    'Np': {'number': 93, 'weight': 237.000, 'name': 'Neptunium', 'group': 3, 'phase': 'solid'},
    'Pu': {'number': 94, 'weight': 244.000, 'name': 'Plutonium', 'group': 3, 'phase': 'solid'},
    'Am': {'number': 95, 'weight': 243.000, 'name': 'Americium', 'group': 3, 'phase': 'solid'},
    'Cm': {'number': 96, 'weight': 247.000, 'name': 'Curium', 'group': 3, 'phase': 'solid'},
    'Bk': {'number': 97, 'weight': 247.000, 'name': 'Berkelium', 'group': 3, 'phase': 'solid'},
    'Cf': {'number': 98, 'weight': 251.000, 'name': 'Californium', 'group': 3, 'phase': 'solid'},
    'Es': {'number': 99, 'weight': 252.000, 'name': 'Einsteinium', 'group': 3, 'phase': 'solid'},
    'Fm': {'number': 100, 'weight': 257.000, 'name': 'Fermium', 'group': 3, 'phase': 'solid'},
    'Md': {'number': 101, 'weight': 258.000, 'name': 'Mendelevium', 'group': 3, 'phase': 'solid'},
    'No': {'number': 102, 'weight': 259.000, 'name': 'Nobelium', 'group': 3, 'phase': 'solid'},
    'Lr': {'number': 103, 'weight': 262.000, 'name': 'Lawrencium', 'group': 3, 'phase': 'solid'},
    'Rf': {'number': 104, 'weight': 267.000, 'name': 'Rutherfordium', 'group': 4, 'phase': 'solid'},
    'Db': {'number': 105, 'weight': 268.000, 'name': 'Dubnium', 'group': 5, 'phase': 'solid'},
    'Sg': {'number': 106, 'weight': 271.000, 'name': 'Seaborgium', 'group': 6, 'phase': 'solid'},
    'Bh': {'number': 107, 'weight': 272.000, 'name': 'Bohrium', 'group': 7, 'phase': 'solid'},
    'Hs': {'number': 108, 'weight': 270.000, 'name': 'Hassium', 'group': 8, 'phase': 'solid'},
    'Mt': {'number': 109, 'weight': 276.000, 'name': 'Meitnerium', 'group': 9, 'phase': 'solid'},
    'Ds': {'number': 110, 'weight': 281.000, 'name': 'Darmstadtium', 'group': 10, 'phase': 'solid'},
    'Rg': {'number': 111, 'weight': 280.000, 'name': 'Roentgenium', 'group': 11, 'phase': 'solid'},
    'Cn': {'number': 112, 'weight': 285.000, 'name': 'Copernicium', 'group': 12, 'phase': 'solid'},
    'Nh': {'number': 113, 'weight': 284.000, 'name': 'Nihonium', 'group': 13, 'phase': 'solid'},
    'Fl': {'number': 114, 'weight': 289.000, 'name': 'Flerovium', 'group': 14, 'phase': 'solid'},
    'Mc': {'number': 115, 'weight': 288.000, 'name': 'Moscovium', 'group': 15, 'phase': 'solid'},
    'Lv': {'number': 116, 'weight': 293.000, 'name': 'Livermorium', 'group': 16, 'phase': 'solid'},
    'Ts': {'number': 117, 'weight': 294.000, 'name': 'Tennessine', 'group': 17, 'phase': 'solid'},
    'Og': {'number': 118, 'weight': 294.000, 'name': 'Oganesson', 'group': 18, 'phase': 'solid'},
}


# ============================================================================
# CONSTANTS
# ============================================================================

R_GAS_CONSTANT = {
    'L·atm/(mol·K)': 0.08206,
    'J/(mol·K)': 8.314,
    'L·kPa/(mol·K)': 8.314,
    'cal/(mol·K)': 1.987,
}

AVOGADRO = 6.022e23
STANDARD_TEMP_K = 273.15  # 0°C in Kelvin
STANDARD_PRESSURE_ATM = 1.0


# ============================================================================
# FORMULA PARSING
# ============================================================================

def parse_formula(formula: str) -> Dict[str, int]:
    """
    Parse a chemical formula and return element counts.
    Handles parentheses and brackets.
    
    Examples:
        Ca(OH)2 -> {'Ca': 1, 'O': 2, 'H': 2}
        Fe2(SO4)3 -> {'Fe': 2, 'S': 3, 'O': 12}
    """
    # Expand parentheses first
    while '(' in formula or '[' in formula:
        # Find innermost parentheses/brackets
        match = re.search(r'[\(\[]([^\(\)\[\]]+)[\)\]](\d*)', formula)
        if not match:
            break
        
        group = match.group(1)
        multiplier = int(match.group(2)) if match.group(2) else 1
        
        # Expand the group
        expanded = ''
        element_pattern = r'([A-Z][a-z]?)(\d*)'
        for elem_match in re.finditer(element_pattern, group):
            element = elem_match.group(1)
            count = int(elem_match.group(2)) if elem_match.group(2) else 1
            if count * multiplier > 1:
                expanded += f"{element}{count * multiplier}"
            else:
                expanded += element
        
        formula = formula[:match.start()] + expanded + formula[match.end():]
    
    # Now parse the expanded formula
    composition = defaultdict(int)
    pattern = r'([A-Z][a-z]?)(\d*)'
    
    for match in re.finditer(pattern, formula):
        element = match.group(1)
        count = int(match.group(2)) if match.group(2) else 1
        
        if element not in PERIODIC_TABLE:
            raise ValueError(f"Unknown element: {element}")
        
        composition[element] += count
    
    return dict(composition)


def calculate_molar_mass(formula: str) -> float:
    """Calculate the molar mass of a chemical formula."""
    composition = parse_formula(formula)
    molar_mass = sum(
        PERIODIC_TABLE[element]['weight'] * count
        for element, count in composition.items()
    )
    return molar_mass


# ============================================================================
# ELEMENT LOOKUP
# ============================================================================

def element_info(query: str) -> Optional[Dict]:
    """
    Look up an element by symbol, name, or atomic number.
    """
    query = query.strip()
    
    # Try as symbol
    if query in PERIODIC_TABLE:
        return {**PERIODIC_TABLE[query], 'symbol': query}
    
    # Try as number
    if query.isdigit():
        number = int(query)
        for symbol, data in PERIODIC_TABLE.items():
            if data['number'] == number:
                return {**data, 'symbol': symbol}
    
    # Try as name (case-insensitive)
    query_lower = query.lower()
    for symbol, data in PERIODIC_TABLE.items():
        if data['name'].lower() == query_lower:
            return {**data, 'symbol': symbol}
    
    return None


# ============================================================================
# IDEAL GAS LAW
# ============================================================================

def ideal_gas_law(P=None, V=None, n=None, T=None, R_unit='L·atm/(mol·K)'):
    """
    Solve ideal gas law: PV = nRT
    Provide 3 of 4 variables to solve for the 4th.
    
    P: Pressure (atm)
    V: Volume (L)
    n: Moles (mol)
    T: Temperature (K)
    """
    R = R_GAS_CONSTANT[R_unit]
    
    known_vars = sum(x is not None for x in [P, V, n, T])
    
    if known_vars != 3:
        raise ValueError("Provide exactly 3 variables to solve for the 4th")
    
    if P is None:
        return (n * R * T) / V
    elif V is None:
        return (n * R * T) / P
    elif n is None:
        return (P * V) / (R * T)
    elif T is None:
        return (P * V) / (n * R)


# ============================================================================
# SOLUTION PREPARATION
# ============================================================================

def dilution_calculator(C1=None, V1=None, C2=None, V2=None):
    """
    Calculate dilution using C1V1 = C2V2
    Provide 3 of 4 variables to solve for the 4th.
    
    C1: Initial concentration
    V1: Initial volume
    C2: Final concentration
    V2: Final volume
    """
    known_vars = sum(x is not None for x in [C1, V1, C2, V2])
    
    if known_vars != 3:
        raise ValueError("Provide exactly 3 variables to solve for the 4th")
    
    if C1 is None:
        return (C2 * V2) / V1
    elif V1 is None:
        return (C2 * V2) / C1
    elif C2 is None:
        return (C1 * V1) / V2
    elif V2 is None:
        return (C1 * V1) / C2


def molarity_calculator(moles=None, volume_L=None, molarity=None, mass_g=None, molar_mass=None):
    """
    Calculate molarity (M = mol/L) or related quantities.
    """
    # Calculate moles from mass if provided
    if mass_g is not None and molar_mass is not None:
        moles = mass_g / molar_mass
    
    known = sum(x is not None for x in [moles, volume_L, molarity])
    
    if known != 2:
        raise ValueError("Provide exactly 2 of: moles, volume_L, molarity")
    
    if molarity is None:
        return moles / volume_L
    elif moles is None:
        return molarity * volume_L
    elif volume_L is None:
        return moles / molarity


# ============================================================================
# pH CALCULATIONS
# ============================================================================

def pH_calculator(H_concentration=None, pH=None, pOH=None, OH_concentration=None):
    """
    Calculate pH, pOH, [H+], or [OH-] given one value.
    """
    import math
    
    if H_concentration is not None:
        pH = -math.log10(H_concentration)
        pOH = 14 - pH
        OH_concentration = 10**(-pOH)
    elif pH is not None:
        H_concentration = 10**(-pH)
        pOH = 14 - pH
        OH_concentration = 10**(-pOH)
    elif pOH is not None:
        pH = 14 - pOH
        H_concentration = 10**(-pH)
        OH_concentration = 10**(-pOH)
    elif OH_concentration is not None:
        pOH = -math.log10(OH_concentration)
        pH = 14 - pOH
        H_concentration = 10**(-pH)
    else:
        raise ValueError("Provide one of: H_concentration, pH, pOH, OH_concentration")
    
    return {
        'pH': pH,
        'pOH': pOH,
        '[H+]': H_concentration,
        '[OH-]': OH_concentration
    }


# ============================================================================
# STOICHIOMETRY
# ============================================================================

def balance_equation_info():
    """Provide information about balancing equations (manual feature)."""
    return """
Equation balancing is a manual process, but here's the approach:

1. Write the unbalanced equation
2. Count atoms of each element on both sides
3. Adjust coefficients (not subscripts) to balance
4. Start with the most complex molecule
5. Balance elements that appear in only one reactant and product first
6. Balance hydrogen and oxygen last

Example:
Unbalanced: C3H8 + O2 → CO2 + H2O
Balanced: C3H8 + 5O2 → 3CO2 + 4H2O

Verification:
  C: 3 = 3 ✓
  H: 8 = 8 ✓
  O: 10 = 10 ✓
"""


def mole_conversion(value, from_unit, to_unit, molar_mass=None):
    """
    Convert between moles, grams, and particles.
    
    Units: 'mol', 'g', 'particles'
    """
    # First convert to moles
    if from_unit == 'mol':
        moles = value
    elif from_unit == 'g':
        if molar_mass is None:
            raise ValueError("Molar mass required for gram conversions")
        moles = value / molar_mass
    elif from_unit == 'particles':
        moles = value / AVOGADRO
    else:
        raise ValueError(f"Unknown unit: {from_unit}")
    
    # Then convert to target unit
    if to_unit == 'mol':
        return moles
    elif to_unit == 'g':
        if molar_mass is None:
            raise ValueError("Molar mass required for gram conversions")
        return moles * molar_mass
    elif to_unit == 'particles':
        return moles * AVOGADRO
    else:
        raise ValueError(f"Unknown unit: {to_unit}")


# ============================================================================
# PERIODIC TABLE DISPLAY
# ============================================================================

def display_periodic_table():
    """Display a simple periodic table grid."""
    table = """
PERIODIC TABLE OF ELEMENTS
═══════════════════════════════════════════════════════════════════════════

  1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18
 ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───
| H |                                                                                  |He |
 ───                                                                                   ───
|Li |Be |                                                       | B | C | N | O | F |Ne |
 ───  ───                                                        ───  ───  ───  ───  ───  ───
|Na |Mg |                                                       |Al |Si | P | S |Cl |Ar |
 ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───    ───  ───  ───  ───  ───  ───
| K |Ca |Sc |Ti | V |Cr |Mn |Fe |Co |Ni |Cu |Zn |               |Ga |Ge |As |Se |Br |Kr |
 ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───    ───  ───  ───  ───  ───  ───
|Rb |Sr | Y |Zr |Nb |Mo |Tc |Ru |Rh |Pd |Ag |Cd |               |In |Sn |Sb |Te | I |Xe |
 ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───    ───  ───  ───  ───  ───  ───
|Cs |Ba |La*|Hf |Ta | W |Re |Os |Ir |Pt |Au |Hg |               |Tl |Pb |Bi |Po |At |Rn |
 ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───    ───  ───  ───  ───  ───  ───
|Fr |Ra |Ac°|Rf |Db |Sg |Bh |Hs |Mt |Ds |Rg |Cn |               |Nh |Fl |Mc |Lv |Ts |Og |
 ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───  ───    ───  ───  ───  ───  ───  ───

      * Lanthanides:  La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu
      ° Actinides:    Ac Th Pa U  Np Pu Am Cm Bk Cf Es Fm Md No Lr

Use 'chem_toolkit.py element <symbol/name/number>' for detailed information.
"""
    return table


# ============================================================================
# CLI INTERFACE
# ============================================================================

def format_output(title, data):
    """Format output nicely."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")
    for key, value in data.items():
        if isinstance(value, float):
            print(f"  {key:.<30} {value:.4f}")
        else:
            print(f"  {key:.<30} {value}")
    print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Chemistry Calculation Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s element H
  %(prog)s element Sodium
  %(prog)s element 6
  %(prog)s molar H2O
  %(prog)s molar Ca(OH)2
  %(prog)s gas -P 2 -V 5 -T 300
  %(prog)s dilution -C1 10 -V1 50 -C2 2
  %(prog)s molarity --moles 0.5 --volume 2
  %(prog)s pH --pH 7
  %(prog)s convert --value 18 --from g --to mol --molar-mass 18.015
  %(prog)s table
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Element lookup
    elem_parser = subparsers.add_parser('element', help='Look up element information')
    elem_parser.add_argument('query', help='Element symbol, name, or atomic number')
    
    # Molar mass
    molar_parser = subparsers.add_parser('molar', help='Calculate molar mass')
    molar_parser.add_argument('formula', help='Chemical formula (e.g., H2O, Ca(OH)2)')
    
    # Ideal gas law
    gas_parser = subparsers.add_parser('gas', help='Ideal gas law calculator (PV=nRT)')
    gas_parser.add_argument('-P', '--pressure', type=float, help='Pressure (atm)')
    gas_parser.add_argument('-V', '--volume', type=float, help='Volume (L)')
    gas_parser.add_argument('-n', '--moles', type=float, help='Moles (mol)')
    gas_parser.add_argument('-T', '--temperature', type=float, help='Temperature (K)')
    
    # Dilution
    dil_parser = subparsers.add_parser('dilution', help='Dilution calculator (C1V1=C2V2)')
    dil_parser.add_argument('-C1', '--conc1', type=float, help='Initial concentration')
    dil_parser.add_argument('-V1', '--vol1', type=float, help='Initial volume')
    dil_parser.add_argument('-C2', '--conc2', type=float, help='Final concentration')
    dil_parser.add_argument('-V2', '--vol2', type=float, help='Final volume')
    
    # Molarity
    mol_parser = subparsers.add_parser('molarity', help='Molarity calculator')
    mol_parser.add_argument('--moles', type=float, help='Moles')
    mol_parser.add_argument('--volume', type=float, help='Volume (L)')
    mol_parser.add_argument('--molarity', type=float, help='Molarity (M)')
    mol_parser.add_argument('--mass', type=float, help='Mass (g)')
    mol_parser.add_argument('--molar-mass', type=float, help='Molar mass (g/mol)')
    
    # pH calculator
    ph_parser = subparsers.add_parser('ph', help='pH calculator')
    ph_parser.add_argument('--pH', type=float, help='pH value')
    ph_parser.add_argument('--pOH', type=float, help='pOH value')
    ph_parser.add_argument('--H-conc', type=float, help='[H+] concentration')
    ph_parser.add_argument('--OH-conc', type=float, help='[OH-] concentration')
    
    # Conversion
    conv_parser = subparsers.add_parser('convert', help='Convert between moles, grams, particles')
    conv_parser.add_argument('--value', type=float, required=True, help='Value to convert')
    conv_parser.add_argument('--from', dest='from_unit', required=True, 
                             choices=['mol', 'g', 'particles'], help='From unit')
    conv_parser.add_argument('--to', dest='to_unit', required=True,
                             choices=['mol', 'g', 'particles'], help='To unit')
    conv_parser.add_argument('--molar-mass', type=float, help='Molar mass (required for g conversions)')
    
    # Periodic table
    subparsers.add_parser('table', help='Display periodic table')
    
    # Balance info
    subparsers.add_parser('balance', help='Show equation balancing guide')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'element':
            info = element_info(args.query)
            if info:
                format_output(f"Element Information: {info['name']}", {
                    'Symbol': info['symbol'],
                    'Atomic Number': info['number'],
                    'Atomic Weight': f"{info['weight']:.3f} u",
                    'Group': info['group'],
                    'Phase': info['phase'].capitalize()
                })
            else:
                print(f"Error: Element '{args.query}' not found.")
        
        elif args.command == 'molar':
            composition = parse_formula(args.formula)
            mass = calculate_molar_mass(args.formula)
            
            print(f"\n{'='*70}")
            print(f"  Molar Mass Calculation: {args.formula}")
            print(f"{'='*70}")
            print(f"  Composition:")
            for element, count in sorted(composition.items()):
                elem_mass = PERIODIC_TABLE[element]['weight'] * count
                print(f"    {element:.<10} {count} × {PERIODIC_TABLE[element]['weight']:.3f} = {elem_mass:.3f} g/mol")
            print(f"  {'-'*68}")
            print(f"  {'Total Molar Mass':.<30} {mass:.3f} g/mol")
            print(f"{'='*70}\n")
        
        elif args.command == 'gas':
            result = ideal_gas_law(
                P=args.pressure,
                V=args.volume,
                n=args.moles,
                T=args.temperature
            )
            
            # Determine which variable was solved
            if args.pressure is None:
                var_name = "Pressure (P)"
                unit = "atm"
            elif args.volume is None:
                var_name = "Volume (V)"
                unit = "L"
            elif args.moles is None:
                var_name = "Moles (n)"
                unit = "mol"
            else:
                var_name = "Temperature (T)"
                unit = "K"
            
            format_output("Ideal Gas Law: PV = nRT", {
                var_name: f"{result:.4f} {unit}",
                'Given P': f"{args.pressure} atm" if args.pressure else "—",
                'Given V': f"{args.volume} L" if args.volume else "—",
                'Given n': f"{args.moles} mol" if args.moles else "—",
                'Given T': f"{args.temperature} K" if args.temperature else "—",
            })
        
        elif args.command == 'dilution':
            result = dilution_calculator(
                C1=args.conc1,
                V1=args.vol1,
                C2=args.conc2,
                V2=args.vol2
            )
            
            # Determine which variable was solved
            if args.conc1 is None:
                var_name = "Initial Concentration (C1)"
            elif args.vol1 is None:
                var_name = "Initial Volume (V1)"
            elif args.conc2 is None:
                var_name = "Final Concentration (C2)"
            else:
                var_name = "Final Volume (V2)"
            
            format_output("Dilution: C1V1 = C2V2", {
                var_name: f"{result:.4f}",
                'C1': args.conc1 if args.conc1 else "—",
                'V1': args.vol1 if args.vol1 else "—",
                'C2': args.conc2 if args.conc2 else "—",
                'V2': args.vol2 if args.vol2 else "—",
            })
        
        elif args.command == 'molarity':
            result = molarity_calculator(
                moles=args.moles,
                volume_L=args.volume,
                molarity=args.molarity,
                mass_g=args.mass,
                molar_mass=args.molar_mass
            )
            
            if args.molarity is None:
                var_name = "Molarity"
                unit = "M"
            elif args.moles is None:
                var_name = "Moles"
                unit = "mol"
            else:
                var_name = "Volume"
                unit = "L"
            
            format_output("Molarity Calculation", {
                var_name: f"{result:.4f} {unit}",
                'Moles': f"{args.moles} mol" if args.moles else "—",
                'Volume': f"{args.volume} L" if args.volume else "—",
                'Molarity': f"{args.molarity} M" if args.molarity else "—",
            })
        
        elif args.command == 'ph':
            result = pH_calculator(
                H_concentration=args.H_conc,
                pH=args.pH,
                pOH=args.pOH,
                OH_concentration=args.OH_conc
            )
            
            format_output("pH/pOH Calculation", {
                'pH': f"{result['pH']:.2f}",
                'pOH': f"{result['pOH']:.2f}",
                '[H+] concentration': f"{result['[H+]']:.2e} M",
                '[OH-] concentration': f"{result['[OH-]']:.2e} M",
                'Solution Type': 'Acidic' if result['pH'] < 7 else ('Basic' if result['pH'] > 7 else 'Neutral')
            })
        
        elif args.command == 'convert':
            result = mole_conversion(
                value=args.value,
                from_unit=args.from_unit,
                to_unit=args.to_unit,
                molar_mass=args.molar_mass
            )
            
            format_output("Unit Conversion", {
                f"From": f"{args.value} {args.from_unit}",
                f"To": f"{result:.4e} {args.to_unit}",
                'Molar Mass Used': f"{args.molar_mass} g/mol" if args.molar_mass else "—"
            })
        
        elif args.command == 'table':
            print(display_periodic_table())
        
        elif args.command == 'balance':
            print(balance_equation_info())
    
    except Exception as e:
        print(f"\n❌ Error: {e}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()