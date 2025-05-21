
package pol;

import java.util.*;

class Z {

    public static int getIndex(int length, int inIndex) {

        int outIndex = 0;
        if (inIndex < 0) {
            outIndex = length + inIndex;

        } else if (inIndex >= 0) {
            outIndex = inIndex;
        }

        if (outIndex < 0) {
            outIndex = 0;
        } else if (outIndex >= length) {
            outIndex = length - 1;
        }

        return outIndex;
    }

    public static void main(String[] args) {
        List<CT> list = new ArrayList<>();
        list.add(new CT(2, 2.0));
        list.add(new CT(1, 1.0));
        list.add(new CT(4, 1.0));
        list.add(new CT(3, 3.0));
        list.add(new CT(6, 1.0));
        list.add(new CT(5, 5.0));

        list.sort((CT o1, CT o2) -> {
            if (o1.getValue() == o2.getValue()) {
                return Long.compare(o1.getId(), o2.getId());
            }

            return Double.compare(o1.getValue(), o2.getValue());
        });

        for (CT ct : list) {
            System.out.println(ct.getId() + " " + ct.getValue());
        }

        System.out.println(list.get(Z.getIndex(list.size(), 66)).getId());

    }

}

class CT {
    private long id;
    private double value;

    public CT() {
        this.id = 0;
        this.value = 0.0;
    }

    public CT(long id) {
        this.id = id;
        this.value = 0.0;
    }

    public CT(long id, double value) {
        this.id = id;
        this.value = value;
    }

    public long getId() {
        return id;
    }

    public double getValue() {
        return value;
    }

    public void setId(long id) {
        this.id = id;
    }

    public void setValue(double value) {
        this.value = value;
    }
}