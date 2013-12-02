##########################################################################
# Copyright or © or Copr. Michaël Gabay (2013)
#
# michael [dot] gabay [at] g-scop.grenoble-inp.fr
#
# This software is a computer program whose purpose is to be
# a proof of concept on using game theoretical approaches to prove
# lower bounds on online packing and scheduling problems.
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
##########################################################################

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

