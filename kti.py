import math

def simulate_thermocline_pump(
    wave_height_m=1.8,       # Average height of Indian Ocean waves (peak to trough)
    wave_period_s=6.5,       # Seconds between wave crests
    pipe_diameter_m=1.2,     # Diameter of the KTI downward displacement tube
    thermocline_depth_m=120, # Depth where cold layer begins
    surface_temp_c=29.5,     # Warm surface water temperature (El Niño conditions)
    deep_temp_c=14.0,        # Cold deep ocean temperature below thermocline
    valve_efficiency=0.85    # 85% efficiency (accounting for valve lag/backflow)
):
    """
    Simulates a single wave-driven Kinetic Thermocline Inverter (KTI) buoy.
    Calculates hourly water displacement and downward thermal energy transfer.
    """
    print("=" * 60)
    print(" KINETIC THERMOCLINE INVERTER (KTI) - SIMULATION LOG ")
    print("=" * 60)
    
    # Constants
    RHO_SEAWATER = 1025      # Density of seawater in kg/m^3
    SPECIFIC_HEAT = 3993     # Specific heat capacity of seawater in J/(kg*C)
    
    # 1. Calculate Wave Frequency
    waves_per_hour = 3600 / wave_period_s
    
    # 2. Calculate Pump Geometry
    pipe_radius = pipe_diameter_m / 2.0
    pipe_area = math.pi * (pipe_radius ** 2)
    
    # 3. Volumetric Displacement Per Stroke (Wave Height = Stroke Length)
    volume_per_stroke_m3 = pipe_area * wave_height_m * valve_efficiency
    
    # 4. Hourly Performance
    total_volume_hourly_m3 = volume_per_stroke_m3 * waves_per_hour
    total_mass_hourly_kg = total_volume_hourly_m3 * RHO_SEAWATER
    
    # 5. Thermodynamics: Heat Energy Transferred Downward
    # Delta T is the thermal difference between the layers we are modifying
    delta_t = surface_temp_c - deep_temp_c
    heat_energy_joules = total_mass_hourly_kg * SPECIFIC_HEAT * delta_t
    heat_energy_mj = heat_energy_joules / 1_000_000 # Convert to Megajoules
    
    # --- OUTPUT RESULTS ---
    print(f"[-] Input Conditions:")
    print(f"    * Ocean Wave Regime: {wave_height_m}m height @ {wave_period_s}s period")
    print(f"    * Tube Dimensions  : {pipe_diameter_m}m Diameter x {thermocline_depth_m}m Depth")
    print(f"    * Thermal Gradient : Surface ({surface_temp_c}°C) -> Deep ({deep_temp_c}°C)")
    print(f"    * Valve Efficiency : {valve_efficiency * 100}%")
    print("-" * 60)
    print(f"[+] Simulation Output (Per Single Buoy / Hour):")
    print(f"    * Waves Processed  : {int(waves_per_hour)} waves/hour")
    print(f"    * Water Displaced  : {total_volume_hourly_m3:.2f} cubic meters / hour")
    print(f"    * Liters Pumped    : {total_volume_hourly_m3 * 1000:,.0f} Liters / hour")
    print(f"    * Mass Displaced   : {total_mass_hourly_kg:,.2f} kg / hour")
    print(f"    * Heat Forced Down : {heat_energy_mj:,.2f} MJ of thermal energy / hour")
    print("=" * 60)
    
    return total_volume_hourly_m3, heat_energy_mj

# Execute the simulation with standard equatorial Indian Ocean parameters
displaced_vol, thermal_mj = simulate_thermocline_pump()