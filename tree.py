class TreeNode(list):

    def __init__(self, iterable=(), **attributes):
        self.attr = attributes
        list.__init__(self, iterable)

    def __repr__(self):
        return '%s(%s, %r)' % (type(self).__name__, list.__repr__(self),
                self.attr)

    def id(self):
        return "n"+str(id(self))


    def dot(self):
        s  = "graph {\n"
        s += self.dot_enc()
        return s + "}\n"

    def dot_enc(self):
        s = self.id()+" [label=\""

        for i,j in self.attr.iteritems():
            s += i+": "+str(j)+"\\n"
        if self.attr:
            s = s[:-2]
        s += "\"];\n"

        for i in self:
            s += self.id()+" -- "+i.id()+";\n"
            s += i.dot_enc()

        return s

