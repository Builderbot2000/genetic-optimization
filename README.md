## Continuous Genetic Algorithm Implementation
### Setting up the environment
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Creating problem instance
In the current implementation, the optimizer's fitness score is calculated using Calculator object in optimizer/calculator.py. The formula is detailed in formula.pdf. The paramaters nonconfigurable by the optimizer are specified in instances/\[instance_name\].log. \

If you do not want to use the current formula, modify the Calculator class in optimizer/calculator.py to your likings.

### Running the optimizer
```
python run_optimizer.py
python run_optimizer.py --input instances/[instance_name].log
python run_optimizer.py -h  ## for more information on how to pass arguments to modify hyperparameters of the optimizer
```
The results will be in output/\[instance_name\].out.log.

### Running the experiments
Our experiment results are available in output/wafer.expt.csv. \
To check any of these results, you need to open output/wafer.expt.csv in Excel or program where csv files are viewable. Then find a set of crossover_operator, selection_factor, branching_factor, mutation_factor, and random_seed you want to run. The results will span 10 rows (score every 100 epochs) \
Please substitute the name of crossover operator by their shorthand: {'intermediate_crossover': 'ic', 'heuristic_crossover': 'hc', 'single_arithmetic_crossover': 'sac'}
```
python run_experiment.py --crossover_operator CROSSOVER_OPERATOR --selection_factor SELECTION_FACTOR --branching_factor BRANCHING_FACTOR --mutation_factor MUTATION_FACTOR --random_seed RANDOM_SEED
```
