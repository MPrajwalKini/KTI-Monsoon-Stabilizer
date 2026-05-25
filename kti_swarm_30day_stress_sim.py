import math
import random

def simulate_30_day_kti_fleet(num_buoys=1):
    """
    Simulates the performance of KTI buoys over 720 hours (30 days)
    accounting for changing weather states (Calm, Normal, Storm).
    """
    print("=" * 70)
    print(f" KTI SYSTEM 30-DAY ENVIRONMENTAL STRESS SIMULATION ({num_buoys} BUOY(S)) ")
    print("=" * 70)
    
    # Constants
    RHO_SEAWATER = 1025      # kg/m^3
    SPECIFIC_HEAT = 3993     # J/(kg*C)
    PIPE_DIAMETER_M = 1.2    # Tube diameter
    SURFACE_TEMP_C = 29.5    # El Niño surface heat
    DEEP_TEMP_C = 14.0       # Deep ocean cold
    DELTA_T = SURFACE_TEMP_C - DEEP_TEMP_C
    
    pipe_radius = PIPE_DIAMETER_M / 2.0
    pipe_area = math.pi * (pipe_radius ** 2)
    
    # Cumulative Trackers
    total_volume_m3 = 0.0
    total_energy_gj = 0.0
    
    # Weather State Trackers (for final report)
    calm_hours = 0
    normal_hours = 0
    storm_hours = 0
    
    # Initial weather state
    current_state = "NORMAL"
    
    # Loop through 720 hours (24 hours * 30 days)
    for hour in range(1, 721):
        # Determine weather state transition probabilities per hour
        roll = random.random()
        if current_state == "CALM":
            if roll < 0.15: current_state = "NORMAL"
        elif current_state == "NORMAL":
            if roll < 0.10: current_state = "CALM"
            elif roll > 0.92: current_state = "STORM"  # 8% chance to hit a storm
        elif current_state == "STORM":
            if roll < 0.30: current_state = "NORMAL"  # Storms clear out eventually
            
        # Set dynamic environmental and mechanical variables based on weather
        if current_state == "CALM":
            calm_hours += 1
            wave_height = random.uniform(0.4, 0.9)
            wave_period = random.uniform(7.0, 9.0)
            valve_efficiency = 0.92  # Smooth, gentle waves mean near-perfect valve seal
        elif current_state == "NORMAL":
            normal_hours += 1
            wave_height = random.uniform(1.2, 2.2)
            wave_period = random.uniform(5.5, 7.5)
            valve_efficiency = 0.85  # Standard operating parameters
        elif current_state == "STORM":
            storm_hours += 1
            wave_height = random.uniform(4.0, 7.5)   # Giant storm waves
            wave_period = random.uniform(4.0, 6.0)   # Rapid, choppy frequencies
            valve_efficiency = random.uniform(0.35, 0.55) # Heavy degradation due to tilting/submersion
            
        # Physics Calculations for this specific hour
        waves_this_hour = 3600 / wave_period
        vol_per_stroke = pipe_area * wave_height * valve_efficiency
        hourly_volume_m3 = vol_per_stroke * waves_this_hour * num_buoys
        hourly_mass_kg = hourly_volume_m3 * RHO_SEAWATER
        
        # Thermal Energy calculation (Joules -> Gigajoules)
        hourly_energy_j = hourly_mass_kg * SPECIFIC_HEAT * DELTA_T
        hourly_energy_gj = hourly_energy_j / 1_000_000_000
        
        # Accumulate totals
        total_volume_m3 += hourly_volume_m3
        total_energy_gj += hourly_energy_gj
        
    # --- FINAL 30-DAY LOG ANALYSIS ---
    print(f"[-] Weather Breakdown over 30 Days (720 Hours):")
    print(f"    * Calm Weather     : {calm_hours} hours ({calm_hours/720*100:.1f}%)")
    print(f"    * Standard Swell   : {normal_hours} hours ({normal_hours/720*100:.1f}%)")
    print(f"    * Severe Storms    : {storm_hours} hours ({storm_hours/720*100:.1f}%)")
    print("-" * 70)
    print(f"[+] Cumulative 30-Day System Yield:")
    print(f"    * Total Water Displaced   : {total_volume_m3:,.2f} m³")
    print(f"    * Total Liters Injected   : {total_volume_m3 * 1000:,.0f} Liters")
    print(f"    * Total Thermal Energy    : {total_energy_gj:,.2f} GJ (Gigajoules)")
    
    # Contextualizing the energy moved
    equivalent_hiroshima_bombs = (total_energy_gj * 1_000_000_000) / 6.3e13
    print(f"    * Planetary Heat Leverage : Equivalent to removing {equivalent_hiroshima_bombs:.2f} atomic bombs of heat from the surface.")
    print("=" * 70)

# Run the simulation assuming a test cluster deployment of 10 buoys
simulate_30_day_kti_fleet(num_buoys=10)