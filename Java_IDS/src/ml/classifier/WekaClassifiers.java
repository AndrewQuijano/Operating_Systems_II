package ml.classifier;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.Random;

import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.BayesNet;
import weka.classifiers.evaluation.NominalPrediction;
import weka.classifiers.evaluation.Prediction;
import weka.classifiers.functions.LibSVM;
import weka.classifiers.functions.Logistic;
import weka.classifiers.meta.AdaBoostM1;
import weka.classifiers.meta.CVParameterSelection;
import weka.classifiers.rules.DecisionTable;
import weka.classifiers.rules.PART;
import weka.classifiers.trees.DecisionStump;
import weka.classifiers.trees.J48;
import weka.classifiers.trees.RandomForest;
import weka.core.Instances;
import weka.core.Range;
import weka.core.converters.ArffLoader;
import weka.classifiers.evaluation.output.prediction.PlainText;
import weka.core.SerializationHelper;

public class WekaClassifiers
{
	// Load all NON-Incremental models
	private static Classifier [] models = { 
			//new J48(), 				// a decision tree
			new AdaBoostM1(),
			new BayesNet()
			//new DecisionTable(),	//decision table majority classifier
			//new DecisionStump(),	//one-level decision tree
			//new Logistic(),
			//new LibSVM(),
			//new RandomForest()
	};
	private static int NUM_CLASSIFIERS = models.length;
 
	public static Evaluation classify(Classifier model,
			Instances trainingSet, Instances testingSet) throws Exception 
	{
		Evaluation evaluation = new Evaluation(trainingSet);
		model.buildClassifier(trainingSet);
		evaluation.evaluateModel(model, testingSet);
		return evaluation;
	}
 
	public static double calculateAccuracy(ArrayList<Prediction> predictions) 
	{
		double correct = 0;
		for (int i = 0; i < predictions.size(); i++) 
		{
			NominalPrediction np = (NominalPrediction) predictions.get(i);
			if (np.predicted() == np.actual()) 
			{
				correct++;
			}
		}
		return 100 * correct / predictions.size();
	}
 
	public static Instances[][] crossValidationSplit(Instances data, int numberOfFolds) 
	{
		Instances[][] split = new Instances[2][numberOfFolds];
 
		for (int i = 0; i < numberOfFolds; i++) 
		{
			split[0][i] = data.trainCV(numberOfFolds, i);
			split[1][i] = data.testCV(numberOfFolds, i);
		}
		return split;
	}
	
	public static Instances read_arff_file(String filepath) throws IOException
	{
		ArffLoader loader = new ArffLoader();
		loader.setFile(new File(filepath));
		Instances data = loader.getDataSet();
		data.setClassIndex(data.numAttributes() - 1);
		return data;
	}
	
	public static void main(String[] args) throws Exception 
	{
		/*
		if (args.length == 0)
		{
			// Default
		}
		else if(args.length == 1)
		{
			
		}
		*/
		
		// Load Training Data
		//Instances training_data = read_arff_file("C:\\Users\\Andrew\\Desktop\\iris.arff");
		Instances training_data = read_arff_file("../../../KDDTrain+.arff");
		
		// Cross Validate each one
		Evaluation [] evals = new Evaluation[NUM_CLASSIFIERS];
		
		StringBuffer predictionSB = new StringBuffer();
		Range attributesToShow = null;
		Boolean outputDistributions = new Boolean(true);

		PlainText predictionOutput = new PlainText();
		predictionOutput.setBuffer(predictionSB);
		predictionOutput.setOutputDistribution(true);

		for (int i = 0; i < NUM_CLASSIFIERS; i++)
		{
			evals[i] = new Evaluation(training_data);
			//evals[i].crossValidateModel(models[i], training_data, 10, new Random(1), predictionOutput, attributesToShow, outputDistributions);
			CVParameterSelection hi = new CVParameterSelection();
			hi.setClassifier(models[i]);
			hi.setNumFolds(10);  // using 10-fold CV
		    /*
		    	cvParam - the string representation of a scheme parameter. The format is:
				param_char lower_bound upper_bound number_of_steps
				eg to search a parameter -P from 1 to 10 by increments of 1:
				P 1 10 11 
		     */
		    hi.buildClassifier(training_data);
		    System.out.println(models[i].getClass().getSimpleName());
		    writeClassifier(models[i].getClass().getSimpleName() + ".model", hi);
		    /*
		    String [] x = hi.getBestClassifierOptions();
		    for (int j = 0; j < x.length; j++)
		    {
		    	//System.out.println(x[j]);;
		    }
		    */
		}
		
		// Get Results
		for (int i = 0; i < evals.length; i++)
		{
			//System.out.println(evals[i].toSummaryString());
		}
		
		// Conduct Test Set Evaluations
		
		// Write the classes into object files!
		for (int i = 0; i < evals.length; i++)
		{
			//WriteObjectToFile(models[i], "class"+i+".obj");
			//writeClassifier("", mode);
		}
	}
	
    public static void WriteObjectToFile(Object serObj, String filepath) 
    {	 
        try
        {
        	FileOutputStream fileOut = new FileOutputStream(filepath);
            ObjectOutputStream objectOut = new ObjectOutputStream(fileOut);
            objectOut.writeObject(serObj);
            objectOut.close();
            System.out.println("The Object  was succesfully written to a file");
 
        } 
        catch (Exception ex) 
        {
            ex.printStackTrace();
        }
    }
    
    public static void writeClassifier(String path, Classifier clf) throws Exception
    {
    	SerializationHelper.write(path, clf);
    }
}