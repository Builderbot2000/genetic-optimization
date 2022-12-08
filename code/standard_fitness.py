import fitness_function

class StandardFitness(fitness_function.FitnessFunction):    
    def evaluate(self, state) -> dict:
        """
        Evaluate and return the fitness scores of a state
        -
        Outputs a list of scores that measures the state's performance on different aspects 
        (ex. a product's capacity for profit, risk of litigation, environmental impact, etc.)
        Scores are calculated according to the state's attributes and the modifiers given in parameter
        -
        Modifiers: each modifier in modifiers is a length m list of strings in the format of
        "[target] [args[0]] [args[1]] ... [args[n]] @ [Expression] (ex. 'args[0] + args[1] * args[2]')" 
        * Note that target is the 0th index item and expression is the mth index item
        * Each arg is the key to a state value
        * The fitness score pointed to by target key will be set to the result of the expression
        """
        output_scores = {}
        for modifier in self.optimizer.modifiers:
            args = []
            for arg in modifier[1:len(modifier)-2]:
                args.append(state[arg])
            output_scores[modifier[0]] = eval(modifier[len(modifier)-1])
        return output_scores