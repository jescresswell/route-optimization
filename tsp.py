from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
import numpy as np
import pandas as pd
import os

# Distance callback
class CreateDistanceCallback(object):
  """Create callback to calculate distances between points."""
  def __init__(self,fname):
    """Array of distances between points."""

    data = pd.read_csv('./manifests/'+fname+'_dmatrix.csv',header= None)
    self.matrix= data.values.tolist()



  def Distance(self, from_node, to_node):
    return self.matrix[from_node][to_node]
def main():

  fname = '243884' #Automate this later..

  os.system('java -jar dmatrix.jar ./manifests/'+fname +'.csv')

  df = pd.read_csv('./manifests/'+fname+'.csv')
  city_names = df['Address'][:]
  lats = df['Latitude'][:]
  lons = df['Longitude'][:]


  tsp_size = len(df)

  # Create routing model
  if tsp_size > 0:
    # TSP of size tsp_size
    # Second argument = 1 to build a single tour (it's a TSP).
    # Nodes are indexed from 0 to tsp_size - 1. By default the start of
    # the route is node 0.
    routing = pywrapcp.RoutingModel(tsp_size, 1, 0) #had to add depot index
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()

    # Setting first solution heuristic: the
    # method for finding a first solution to the problem.
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Create the distance callback, which takes two arguments (the from and to node indices)
    # and returns the distance between these nodes.

    dist_between_nodes = CreateDistanceCallback(fname)
    dist_callback = dist_between_nodes.Distance
    routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
    # Solve, returns a solution if any.
    assignment = routing.SolveWithParameters(search_parameters)
    if assignment:
      # Solution cost.
      print "Total distance: " + str(assignment.ObjectiveValue()) + " meters\n"
      # Inspect solution.
      # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1


      leadingurl = 'http://localhost:8989/?point='
      trailingurl = '&locale=en-US&vehicle=car&weighting=fastest&elevation=false&use_miles=false&layer=Omniscale'
      urlspace = '%2C'
      urlnext = '&point='
      theurl = leadingurl

      route_number = 0
      index = routing.Start(route_number)  # Index of the variable for the starting node.
      route = ''

      while not routing.IsEnd(index):
        # Convert variable indices to node indices in the displayed route.
        route += str(city_names[routing.IndexToNode(index)]) + ' -> '
        theurl += str(lats[routing.IndexToNode(index)]) + urlspace + str(lons[routing.IndexToNode(index)]) + urlnext
        index = assignment.Value(routing.NextVar(index))
      route += str(city_names[routing.IndexToNode(index)])
      theurl += str(lats[routing.IndexToNode(index)]) + urlspace + str(lons[routing.IndexToNode(index)])
      print "Route:\n\n" + route
      print theurl + trailingurl



    else:
      print 'No solution found.'
  else:
    print 'Specify an instance greater than 0.'

if __name__ == '__main__':
  main()