package pol;

import java.util.Random;

import pol.log.Skip;
import pol.log.State;

/**
 * This code is to create a outlier object that has a chance to be a outlier.
 * The outlier object is used in the Person class to determine if a person is a
 * outlier user.
 * 
 * @author: W
 *
 */

public class Outlier implements java.io.Serializable {

    @Skip
    private static final double RED_OUTLIER_DEGREE = 1.0;
    @Skip
    private static final double ORANGE_OUTLIER_DEGREE = 0.5;
    @Skip
    private static final double YELLOW_OUTLIER_DEGREE = 0.2;

    // General Outlier Parameters
    @Skip
    private static double chanceToBeYellow;
    @Skip
    private static double chanceToBeOrange;
    @Skip
    private static double chanceToBeRed;

    @Skip
    private Person agent;
    @State
    private double outlierDegree;
    @Skip
    private Random random;
    @State
    private OutlierType type;

    @Skip
    private int stepToChangeInterest;
    @Skip
    private int remainingStepToChangeInterest;

    public static void initializeParameters(WorldParameters params) {
        chanceToBeYellow = params.chanceToBeYellow;
        chanceToBeOrange = params.chanceToBeOrange;
        chanceToBeRed = params.chanceToBeRed;
    }

    public Outlier() {
        this.agent = null;
        this.outlierDegree = 0;
        this.random = new Random();
        this.type = null;
        this.stepToChangeInterest = 0;
        this.remainingStepToChangeInterest = 0;
    }

    public Outlier(Person agent) {
        this();
        this.agent = agent;
    }

    public Outlier(Person agent, double outlierDegree) {
        this(agent);
        this.outlierDegree = outlierDegree;
    }

    public OutlierType getType() {
        return type;
    }

    public void setType(OutlierType type) {
        double degree = 0;
        double maxChance = chanceToBeYellow + chanceToBeOrange + chanceToBeRed;
        if (maxChance == 0) {
            return;
        }
        double val = random.nextDouble() * (maxChance);
        if (val < chanceToBeYellow) {
            degree = YELLOW_OUTLIER_DEGREE;
        } else if (val < chanceToBeYellow + chanceToBeOrange) {
            degree = ORANGE_OUTLIER_DEGREE;
        } else if (val < maxChance) {
            degree = RED_OUTLIER_DEGREE;
        }

        this.setType(type, degree);
    }

    public void setType(String type, double degree) {
        OutlierType convertedType = OutlierType.valueOf(type);
        this.setType(convertedType, degree);
    }

    public void setType(OutlierType type, double degree) {
        this.type = type;
        this.outlierDegree = degree;

        if (this.type == OutlierType.Hunger) {
            if (this.outlierDegree == YELLOW_OUTLIER_DEGREE) {
                agent.getFoodNeed().changeKeepingFullTimeInMinutes(0.75);
                agent.getFoodNeed().changeFullnessDecreasePerStep(1.5);
            } else if (this.outlierDegree == ORANGE_OUTLIER_DEGREE) {
                agent.getFoodNeed().changeKeepingFullTimeInMinutes(0.5);
                agent.getFoodNeed().changeFullnessDecreasePerStep(2);
            } else if (this.outlierDegree == RED_OUTLIER_DEGREE) {
                agent.getFoodNeed().changeKeepingFullTimeInMinutes(0);
                agent.getFoodNeed().changeFullnessDecreasePerStep(3);
            }

        } else if (this.type == OutlierType.Interest) {
            if (this.outlierDegree == YELLOW_OUTLIER_DEGREE) {
                this.stepToChangeInterest = 7;
            } else if (this.outlierDegree == ORANGE_OUTLIER_DEGREE) {
                this.stepToChangeInterest = 2;
            } else if (this.outlierDegree == RED_OUTLIER_DEGREE) {
                this.stepToChangeInterest = 1;
            }
            this.remainingStepToChangeInterest = this.stepToChangeInterest;
        }
    }

    public void backToNormal() {
        if (this.type == OutlierType.Hunger)
            this.agent.getFoodNeed().resetOutlierAppetite();
        this.type = null;
        this.outlierDegree = 0;
        this.stepToChangeInterest = 0;
        this.remainingStepToChangeInterest = 0;
    }

    public void setType(String outlierType) {
        this.type = OutlierType.valueOf(outlierType);
    }

    public double getOutlierDegree() {
        return outlierDegree;
    }

    public void setOutlierDegree(double outlierDegree) {
        this.outlierDegree = outlierDegree;
    }

    /**
     * This method is to generate a random number between 0 and max. The max should
     * be the size of the list that you want to use this method for.
     * 
     * @param max the size of the list that you want to use this method for.
     * @return a random number between 0 and max.
     */
    public int getRandomIndex(int max) {
        return random.nextInt(max);
    }

    /**
     * This method is to determine if a person is a outlier user. Every call to this
     * method will generate different result. The chance to be a outlier user is
     * determined by the outlierDegree variable. If you want to do an action
     * based on the result of this method in different places, you should call this
     * method once and save the result in a variable.
     * 
     * @return true if the person is a outlier user, false otherwise.
     */
    public boolean isActiveRightNow() {
        return random.nextDouble() < this.outlierDegree;
    }

    public void update() {
        if (this.type != OutlierType.Interest)
            return;
        this.remainingStepToChangeInterest--;
        if (this.remainingStepToChangeInterest == 0) {
            agent.shiftInterest();
            this.remainingStepToChangeInterest = this.stepToChangeInterest;
        }
    }

}
