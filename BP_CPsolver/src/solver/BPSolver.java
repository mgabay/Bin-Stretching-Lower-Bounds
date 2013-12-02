/*
* Copyright or © or Copr. Michaël Gabay (2013)
*
* michael [dot] gabay [at] g-scop.grenoble-inp.fr
*
* This software is a computer program whose purpose is to be
* a proof of concept on using game theoretical approaches to prove
* lower bounds on online packing and scheduling problems.
*
* This software is governed by the CeCILL license under French law and
* abiding by the rules of distribution of free software.  You can  use,
* modify and/ or redistribute the software under the terms of the CeCILL
* license as circulated by CEA, CNRS and INRIA at the following URL
* "http://www.cecill.info".
*
* As a counterpart to the access to the source code and  rights to copy,
* modify and redistribute granted by the license, users are provided only
* with a limited warranty  and the software's author,  the holder of the
* economic rights,  and the successive licensors  have only  limited
* liability.
*
* In this respect, the user's attention is drawn to the risks associated
* with loading,  using,  modifying and/or developing or reproducing the
* software by the user in light of its specific status of free software,
* that may mean  that it is complicated to manipulate,  and  that  also
* therefore means  that it is reserved for developers  and  experienced
* professionals having in-depth computer knowledge. Users are therefore
* encouraged to load and test the software's suitability as regards their
* requirements in conditions enabling the security of their systems and/or
* data to be ensured and,  more generally, to use and operate it in the
* same conditions as regards security.
*
* The fact that you are presently reading this means that you have had
* knowledge of the CeCILL license and that you accept its terms.
*/

package solver;
import choco.Choco;
import choco.Options;
import choco.cp.model.CPModel;
import choco.cp.solver.CPSolver;
import choco.kernel.model.constraints.pack.PackModel;


public class BPSolver {

    int [] items;
    int numBins;
    int capacity;

    CPModel mod;
    CPSolver solver;

    public BPSolver(int[] items, int numBins, int capacity) {
        reset(items, numBins, capacity);
    }

    public void reset(int[] items, int numBins, int capacity) {
        this.items = items;
        this.numBins = numBins;
        this.capacity = capacity;
        mod = null;
        solver = null;
    }

    public void setItems(int[] items) {
        this.items = items;
    }

    public void setNumBins(int numBins) {
        this.numBins = numBins;
    }

    public void setCapacity(int capacity) {
        this.capacity = capacity;
    }

    public void makeModel() {
        mod = new CPModel();
        PackModel pack = new PackModel(items, numBins, capacity);
        // we apply all packing options
        mod.addConstraint(Choco.pack(pack,
                Options.C_PACK_AR, Options.C_PACK_DLB,Options.C_PACK_FB, Options.C_PACK_LBE));
    }

    public void solve() {
        if (mod == null) makeModel();
        solver = new CPSolver();
        solver.read(mod);
        solver.solve();
    }

    public boolean isFeasible() {
        if (items == null) return capacity >= 0 && numBins >= 0;
        makeModel();
        solve();

        return solver.isFeasible();
    }
}
