from owlready2 import *
import os

onto_path.append('resources')
math_onto = get_ontology('http://example.org/physics/physics-math').load()
domain_onto = get_ontology('http://example.org/physics/physics-domain').load()
physics_ns = math_onto.get_namespace('http://example.org/physics#')

# Classes
Measurement = math_onto.world.search_one(iri="*#Measurement")
PhysicalQuantity = physics_ns.PhysicalQuantity

# Properties (specifically from math_onto)
hasNumericValue = math_onto.world.search_one(iri="*#hasNumericValue")
hasQuantityType = math_onto.world.search_one(iri="*#hasQuantityType")
hasSymbol = math_onto.world.search_one(iri="*#hasSymbol")

# Quantities
MassQuantity = physics_ns.MassQuantity
LengthQuantity = physics_ns.LengthQuantity
TimeQuantity = physics_ns.TimeQuantity
VelocityQuantity = physics_ns.VelocityQuantity
AccelerationQuantity = physics_ns.AccelerationQuantity
GravitationalParameterQuantity = physics_ns.GravitationalParameterQuantity
DimensionlessQuantity = physics_ns.DimensionlessQuantity

with domain_onto:
    def add_const(name, q_type, value, symbol=None):
        c = domain_onto.world.search_one(iri=f"*#{name}")
        if not c:
            c = Measurement(name)
        
        c.hasQuantityType = [q_type]
        c.hasNumericValue = [value]
        if symbol:
            c.hasSymbol = [symbol]
        return c

    # --- UNIVERSAL CONSTANTS ---
    add_const("Pi", DimensionlessQuantity, 3.141592653589793, "pi")
    add_const("StandardGravity", AccelerationQuantity, 9.80665, "g")
    
    # G needs a specific type or just PhysicalQuantity
    G_type = physics_ns.PhysicalQuantity("UniversalGravitationalConstantType")
    add_const("UniversalGravitationalConstant", G_type, 6.67430e-11, "G")
    
    add_const("SpeedOfLight", VelocityQuantity, 299792458.0, "c")
    
    # --- UNITS / SCALE ---
    add_const("AstronomicalUnit", LengthQuantity, 149597870700.0, "AU")
    add_const("Day", TimeQuantity, 86400.0)
    add_const("JulianYear", TimeQuantity, 31557600.0)
    add_const("MeanSiderealDay", TimeQuantity, 86164.09054)
    add_const("SiderealYear", TimeQuantity, 31558149.0)
    add_const("LightTimeFor1AU", TimeQuantity, 499.004783836)

    bodies = {
        "Sun": {"mu": 1.32712440041279419e20, "rad": 695700000.0, "mass": None},
        "Earth": {"mu": 3.98600435507e14, "rad_eq": 6378136.6, "rad_mean": 6371008.4, "mass": 5.97217e24},
        "Moon": {"mu": 4.902800118e12, "rad": 1737400.0, "mass": 7.34767309e22},
        "Mercury": {"mu": 2.2031868551e13, "rad": 2439400.0, "mass": 0.330103e24},
        "Venus": {"mu": 3.24858592e14, "rad": 6051800.0, "mass": 4.86731e24},
        "Mars": {"mu": 4.2828375816e13, "rad": 3389500.0, "mass": 0.641691e24},
        "Jupiter": {"mu": 1.267127641e17, "rad": 69911000.0, "mass": 1898.125e24},
        "Saturn": {"mu": 3.79405848418e16, "rad": 58232000.0, "mass": 568.317e24},
        "Uranus": {"mu": 5.7945564e15, "rad": 25362000.0, "mass": 86.8099e24},
        "Neptune": {"mu": 6.83652710058e15, "rad": 24622000.0, "mass": 102.4092e24},
        "Pluto": {"mu": 9.755e11, "rad": 1188300.0, "mass": 1.30246e22}
    }

    for body, data in bodies.items():
        if data["mu"]: add_const(f"{body}_GravitationalParameter", GravitationalParameterQuantity, data["mu"])
        if "rad" in data and data["rad"]: add_const(f"{body}_MeanRadius", LengthQuantity, data["rad"])
        if "rad_eq" in data and data["rad_eq"]: add_const(f"{body}_EquatorialRadius", LengthQuantity, data["rad_eq"])
        if "rad_mean" in data and data["rad_mean"]: add_const(f"{body}_MeanRadius", LengthQuantity, data["rad_mean"])
        if data["mass"]: add_const(f"{body}_Mass", MassQuantity, data["mass"])

domain_onto.save(file=os.path.join('resources', 'physics-domain.owl'))
print("Astronomy constants updated in physics-domain.owl")
