package pol;

import pol.environment.AgentMobility;
import pol.environment.BuildingUnit;
import pol.log.Skip;
import pol.log.State;

import java.util.Random;

public class InfectiousModel implements java.io.Serializable {

    @Skip
    private Person agent;
    @State
    private InfectiousStatus status;
    @Skip
    private static int globalNumInfectious;
    @Skip
    private static int globalNumHasBeenExposed;
    @Skip
    private static long totalNumAgents;
    @Skip
    private static int daysSpreading;

    // General Disease Parameters
    @Skip
    private static int minExposed;
    @Skip
    private static int maxExposed;
    @Skip
    private static int minInfectious;
    @Skip
    private static int maxInfectious;
    @Skip
    private static int minRecovered;
    @Skip
    private static int maxRecovered;

    @Skip
    private static double effectWearingMask;
    @Skip
    private static double threWearingMask;

    @Skip
    private static int maxNumOfInfectedAgents;
    @Skip
    private static int maxNumOfDiseaseDays;

    // Count for time in current status
    @Skip
    private int remainingTimeInStatus;

    // Spreading Chances
    @Skip
    private double spreadDegree;
    @Skip
    private double chanceBeInfected;

    // Mask Wearing Parameters
    @Skip
    private boolean isWearingMasks;

    // Outlier Type
    @State
    private OutlierType outlierType;
    @State
    private double outlierDegree;

    // Logging info
    @Skip
    private long infectedByAgentID;
    @Skip
    private String statusChangeTime;
    @Skip
    private String statusChangeLocation;
    @Skip
    private String statusChangeCheckIn;

    // Helper
    @Skip
    private static Random random;

    // Spread
    public static void spreadDiseaseAgentToAgent(Person des, Person src) {
        double chance = des.getChanceBeInfected() * src.getSpreadDegree();
        if (chance == 0)
            return;
        if (random.nextDouble() < chance) {
            des.beenExposed(src);
        }
    }

    public static void spreadDiseasePlaceToAgent(Person des, BuildingUnit src) {
        double chance = des.getChanceBeInfected() * src.getSpreadDegree();
        if (chance == 0)
            return;
        if (random.nextDouble() < chance) {
            des.beenExposed(src);
        }

    }

    public static void initCountOfDay(){
        if (daysSpreading <= 0) daysSpreading = 1;
    }

    public static void incrementDaysSpreading() {
        if (daysSpreading <= 0)
            return;
        daysSpreading++;
        if (maxNumOfDiseaseDays > 0 && daysSpreading > maxNumOfDiseaseDays) {
            LoveNeed.stopAgentToAgentSpread();
            AgentMobility.stopPlaceToAgentSpread();
        }
    }

    // Initialize parameters
    public static void initializeGeneralParam(WorldParameters params) {
        globalNumInfectious = 0;
        globalNumHasBeenExposed = 0;

        maxNumOfInfectedAgents = params.maxNumOfInfectedAgents;
        maxNumOfDiseaseDays = params.maxNumOfDiseaseDays;
        daysSpreading = 0;

        String[] splits = params.exposedLasting.split("-");
        try {
            minExposed = Integer.valueOf(splits[0]);
        } catch (Exception ignore) {
            System.err.println("Invalid Exposed Lasting Parameter");
            minExposed = 288;
        }
        try {
            maxExposed = Integer.valueOf(splits[1]);
        } catch (Exception ignore) {
            System.err.println("Invalid Exposed Lasting Parameter");
            maxExposed = 1440;
        }

        splits = params.infectiousLasting.split("-");
        try {
            minInfectious = Integer.valueOf(splits[0]);
        } catch (Exception ignore) {
            System.err.println("Invalid Infectious Lasting Parameter");
            minInfectious = 1440;
        }
        try {
            maxInfectious = Integer.valueOf(splits[1]);
        } catch (Exception ignore) {
            System.err.println("Invalid Infectious Lasting Parameter");
            maxInfectious = 2304;
        }

        splits = params.recoveredLasting.split("-");
        try {
            minRecovered = Integer.valueOf(splits[0]);
        } catch (Exception ignore) {
            System.err.println("Invalid Recovered Lasting Parameter");
            minRecovered = 2016;
        }
        try {
            maxRecovered = Integer.valueOf(splits[1]);
        } catch (Exception ignore) {
            System.err.println("Invalid Recovered Lasting Parameter");
            maxRecovered = 4023;
        }

        effectWearingMask = params.maskEffectivity;
        threWearingMask = params.maskWearingThreshold;
        totalNumAgents = params.numOfAgents;
        random = new Random();
        random.setSeed(params.seed);

    }

    public InfectiousModel() {
        this.agent = null;
        this.status = InfectiousStatus.Susceptible;

        this.remainingTimeInStatus = 0;

        this.spreadDegree = 0;
        this.chanceBeInfected = 0;

        this.isWearingMasks = false;
        this.outlierType = null;
        this.outlierDegree = 0;

        this.infectedByAgentID = -1; // -1 for not yet been infected, self ID for initial random zero-patients
        this.statusChangeTime = null;
        this.statusChangeLocation = null;
        this.statusChangeCheckIn = null;
    }

