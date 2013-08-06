package solver;

import py4j.GatewayServer;

public class BPSolverEntryPoint {

	private BPSolver bps;

    public BPSolverEntryPoint() {
    	bps = new BPSolver(null, 0, 0);
    }

    public BPSolver getSolver() {
        return bps;
    }

    public static void main(String[] args) {
        GatewayServer gatewayServer = new GatewayServer(new BPSolverEntryPoint());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }

}
