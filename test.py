import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="Farm Water Optimization", layout="wide")

def hectares_to_acres(hectares):
    return hectares * 2.47105

def acres_to_hectares(acres):
    return acres * 0.404686

def calculate_water_efficiency(crop_type, area_acres, irrigation_method, soil_type):
    # Base water requirements (gallons per acre)
    water_requirements = {
        'corn': 600000,  # ~4.5 acre-feet
        'wheat': 480000, # ~3.6 acre-feet
        'soybeans': 450000,  # ~3.4 acre-feet
        'rice': 800000,  # ~6.0 acre-feet
        'cotton': 640000  # ~4.8 acre-feet
    }
    
    # Irrigation efficiency factors
    irrigation_efficiency = {
        'drip': 0.90,
        'sprinkler': 0.75,
        'flood': 0.50
    }
    
    # Soil type adjustment factors
    soil_efficiency = {
        'sandy': 0.85,  # Requires more water due to drainage
        'loamy': 1.0,   # Ideal soil type
        'clay': 1.15    # Holds water longer
    }
    
    base_water = water_requirements.get(crop_type, 500000)
    total_water = (base_water * area_acres * soil_efficiency[soil_type]) / irrigation_efficiency[irrigation_method]
    return total_water

def gallons_to_cubic_meters(gallons):
    return gallons * 0.00378541

def calculate_cost(water_usage_gallons, cost_per_cubic_meter):
    water_usage_cubic_meters = gallons_to_cubic_meters(water_usage_gallons)
    return water_usage_cubic_meters * cost_per_cubic_meter

def main():
    st.title("Farm Water Usage Optimization System")
    
    # Sidebar for input parameters
    with st.sidebar:
        st.header("Farm Parameters")
        crop_type = st.selectbox(
            "Select Crop Type",
            ['corn', 'wheat', 'soybeans', 'rice', 'cotton']
        )
        
        # Area input in acres with hectare conversion shown
        area_acres = st.number_input(
            "Farm Area (acres)",
            min_value=1.0,
            max_value=2500.0,
            value=25.0
        )
        
        # Show hectare conversion
        st.info(f"{area_acres:.2f} acres = {acres_to_hectares(area_acres):.2f} hectares")
        
        irrigation_method = st.selectbox(
            "Irrigation Method",
            ['drip', 'sprinkler', 'flood']
        )
        
        soil_type = st.selectbox(
            "Soil Type",
            ['sandy', 'loamy', 'clay']
        )
        
        water_cost = st.number_input(
            "Water Cost ($ per cubic meter)",
            min_value=0.1,
            max_value=10.0,
            value=0.5
        )

    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Current Water Usage Analysis")
        current_water_usage_gallons = calculate_water_efficiency(
            crop_type, area_acres, irrigation_method, soil_type
        )
        current_water_usage_cubic_meters = gallons_to_cubic_meters(current_water_usage_gallons)
        current_cost = calculate_cost(current_water_usage_gallons, water_cost)
        
        st.metric(
            "Annual Water Usage",
            f"{current_water_usage_gallons:,.0f} gallons"
        )
        st.metric(
            "Annual Water Usage (Metric)",
            f"{current_water_usage_cubic_meters:,.0f} cubic meters"
        )
        st.metric(
            "Annual Water Cost",
            f"${current_cost:,.2f}"
        )
        
        # Add per-acre metrics
        st.metric(
            "Water Usage per Acre",
            f"{(current_water_usage_gallons/area_acres):,.0f} gallons"
        )
        st.metric(
            "Cost per Acre",
            f"${(current_cost/area_acres):,.2f}"
        )

    with col2:
        st.header("Optimization Recommendations")
        
        # Calculate optimized scenarios
        optimized_methods = {
            'drip': calculate_water_efficiency(crop_type, area_acres, 'drip', soil_type),
            'sprinkler': calculate_water_efficiency(crop_type, area_acres, 'sprinkler', soil_type),
            'flood': calculate_water_efficiency(crop_type, area_acres, 'flood', soil_type)
        }
        
        # Find best method
        best_method = min(optimized_methods.items(), key=lambda x: x[1])
        potential_savings_gallons = current_water_usage_gallons - best_method[1]
        potential_savings_cubic_meters = gallons_to_cubic_meters(potential_savings_gallons)
        cost_savings = calculate_cost(potential_savings_gallons, water_cost)
        
        if irrigation_method != best_method[0]:
            st.success(f"Recommended: Switch to {best_method[0]} irrigation")
            st.metric(
                "Potential Water Savings",
                f"{potential_savings_gallons:,.0f} gallons"
            )
            st.metric(
                "Potential Water Savings (Metric)",
                f"{potential_savings_cubic_meters:,.0f} cubic meters"
            )
            st.metric(
                "Potential Cost Savings",
                f"${cost_savings:,.2f}"
            )
            st.metric(
                "Savings per Acre",
                f"${(cost_savings/area_acres):,.2f}"
            )
        else:
            st.success("You're already using the most efficient irrigation method!")

    # Historical comparison
    st.header("Water Usage Trends")
    
    # Generate sample historical data
    dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
    historical_usage = pd.DataFrame({
        'Date': dates,
        'Water Usage (gallons)': [
            current_water_usage_gallons * (1 + np.random.normal(0, 0.1))
            for _ in range(12)
        ]
    })
    
    st.line_chart(
        historical_usage.set_index('Date')
    )
    
    # Conservation tips
    st.header("Water Conservation Tips")
    tips = {
        'drip': [
            "Maintain filters to prevent clogging",
            "Check for leaks regularly",
            "Consider automated scheduling",
            "Monitor soil moisture levels"
        ],
        'sprinkler': [
            "Water during early morning or evening",
            "Adjust sprinkler heads for optimal coverage",
            "Use soil moisture sensors",
            "Consider weather conditions before irrigating"
        ],
        'flood': [
            "Level fields to ensure even distribution",
            "Implement surge flooding techniques",
            "Consider converting to more efficient methods",
            "Monitor field drainage patterns"
        ]
    }
    
    for tip in tips[irrigation_method]:
        st.write(f"• {tip}")

if __name__ == "__main__":
    main()