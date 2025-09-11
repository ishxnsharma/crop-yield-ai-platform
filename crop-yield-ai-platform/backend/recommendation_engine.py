"""
Recommendation Engine for Crop Yield Optimization
Provides actionable recommendations for irrigation, fertilization, and pest control
"""

def generate_recommendations(input_data, predicted_yield):
    """
    Generate farming recommendations based on input parameters and predicted yield
    """
    recommendations = {
        'irrigation': [],
        'fertilization': [],
        'pest_control': [],
        'general': [],
        'priority': 'medium'
    }
    
    # Analyze temperature
    temp = input_data['temperature']
    if temp > 35:
        recommendations['irrigation'].append({
            'action': 'Increase irrigation frequency',
            'detail': 'High temperature detected. Consider irrigating twice daily during peak heat.',
            'impact': 'Can improve yield by 5-10%'
        })
        recommendations['priority'] = 'high'
    elif temp < 15:
        recommendations['irrigation'].append({
            'action': 'Reduce irrigation',
            'detail': 'Low temperature detected. Reduce watering to prevent root rot.',
            'impact': 'Prevents crop damage'
        })
    
    # Analyze rainfall
    rainfall = input_data['rainfall']
    if rainfall < 500:
        recommendations['irrigation'].append({
            'action': 'Implement drip irrigation',
            'detail': 'Low rainfall region. Drip irrigation can save 40% water.',
            'impact': 'Water conservation and consistent yield'
        })
    elif rainfall > 1500:
        recommendations['general'].append({
            'action': 'Ensure proper drainage',
            'detail': 'High rainfall detected. Good drainage prevents waterlogging.',
            'impact': 'Prevents root diseases'
        })
    
    # Analyze soil pH
    soil_ph = input_data['soil_ph']
    if soil_ph < 6.0:
        recommendations['fertilization'].append({
            'action': 'Add lime to soil',
            'detail': f'Soil pH is {soil_ph}, which is acidic. Add agricultural lime.',
            'impact': 'Improves nutrient availability'
        })
    elif soil_ph > 7.5:
        recommendations['fertilization'].append({
            'action': 'Add sulfur or organic matter',
            'detail': f'Soil pH is {soil_ph}, which is alkaline. Add sulfur to lower pH.',
            'impact': 'Better nutrient absorption'
        })
    
    # Analyze NPK levels
    nitrogen = input_data['nitrogen']
    phosphorus = input_data['phosphorus']
    potassium = input_data['potassium']
    
    if nitrogen < 100:
        recommendations['fertilization'].append({
            'action': 'Increase nitrogen fertilizer',
            'detail': 'Low nitrogen detected. Apply urea or ammonium nitrate.',
            'dosage': f'Add {150 - nitrogen} kg/hectare',
            'impact': 'Improves leaf growth and yield'
        })
    
    if phosphorus < 35:
        recommendations['fertilization'].append({
            'action': 'Add phosphorus fertilizer',
            'detail': 'Low phosphorus levels. Apply DAP or superphosphate.',
            'dosage': f'Add {50 - phosphorus} kg/hectare',
            'impact': 'Better root development'
        })
    
    if potassium < 35:
        recommendations['fertilization'].append({
            'action': 'Add potassium fertilizer',
            'detail': 'Low potassium detected. Apply MOP (Muriate of Potash).',
            'dosage': f'Add {50 - potassium} kg/hectare',
            'impact': 'Improves disease resistance'
        })
    
    # Analyze pesticide usage
    pesticide = input_data['pesticide_usage']
    if pesticide > 3:
        recommendations['pest_control'].append({
            'action': 'Reduce pesticide usage',
            'detail': 'High pesticide usage detected. Consider integrated pest management.',
            'impact': 'Reduces costs and environmental impact'
        })
        recommendations['pest_control'].append({
            'action': 'Use biological pest control',
            'detail': 'Introduce beneficial insects or use neem-based pesticides.',
            'impact': 'Sustainable pest management'
        })
    
    # Crop-specific recommendations
    crop_type = input_data['crop_type'].lower()
    
    if crop_type == 'rice':
        recommendations['general'].append({
            'action': 'Maintain water level',
            'detail': 'Keep 5-10 cm water level during tillering stage.',
            'impact': 'Critical for rice yield'
        })
    elif crop_type == 'wheat':
        recommendations['general'].append({
            'action': 'Monitor for rust disease',
            'detail': 'Wheat is susceptible to rust. Regular monitoring needed.',
            'impact': 'Prevents major yield loss'
        })
    elif crop_type == 'cotton':
        recommendations['general'].append({
            'action': 'Control bollworm',
            'detail': 'Cotton bollworm is major pest. Use pheromone traps.',
            'impact': 'Can save 20% yield'
        })
    
    # Irrigation optimization
    irrigation_hours = input_data['irrigation_hours']
    if irrigation_hours > 10:
        recommendations['irrigation'].append({
            'action': 'Optimize irrigation schedule',
            'detail': 'Current irrigation seems excessive. Consider soil moisture sensors.',
            'impact': 'Save water and reduce costs'
        })
    
    # Yield-based recommendations
    if crop_type == 'rice' and predicted_yield < 4000:
        recommendations['priority'] = 'high'
        recommendations['general'].append({
            'action': 'Review cultivation practices',
            'detail': 'Yield is below average. Consider soil testing and expert consultation.',
            'impact': 'Can improve yield by 15-20%'
        })
    
    # Add timing recommendations
    recommendations['timing'] = get_seasonal_recommendations(crop_type)
    
    # Calculate optimization score
    optimization_score = calculate_optimization_score(input_data, predicted_yield)
    recommendations['optimization_score'] = optimization_score
    
    return recommendations

