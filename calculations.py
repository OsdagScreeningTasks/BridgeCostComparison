class CostCalculator:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def calculate_costs(self, span_length, width, traffic_volume, design_life):
        cost_data = self.db_manager.fetch_all_cost_data()
        results = []

        for material, base_rate, maintenance_rate, repair_rate, demolition_rate, env_factor, social_factor, delay_factor in cost_data:
            construction_cost = span_length * width * base_rate
            maintenance_cost = span_length * width * maintenance_rate * design_life
            repair_cost = span_length * width * repair_rate
            demolition_cost = span_length * width * demolition_rate
            environmental_cost = span_length * width * env_factor
            social_cost = traffic_volume * social_factor * design_life
            user_cost = traffic_volume * delay_factor * design_life
            total_cost = (construction_cost + maintenance_cost + repair_cost +
                          demolition_cost + environmental_cost + social_cost + user_cost)
            results.append([material, construction_cost, maintenance_cost, repair_cost, demolition_cost,
                            environmental_cost, social_cost, user_cost, total_cost])
        return results
