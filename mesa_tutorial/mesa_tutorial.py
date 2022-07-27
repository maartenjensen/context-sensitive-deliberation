
"""----------------------
     Mesa Tutorial
----------------------"""
from mesa_tutorial.mesa_model import MesaShoppingModel
import matplotlib.pyplot as plt
import numpy as np
import mesa

# Model params
n_agents = 50
grid_with = 10
grid_height = 10

# Model running
my_model = MesaShoppingModel(n_agents, grid_with, grid_height)
for i in range(20):
    my_model.step()

# Plotting
agent_counts = np.zeros((my_model.grid.width, my_model.grid.height))
for cell in my_model.grid.coord_iter():
    cell_content, x, y = cell
    agent_count = len(cell_content)
    agent_counts[x][y] = agent_count

plt.imshow(agent_counts, interpolation="nearest")
plt.colorbar()
plt.show()

# Data processing agent variables
food = my_model.datacollector.get_model_vars_dataframe()
food.plot()
plt.show()
#food.to_csv("output/avg_food.csv")

# Data processing agent variables
agent_params = my_model.datacollector.get_agent_vars_dataframe()
print(agent_params.head())

end_wealth = agent_params.xs(19, level="Step")["Money"]
end_wealth.hist(bins=range(agent_params.Money.max() + 1))
plt.show()

one_agent_food = agent_params.xs(5, level="AgentID")
one_agent_food.Food.plot()
plt.show()

# Batch running
params = {"width": 10, "height": 10, "n_agents": range(10, 100, 10)}

results = mesa.batch_run(
    MesaShoppingModel,
    parameters=params,
    iterations=5,
    max_steps=100,
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

import pandas as pd

results_df = pd.DataFrame(results)
print(results_df.keys())

results_filtered = results_df[(results_df.AgentID == 0) & (results_df.Step == 100)]
N_values = results_filtered.n_agents.values
gini_values = results_filtered.Money.values
plt.scatter(N_values, gini_values)
plt.show()

# First, we filter the results
one_episode_wealth = results_df[(results_df.n_agents == 10) & (results_df.iteration == 2)]
# Then, print the columns of interest of the filtered data frame
print(
    one_episode_wealth.to_string(
        index=False, columns=["Step", "AgentID", "Money"], max_rows=25
    )
)

results_one_episode = results_df[
    (results_df.n_agents == 10) & (results_df.iteration == 1) & (results_df.AgentID == 0)
]
print(results_one_episode.to_string(index=False, columns=["Step", "Money"], max_rows=25))
