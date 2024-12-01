import math
import numpy as np

# Constants
RHEOSTAT_MIN = 0    # Minimum resistance of the rheostat in ohms
RHEOSTAT_MAX = 1000000000000000000000  # Maximum resistance of the rheostat in ohms
DESIRED_VOLTAGE = 230  # Target voltage in volts
BLADE_ANGLE_LIMIT = 360  # Maximum blade angle in degrees


# Function to calculate effective wind speed
def effective_wind_speed(wind_speed, wind_angle):
    """
    Calculates the effective wind speed based on wind speed and angle.
    The effective speed considers the component of wind blowing perpendicular to the blades.
    """
    return wind_speed * math.cos(math.radians(wind_angle))

# Function to calculate angular speed
def angular_speed(effective_speed, temperature):
    ANGULAR_CONSTANT = (1.45)
    """
    Calculates angular speed considering the wind speed and temperature.
    Angular speed is inversely proportional to temperature.
    """
    return (ANGULAR_CONSTANT)*effective_speed / temperature


def calculate_blade_angle(wind_angle):
    BLADE_ANGLE_LIMIT = 360  # Maximum blade angle in degrees
    SCALE = 100  # Scaling factor to control the infinity behavior
    TOLERANCE = 1e-14
    """
    Adjusts the blade pitch angle based on wind direction using a tangent function for smooth transitions.
    At 0 degrees, the angle is 0. At 180 degrees, it is 180.
    At 90 and 270 degrees, the angle smoothly transitions towards infinity.
    """
    # Wrap the angle between 0 and 360 degrees
    wind_angle = wind_angle % 360  # Ensure the angle is between 0 and 360 degrees
    
    # Apply a tangent function
    # Use tan function for angles between 0 and 180 degrees (and scale for smooth transition to infinity)
    if wind_angle == 90 or wind_angle == 270:
        return float('inf')  # Infinite angle at 90 and 270 degrees
    
    # Adjust the angle with a tangent function centered at 0° and 180° for smooth transition
    # Scale the input to get a better transition behavior
    adjusted_angle = 180 * math.tan(math.radians(wind_angle - 180)) / 10  # Scaled tangent for smoother results
    
    # Apply tolerance: if the adjusted angle is very close to zero, treat it as zero
    if abs(adjusted_angle) < TOLERANCE:
        adjusted_angle = 0.0
    
    return adjusted_angle


# Function to adjust rheostat resistance
def adjust_rheostat(voltage, current, wind_speed):
    """
    Adjusts the rheostat to maintain the desired voltage while considering the effective wind speed.
    Uses Ohm's law: V = IR, rearranged as R = V / I, and adjusts based on wind speed.
    """
    if current == 0:  # Prevent division by zero
        return RHEOSTAT_MAX
    
    # Calculate resistance using Ohm's law
    resistance = voltage / current

    # Adjust resistance based on the effective wind speed:
    # We assume that higher wind speeds should result in higher resistance to stabilize voltage fluctuations
    # This can be modeled as scaling the resistance based on wind speed
    adjusted_resistance = resistance * (1 + wind_speed / 100)  # Modify this factor as needed for fine-tuning
    
    # Clamp the adjusted resistance to the predefined limits
    return max(RHEOSTAT_MIN, min(RHEOSTAT_MAX, adjusted_resistance))

# Function to calculate energy delivered
def calculate_energy(voltage, current, time_period, wind_speed, omega):
    """
    Calculates the energy delivered, factoring in the influence of wind speed, voltage, current, and angular speed (ω).
    """
    # Adjust voltage and current based on wind speed (as previously discussed)
    adjusted_voltage = voltage * (1 + wind_speed / 100)  # Example scaling factor based on wind speed
    adjusted_current = current * (1 + wind_speed / 100)  # Similar scaling for current

    # Incorporate angular speed (ω) into the energy calculation
    # Assume that the power generated is proportional to ω (angular speed) and wind speed
    # For simplicity, using a simple model: P = k * omega * wind_speed
    k = 1  # Scaling constant (depends on system characteristics)
    power = k * omega * wind_speed * (10**5)  # Power generated based on angular speed and wind speed

    # Energy delivered is the power over the time period
    energy = power * time_period  # Energy in kWh (or adjust units as needed)

    return energy


# Main Function
def optimize_wind_turbine(wind_speed, wind_angle, temperature, current, time_period):
    """
    Optimizes the wind turbine operation for constant voltage and maximum energy output.
    """
    # Step 1: Calculate effective wind speed
    v_eff = effective_wind_speed(wind_speed, wind_angle)

    # Step 2: Calculate angular speed
    omega_1 = angular_speed(v_eff, temperature)

    # Step 3: Adjust blade pitch angle
    blade_angle = calculate_blade_angle(wind_angle)

    # Step 4: Adjust rheostat resistance
    rheostat_resistance = adjust_rheostat(DESIRED_VOLTAGE, current,v_eff)

    # Step 5: Calculate energy delivered
    energy = calculate_energy(DESIRED_VOLTAGE, current, time_period,v_eff,omega_1)

    # Results
    return {
        #"Effective Wind Speed (m/s)": v_eff,
        #"Angular Speed (rad/s)": omega_1,
        "Blade Pitch Angle (degrees)": blade_angle,
        "Rheostat Resistance (ohms)": rheostat_resistance,
        "Energy Delivered (kWh)": energy / 1000  # Convert to kWh
    }

# Example usage
if __name__ == "__main__":
    wind_speed = 60  # m/s
    wind_angle = 0  # degrees
    temperature = 600.0  # Kelvin
    current = 5.0  # Amperes
    time_period = 1.0  # Hours

        # Optimization
    results = optimize_wind_turbine(wind_speed, (wind_angle), temperature, current, time_period)

        # Print results
    for key, value in results.items():
            
        print(f"{key}: {value}")
    

        
