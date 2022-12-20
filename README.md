## Continuous Genetic Algorithm Implementation
### Setting up the environment
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Creating problem instance
In the current implementation, the optimizer's fitness score is calculated using Calculator object in optimizer/calculator.py. The formula is detailed in formula.pdf. The paramaters nonconfigurable by the optimizer are specified in instances/\[instance_name\].log. \\

If you do not want to use the current formula, modify the Calculator class in optimizer/calculator.py to your likings.

### Running the optimizer
```
python run_optimizer.py
python run_optimizer.py --input instances/[instance_name].log
python run_optimizer.py -h  ## for more information on how to pass arguments to modify hyperparameters of the optimizer
```
