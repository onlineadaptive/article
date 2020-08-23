package se.su.dsv.online_concurrent;

import java.util.ArrayList;
import java.util.Collections;
import java.util.concurrent.atomic.AtomicInteger;

public class OperationGenerator {
    private AtomicInteger index;
    private ArrayList<Integer> operationSequence;

    public OperationGenerator(int lookupPercentage, int insertPercentage, int forEachPercentage, int removePercentage) {
        operationSequence = new ArrayList<>();
        index = new AtomicInteger(0);
        for (int i = 0; i < lookupPercentage; i++)
            operationSequence.add(1);

        for (int i = 0; i < insertPercentage; i++)
            operationSequence.add(2);

        for(int i = 0; i< forEachPercentage; i++)
            operationSequence.add(3);

        for (int i = 0; i < removePercentage; i++)
            operationSequence.add(4);

        Collections.shuffle(operationSequence);
    }

    public int getOperation(){
        return operationSequence.get((index.getAndIncrement())%100);
    }

    public void reset(){
        index.set(0);
    }
}
