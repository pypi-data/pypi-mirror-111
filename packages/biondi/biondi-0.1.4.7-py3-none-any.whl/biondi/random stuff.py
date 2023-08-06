import biondi

def get_d_values(list_of_lists_of_affected_and_total_coords):
    d_values = []
    for i in list_of_lists_of_affected_and_total_coords:
        obs_densities = biondi.statistics.percent_affected(i[1],i[0])
        sim_densities = biondi.statistics.homogeneity_monte_carlo(i[0],i[1],iterations=1000)
        d_values.append(biondi.statistics.kolmogorov_smirnov_statistic_for_wsi_montecarlo_simulations(obs_densities,sim_densities, test_observed=True, observed_only=True)[0])
    return d_values