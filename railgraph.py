
class RailGraph:
    def __init__(self, file):
        f = open(file,'r')


        self.edges = {}
        for x in f.read().split("\n"):
            a,b = x.split(" ")
            a = int(a)
            b = int(b)
            if a not in self.edges.keys():
                self.edges[a] = [b]
            else:
                self.edges[a].append(b)
            if b not in self.edges.keys():
                self.edges[b] = [a]
            else:
                self.edges[b].append(a)

        f.close()

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.edges.keys():
            return []
        paths = []
        for node in self.edges[start]:
            if node not in path:
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
