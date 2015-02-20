'''by steve molin'''

def recursiveDependencies(n):
  '''given a node, find all upstream nodes. nb: does not eliminate duplicates'''
  thisDependencies = n.dependencies()
  if not thisDependencies:
    return []
  dependencyDependencies = []
  for nn in thisDependencies:
    dependencyDependencies.extend(recursiveDependencies(nn))
  return thisDependencies + dependencyDependencies

