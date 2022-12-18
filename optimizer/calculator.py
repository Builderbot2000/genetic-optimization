from numpy import inf
from math import floor
from scipy.stats.mvn import mvnun

class Calculator:
    def __init__(self, instance):
        self.instance = instance 
    
    def run(self, state, more_details=False):
        """
        Estimate profit given specifications
        """
        instance = self.instance

        """Configurables"""
        unit_price = state['unit_price']
        num_equipments = state['num_equipments']
        equipment_grade = state['equipment_grade']
        num_workers = state['num_workers']
        worker_wage = state['worker_wage']
        marketing_budget = state['marketing_budget']
        RaD_spending = state['RaD_spending']
        design_spending = state['design_spending']
        construction_spending = state['construction_spending']

        """Nonconfigurables"""
        market_size = instance['market_size']
        mean_unit_price = instance['mean_unit_price']
        unit_price_std = instance['unit_price_std']
        mean_product_quality = instance['mean_product_quality']
        product_quality_std = instance['product_quality_std']
        price_quality_corr = instance['price_quality_correlation']
        cost_of_resources_per_unit = instance['cost_of_resources_per_unit']
        num_equipments_per_unit = instance['num_equipments_per_unit']
        num_workers_per_unit = instance['num_workers_per_unit']
        cost_of_best_equipments = instance['cost_of_best_equipments']
        wage_of_best_workers = instance['wage_of_best_workers']
        logistics_cost_per_unit = instance['logistics_cost_per_unit']
        cost_of_best_contractors = instance['cost_of_best_contractors']
        cost_of_best_architects = instance['cost_of_best_architects']
        full_coverage_marketing_cost = instance['full_coverage_marketing_cost']
        max_product_improvement = instance['max_product_improvement']
        RaD_cost_for_max_improvement = instance['RaD_cost_for_max_improvement']
        carbon_emmision_per_unit = instance['carbon_emmision_per_unit']
        industrial_waste_per_unit = instance['industrial_waste_per_unit']
        emmision_cost_per_kg = instance['emmision_cost_per_kg']
        waste_disposal_cost_per_kg = instance['waste_disposal_cost_per_kg']

        """Intermediate values"""
        workforce_skill_level = min(worker_wage / wage_of_best_workers, 1.0)
        product_improvement = max(min(RaD_spending / RaD_cost_for_max_improvement, 1.0) * 
                                  max_product_improvement, 1.0)
        product_quality = product_improvement * min(equipment_grade, 1.0) * workforce_skill_level
        facility_efficiency = min(1.0, (design_spending / cost_of_best_architects) * \
                                       (construction_spending / cost_of_best_contractors))
        
        """Number of products to be manufactured"""
        product_quantity = floor(facility_efficiency * \
                                 min(num_equipments / num_equipments_per_unit,
                                     num_workers / num_workers_per_unit))
        
        """Calculate costs"""
        equipment_cost = num_equipments * equipment_grade * cost_of_best_equipments
        facility_investment = design_spending + construction_spending + equipment_cost 
        workforce_cost = worker_wage * num_workers
        logistics_cost = logistics_cost_per_unit * product_quantity
        manufacture_cost = cost_of_resources_per_unit * product_quantity 
        operating_cost = manufacture_cost + workforce_cost + logistics_cost
        environmental_cost = product_quantity * \
                           (carbon_emmision_per_unit * emmision_cost_per_kg + \
                            industrial_waste_per_unit * waste_disposal_cost_per_kg)
        
        """Calculate market demand"""
        mean = [mean_unit_price, mean_product_quality]
        cov = [[unit_price_std**2, price_quality_corr * unit_price_std * product_quality_std],
               [price_quality_corr * unit_price_std * product_quality_std, product_quality_std**2]]
        lower = [unit_price, -inf]
        upper = [inf, product_quality]
        market_captured, _ = mvnun(lower, upper, mean, cov)
        marketing_coverage = min(marketing_budget / full_coverage_marketing_cost, 1.0)
        market_demand = market_captured * marketing_coverage * market_size

        """Calculate profit"""
        revenue = unit_price * min(product_quantity, market_demand)
        cost = facility_investment + RaD_spending + operating_cost + \
               marketing_budget + environmental_cost
        profit = revenue - cost

        if not more_details:
            return profit
        else:
            details = {}
            details['workforce_skill_level'] = workforce_skill_level 
            details['product_improvement'] = product_improvement 
            details['product_quality'] = product_quality 
            details['facility_efficiency'] = facility_efficiency 
            details['product_quantity'] = product_quantity 
            details['equipment_cost'] = equipment_cost 
            details['facility_investment'] = facility_investment 
            details['workforce_cost'] = workforce_cost 
            details['logistics_cost'] = logistics_cost
            details['manufacture_cost'] = manufacture_cost 
            details['operating_cost'] = operating_cost 
            details['environmental_cost'] = environmental_cost
            details['market_captured'] = market_captured
            details['marketing_coverage'] = marketing_coverage
            details['market_demand'] = market_demand
            details['revenue'] = revenue
            return details, profit