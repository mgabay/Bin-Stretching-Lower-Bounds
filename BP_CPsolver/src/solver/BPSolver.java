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