    public InfectiousModel(Person p) {
        this();
        this.agent = p;
        changeStatus(InfectiousStatus.Susceptible);
    }

    public void initialOutlier(OutlierType outlierType) {
        if (daysSpreading == 0)
            daysSpreading = 1;
        this.outlierType = outlierType;
        changeStatus(InfectiousStatus.Infectious);
        this.infectedByAgentID = agent.getAgentId();
    }

    public void changeStatus(InfectiousStatus newStatus) {
        if (newStatus == InfectiousStatus.Susceptible) {
            this.status = InfectiousStatus.Susceptible;
            this.spreadDegree = 0;
            this.chanceBeInfected = agent.getModel().params.infectionDegreePerStep;
            this.remainingTimeInStatus = 0;
            this.infectedByAgentID = -1; // -1 for not yet been infected, self ID for initial random zero-patients

        } else if (newStatus == InfectiousStatus.Exposed) {
            this.status = InfectiousStatus.Exposed;
            this.spreadDegree = 0;
            this.chanceBeInfected = 0;
            this.remainingTimeInStatus = random.nextInt(maxExposed - minExposed + 1) + minExposed;

            globalNumHasBeenExposed += 1;
            // Stop the spread when # of infectious > *maxNumOfInfectedAgents*
            if (maxNumOfInfectedAgents > 0 && globalNumHasBeenExposed >= maxNumOfInfectedAgents) {
                LoveNeed.stopAgentToAgentSpread();
                AgentMobility.stopPlaceToAgentSpread();
            }

        } else if (newStatus == InfectiousStatus.Infectious) {
            this.status = InfectiousStatus.Infectious;
            this.spreadDegree = agent.getModel().params.spreadDegreePerStep;
            this.chanceBeInfected = 0;
            this.remainingTimeInStatus = random.nextInt(maxInfectious - minInfectious + 1) + minInfectious;

            globalNumInfectious += 1;

            if (this.outlierDegree == 0) {
                this.agent.setOutlierType(this.outlierType);
            } else {
                this.agent.setOutlierType(this.outlierType, this.outlierDegree);
            }

        } else {
            this.status = InfectiousStatus.Recovered;
            this.spreadDegree = 0;
            this.chanceBeInfected = 0;
            this.remainingTimeInStatus = random.nextInt(maxRecovered - minRecovered + 1) + minRecovered;

            globalNumInfectious -= 1;

            this.agent.backToNormal();
        }

        try {
            this.statusChangeTime = this.agent.getSimulationTime().toString();
        } catch (Exception ignore) {
            this.statusChangeTime = null;
        }
        try {
            this.statusChangeLocation = this.agent.getLocation().toString();
        } catch (Exception ignore) {
            this.statusChangeLocation = null;
        }
        try {
            this.statusChangeCheckIn = this.agent.getCurrentMode().toString();
        } catch (Exception ignore) {
            this.statusChangeCheckIn = null;
        }
    }

    public void beenExposed(Person p) {
        this.infectedByAgentID = p.getAgentId();
        this.outlierType = p.getOutlierType();
        changeStatus(InfectiousStatus.Exposed);
    }

    public void beenExposed(BuildingUnit buildingUnit) {
        this.infectedByAgentID = -1;
        this.outlierType = buildingUnit.getOutlierType();
        this.outlierDegree = buildingUnit.getOutlierDegree();
        changeStatus(InfectiousStatus.Exposed);
    }

    public void wearingMask() {
        double infectedPercentage = (double) globalNumInfectious / (double) totalNumAgents;
        if (infectedPercentage <= threWearingMask) {
            this.isWearingMasks = false;
            return;
        }
        double chanceWearing = (threWearingMask >= 1) ? 0
                : (infectedPercentage - threWearingMask) / (1 - threWearingMask);
        this.isWearingMasks = random.nextDouble() < chanceWearing;
    }

    public double getSpreadDegree() {
        if (this.isWearingMasks)
            return (1 - effectWearingMask) * this.spreadDegree;
        return this.spreadDegree;
    }

    public double getChanceBeInfected() {
        if (this.isWearingMasks)
            return (1 - effectWearingMask) * this.chanceBeInfected;
        return this.chanceBeInfected;
    }

    public InfectiousStatus getStatus() {
        return this.status;
    }

    public void nextStep() {
        if (this.status == InfectiousStatus.Susceptible)
            return;

        this.remainingTimeInStatus--;
        if (this.remainingTimeInStatus > 0)
            return;
        if (this.status == InfectiousStatus.Exposed) {
            changeStatus(InfectiousStatus.Infectious);
        } else if (this.status == InfectiousStatus.Infectious) {
            changeStatus(InfectiousStatus.Recovered);
        } else if (this.status == InfectiousStatus.Recovered) {
            changeStatus(InfectiousStatus.Susceptible);
        }
    }

    // Logging Functions
    public String getStatusChangeTime() {
        return this.statusChangeTime;
    }

    public String getStatusChangeLocation() {
        return this.statusChangeLocation;
    }

    public String getStatusChangeCheckIn() {
        return this.statusChangeCheckIn;
    }

    public long getInfectedByAgentID() {
        return this.infectedByAgentID;
    }
}
