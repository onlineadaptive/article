package se.su.dsv.online_concurrent;

import org.openjdk.jmh.infra.Blackhole;
import de.heidelberg.pvs.container_bench.generators.ElementGenerator;
import de.heidelberg.pvs.container_bench.generators.GeneratorFactory;
import de.heidelberg.pvs.container_bench.generators.PayloadType;
import org.openjdk.jmh.annotations.*;
import se.su.dsv.OnlineAdaptiveConcurrentDataStructure;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.NoSuchElementException;
import java.util.concurrent.ConcurrentLinkedDeque;
import java.util.concurrent.ConcurrentLinkedQueue;

public class OnlineConcurrentBench extends AbstractOnlineConcurrentBench{

    private final int generatorSize = 1048576*4;

    @Param
    OnlineConcurrentFact impl;

    String values[];
    ConcurrentLinkedDeque<String> toRemove;

    ElementGenerator<String> valuesGenerator;

    OnlineAdaptiveConcurrentDataStructure<Object> adaptiveList;
    OperationGenerator operations;
    

    @Param("STRING_DICTIONARY")
    PayloadType payloadType;

    @Param("even")
    String testType;

    @Setup(Level.Trial)
    @SuppressWarnings("unchecked")
    public void init() throws  IOException {
        System.out.println("=====Initiating operation distibution: " + testType + "=====");
        switch (testType){
            case "even":
                operations = new OperationGenerator(34,20,33,13);
                break;
            case "iterate":
                operations = new OperationGenerator(0,10,85,5);
                break;
            case "update":
                operations = new OperationGenerator(20, 28, 30, 22);
                break;
            default:
                throw new RuntimeException("Wrong test type: " + testType);
        }
        valuesGenerator = (ElementGenerator<String>) GeneratorFactory.buildRandomGenerator(PayloadType.STRING_UNIFORM);
        valuesGenerator.init(generatorSize, seed);

        values = valuesGenerator.generateArray(generatorSize);
        toRemove = new ConcurrentLinkedDeque<>(Arrays.asList(valuesGenerator.generateArray(size)));

        adaptiveList = impl.maker.get();
        adaptiveList.setup(toRemove.toArray());
        adaptiveList.setThreads(threads);
    }

    @Setup(Level.Iteration)
    @SuppressWarnings("unchecked")
    public void setup(Blackhole bh) throws IOException {
        adaptiveList.stop();
        operations.reset();

        adaptiveList = impl.maker.get();
        toRemove = new ConcurrentLinkedDeque<>(Arrays.asList(valuesGenerator.generateArray(size)));
        adaptiveList.setup(toRemove.toArray());
        adaptiveList.setThreads(threads);
    }


    @Benchmark
    public void operationsRunner(Blackhole bh){
        switch (operations.getOperation()){
            case 1:
                contains(bh);
                break;
            case 2:
                insert();
                break;
            case 3:
                iterate(bh);
                break;
            case 4:
                remove();
                break;
        }

    }

    public void contains(Blackhole bh) {
        int index = valuesGenerator.generateIndex(generatorSize);
        bh.consume(adaptiveList.contains(values[index]));
    }

    // TODO add a dummy operation to simulate the overhead that exist from handling the values queue in add and remove.
    public void insert(){
        String item = values[valuesGenerator.generateIndex(generatorSize)];
        adaptiveList.add(item);
        toRemove.add(item);
    }

    public void iterate(Blackhole bh) {
        for(Object obj: adaptiveList){
            if (Thread.currentThread().isInterrupted())
                break;
            bh.consume(obj);
        }
    }

    public void remove(){
        String item;
        try{
             item = toRemove.pop();
        } catch (NoSuchElementException e) {item = values[valuesGenerator.generateIndex(generatorSize)];}
        adaptiveList.remove(item);
    }
}