def get_seasonal_recommendations(crop_type):
    """Get seasonal farming recommendations"""
    seasonal_tips = {
        'rice': {
            'planting': 'June-July (Kharif), December-January (Rabi)',
            'critical_period': 'Flowering and grain filling stage',
            'harvest_time': '120-150 days after planting'
        },
        'wheat': {
            'planting': 'October-December',
            'critical_period': 'Crown root initiation and flowering',
            'harvest_time': '120-130 days after planting'
        },
        'cotton': {
            'planting': 'April-May',
            'critical_period': 'Square formation and boll development',
            'harvest_time': '180-200 days after planting'
        },
        'maize': {
            'planting': 'June-July (Kharif), October-November (Rabi)',
            'critical_period': 'Tasseling and silking stage',
            'harvest_time': '90-120 days after planting'
        },
        'sugarcane': {
            'planting': 'October-November (Autumn), February-March (Spring)',
            'critical_period': 'Grand growth period',
            'harvest_time': '12-18 months after planting'
        }
    }
    
    return seasonal_tips.get(crop_type.lower(), {
        'planting': 'Consult local agricultural extension',
        'critical_period': 'Monitor regularly',
        'harvest_time': 'Based on crop maturity'
    })

def calculate_optimization_score(input_data, predicted_yield):
    """Calculate optimization score based on input parameters"""
    score = 70  # Base score
    
    # Temperature optimization
    temp = input_data['temperature']
    if 20 <= temp <= 30:
        score += 5
    
    # Soil pH optimization
    ph = input_data['soil_ph']
    if 6.0 <= ph <= 7.0:
        score += 5
    
    # NPK balance
    n = input_data['nitrogen']
    p = input_data['phosphorus']
    k = input_data['potassium']
    
    if 100 <= n <= 150 and 35 <= p <= 50 and 35 <= k <= 50:
        score += 10
    
    # Pesticide usage
    if input_data['pesticide_usage'] < 2:
        score += 5
    
    # Irrigation efficiency
    if 5 <= input_data['irrigation_hours'] <= 8:
        score += 5
    
    return min(score, 100)
