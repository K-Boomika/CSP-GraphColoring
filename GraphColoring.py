import sys

def getData(filename):
    with open(filename, 'r') as f:
        data = f.read()

    # Extract colors value
    colors = int(data[data.find('colors = ') + len('colors = '):data.find('\n', data.find('colors = '))])

    # Extract list of number,number pairs
    pairs = [(int(x.split(',')[0]), int(x.split(',')[1])) for x in data.split('\n') if ',' in x and not x.startswith('#')]

    return [colors,pairs]

class Constraint:
    def __init__(self, variables):
        self.variables = variables

    def satisfied(self, assignment):
        raise NotImplementedError

class CSP:
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains = domains
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
        for variable in self.variables:
            self.domains[variable] = set(self.domains[variable])

        for variable in self.variables:
            self.constraints[variable] = []
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
            self.domains[variable] = set(self.domains[variable])

    def addConstraint(self, constraint):
        for variable in constraint.variables:
            self.constraints[variable].append(constraint)
        # Add tuple of variables as key for constraint
        key = tuple(constraint.variables)
        if key not in self.constraints:
            self.constraints[key] = []
        self.constraints[key].append(constraint)

    def isConsistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def ac3(self, arcs=None):
        if arcs is None:
            # Initialize queue with all arcs in the constraint graph
            arcs = [(var1, var2) for var1 in self.variables for var2 in self.variables if var1 != var2 and any((var1, var2) in constraint.variables for constraint in self.constraints[var1])]
        while arcs:
            var1, var2 = arcs.pop(0)
            if self.revise(var1, var2):
                if not self.domains[var1]:
                    return False
                for neighbor in self.variables:
                    if neighbor != var1 and neighbor in self.constraints[var1]:
                        arcs.append((neighbor, var1))
        return True

    def revise(self, var1, var2):
        revised = False
        for value1 in self.domains[var1]:
            if not any(constraint.satisfied({var1: value1, var2: value2}) for constraint in self.constraints[var1, var2] for value2 in self.domains[var2]):
                self.domains[var1].remove(value1)
                revised = True
        return revised

    def backtrackingSearch(self, assignment={}, depth_limit=None):
        if depth_limit is not None and len(assignment) > depth_limit:
            return None
        if len(assignment) == len(self.variables):
            return assignment

        unassigned = [v for v in self.variables if v not in assignment]
        variable = max(unassigned, key=lambda v: (len(self.constraints[v]), -self.countUnassignedNeighbors(v, sorted(self.domains[v])[0], assignment), len(self.domains[v])))

        for value in sorted(self.domains[variable], key=lambda val: self.countUnassignedNeighbors(variable, val, assignment)):
            local_assignment = assignment.copy()
            local_domains = {k: v.copy() for k, v in self.domains.items()}
            local_assignment[variable] = value
            if self.isConsistent(variable, local_assignment):
                local_domains[variable] = {value}
                inferences = self.forwardCheck(variable, value, local_assignment, local_domains)
                if inferences is not None:
                    result = self.backtrackingSearch(local_assignment, depth_limit)
                    if result is not None:
                        return result
                self.reverseInferences(inferences)
        return None

    def forwardCheck(self, variable, value, assignment, domains):
        inferences = {}
        for constraint in self.constraints[variable]:
            other_variable = next((v for v in constraint.variables if v != variable), None)
            if other_variable is not None and other_variable not in assignment:
                for other_value in domains[other_variable]:
                    if not constraint.satisfied({variable: value, other_variable: other_value}):
                        if len(domains[other_variable]) == 1:
                            return None
                        inferences[other_variable] = inferences.get(other_variable, set())
                        inferences[other_variable].add(other_value)
                        domains[other_variable] = domains[other_variable] - inferences[other_variable]
                if not domains[other_variable]:
                    return None
        return inferences

    def reverseInferences(self, inferences):
        for variable, values in inferences.items():
            self.domains[variable].update(values)

    def countRemainingValues(self, variable):
        return len(self.domains[variable])

    def countUnassignedNeighbors(self, variable, value, assignment):
        count = 0
        for constraint in self.constraints[variable]:
            other_variable = next((v for v in constraint.variables if v != variable), None)
            if other_variable is not None and other_variable not in assignment and value in self.domains[other_variable]:
                count += 1
        return count

def cleanData(data):
    # Remove edges that connect a node to itself
    data[1] = [edge for edge in data[1] if edge[0] != edge[1]]

    # Remove duplicate edges
    data[1] = list(set(tuple(sorted(edge)) for edge in data[1]))

    return data


class MapColoringConstraint(Constraint):
    def __init__(self, place1, place2):
        super().__init__([place1, place2])
        self.place1 = place1
        self.place2 = place2

    def satisfied(self, assignment):
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        return assignment[self.place1] != assignment[self.place2]

def getGraphColoringSolution(data, depth_limit):
    data = cleanData(data)
    variables = []
    edges = data[1]
    for edge in edges:
        if edge[0] not in variables:
            variables.append(edge[0])
        if edge[1] not in variables:
            variables.append(edge[1])
    domain = [i for i in range(data[0])]
    domains = {}
    for variable in variables:
        domains[variable] = domain

    csp = CSP(variables, domains)
    for edge in edges:
        csp.addConstraint(MapColoringConstraint(edge[0], edge[1]))

    solution = None
    if csp.ac3():
        solution = csp.backtrackingSearch({}, depth_limit)

    return solution

def main():
    if len(sys.argv) <= 1:
        return
    else:
        filename = sys.argv[1]
        depth_limit = None
        if len(sys.argv) >= 3:
            depth_limit = int(sys.argv[2])
        if ".txt" in filename:
            if len(sys.argv) < 2:
                return
            else:
                solution = getGraphColoringSolution(getData(filename), depth_limit)
                print("CSP Coloring Solution:")
                if solution is None:
                    print("No Solution has been found")
                else:
                    print("Edge : Color")
                    for edge in solution:
                        print(edge,":",solution[edge])


if __name__ == '__main__':
    main()