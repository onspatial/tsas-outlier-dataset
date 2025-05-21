package pol;

/**
 * General description_________________________________________________________
 * An enumeration to represent agent interests. Letters from A to J represents
 * unique interests while NA represents no interest.
 * 
 * @author Hamdi Kavak (hkavak at gmu.edu), Hossein Amiri (hamiri at emory edu)
 * 
 */
public enum AgentInterest {
	NA(0), A(1), B(2), C(3), D(4), E(5), F(6), G(7), H(8), I(9), J(10);

	private int index;
	private static final int lengthOfAgentInterestEnum = 11; // any change in the enum should be reflected here

	private static int modularAgentInterestEnum(int index) {
		index = index % lengthOfAgentInterestEnum;
		return index;
	}

	private AgentInterest(int index) {
		this.index = modularAgentInterestEnum(index);
	}

	public static AgentInterest valueOf(int index) {
		index = modularAgentInterestEnum(index);

		for (AgentInterest b : AgentInterest.values()) {
			if (b.index == index)
				return b;
		}
		return null;
	}

	public int getValue() {
		return index;
	}
}