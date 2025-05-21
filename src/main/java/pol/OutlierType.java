package pol;

/**
 * This code is to create a outlier object that has a chance to be a outlier.
 * The outlier object is used in the Person class to determine if a person is a
 * outlier user.
 * 
 * @author: W
 *
 */

public enum OutlierType {
    // Social outlier does suspicious activities at pubs
    // Work outlier does not go to work
    Hunger, Interest, Social, Work, All;

}
