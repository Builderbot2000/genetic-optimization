import numpy as np
from scipy.stats.mvn import mvnun

class Calculator:
    def __init__(self, instance):
        self.instance = instance 
    
    def run(self, state, details=False):
        """
        Estimate profit given specifications
        """
        shelf_price = state['shelf_price']
        num_equipments = state['num_equipments']
        equipment_grade = state['equipment_grade']
        num_workers = state['num_workers']
        worker_wage = state['worker_wage']
        marketing_budget = state['marketing_budget']
        RaD_spending = state['RaD_spending']
        design_spending = state['design_spending']
        construction_spending = state['construction_spending']

        market_size = self.instance['market_size']
        mean_shelf_price = self.instance['mean_shelf_price']
        shelf_price_std = self.instance['shelf_price_std']
        mean_product_quality = self.instance['mean_product_quality']
        product_quality_std = self.instance['product_quality_std']
        cost_of_resources_per_unit = self.instance['cost_of_resources_per_unit']
        num_equipments_per_unit = self.instance['num_equipments_per_unit']
        num_workers_per_unit = self.instance['num_workers_per_unit']
        cost_of_best_equipments = self.instance['cost_of_best_equipments']
        wage_for_best_workers = self.instance['wage_for_best_workers']
        pay_for_best_contractors = self.instance['pay_for_best_contractors']
        pay_for_best_facility_designers = self.instance['pay_for_best_facility_designers']
        full_coverage_marketing_cost = self.instance['full_coverage_marketing_cost']
        max_product_improvement = self.instance['max_product_improvement']
        RaD_cost_for_max_improvement = self.instance['RaD_cost_for_max_improvement']
        carbon_emmision_per_unit = self.instance['carbon_emmision_per_unit']
        industrial_waste_per_unit = self.instance['industrial_waste_per_unit']
        emmision_cost_per_kg = self.instance['emmision_cost_per_kg']
        waste_disposal_cost_per_kg = self.instance['waste_disposal_cost_per_kg']

        workforce_skill_level = min(worker_wage / wage_for_best_workers, 1)
        product_improvement = max(min(RaD_spending / RaD_cost_for_max_improvement,  
                                      max_product_improvement), 1)
        product_quality = product_improvement * min(equipment_grade, 1) * workforce_skill_level
        facility_efficiency = min(1, (design_spending / pay_for_best_facility_designers) * \
                                     (construction_spending / pay_for_best_contractors))
        quantity_produced = facility_efficiency * min(num_equipments / num_equipments_per_unit,
                                                      num_workers / num_workers_per_unit) 
        equipment_cost = num_equipments * equipment_grade * cost_of_best_equipments
        facility_investment = design_spending + construction_spending + equipment_cost 
        worker_cost = worker_wage * num_workers
        operating_cost = cost_of_resources_per_unit * quantity_produced + worker_cost
        environmental_tax = quantity_produced * \
                           (carbon_emmision_per_unit * emmision_cost_per_kg + \
                            industrial_waste_per_unit * waste_disposal_cost_per_kg)
        
        mean = [mean_shelf_price, mean_product_quality]
        cov = [[shelf_price_std**2, shelf_price_std*product_quality_std],
               [shelf_price_std*product_quality_std, product_quality_std**2]]
        lower = [shelf_price, -np.inf]
        upper = [np.inf, product_quality]
        percentage_satisfied_with_price_quality, _ = mvnun(lower, upper, mean, cov)
        marketing_coverage = min(marketing_budget / full_coverage_marketing_cost, 1)
        market_demand = percentage_satisfied_with_price_quality * \
                        marketing_coverage * market_size

        revenue = shelf_price * min(quantity_produced, market_demand)
        cost = facility_investment + RaD_spending + operating_cost + \
               marketing_budget + environmental_tax
        profit = revenue - cost

        if details:
            return (workforce_skill_level, product_improvement, product_quality, \
                    marketing_coverage, percentage_satisfied_with_price_quality), \
                   (quantity_produced, revenue, equipment_cost, worker_cost, \
                    environmental_tax), profit
        else:
            return profit