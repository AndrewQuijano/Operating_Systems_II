package ml.classifier;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.Arrays;

import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.bayes.BayesNet;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.bayes.NaiveBayesMultinomial;
import weka.classifiers.bayes.NaiveBayesMultinomialUpdateable;
import weka.classifiers.bayes.NaiveBayesUpdateable;
import weka.classifiers.bayes.net.BIFReader;
import weka.classifiers.bayes.net.BayesNetGenerator;
import weka.classifiers.bayes.net.EditableBayesNet;
import weka.classifiers.evaluation.NominalPrediction;
import weka.classifiers.evaluation.Prediction;
import weka.classifiers.functions.GaussianProcesses;
import weka.classifiers.functions.LinearRegression;
import weka.classifiers.functions.Logistic;
import weka.classifiers.functions.MultilayerPerceptron;
import weka.classifiers.functions.SGD;
import weka.classifiers.functions.SGDText;
import weka.classifiers.functions.SMO;
import weka.classifiers.functions.SMOreg;
import weka.classifiers.functions.SimpleLinearRegression;
import weka.classifiers.functions.SimpleLogistic;
import weka.classifiers.functions.VotedPerceptron;
import weka.classifiers.lazy.IBk;
import weka.classifiers.lazy.KStar;
import weka.classifiers.lazy.LWL;
import weka.classifiers.meta.AdaBoostM1;
import weka.classifiers.meta.AdditiveRegression;
import weka.classifiers.meta.AttributeSelectedClassifier;
import weka.classifiers.meta.Bagging;
import weka.classifiers.meta.CVParameterSelection;
import weka.classifiers.meta.ClassificationViaRegression;
import weka.classifiers.meta.CostSensitiveClassifier;
import weka.classifiers.meta.FilteredClassifier;
import weka.classifiers.meta.IterativeClassifierOptimizer;
import weka.classifiers.meta.LogitBoost;
import weka.classifiers.meta.MultiClassClassifier;
import weka.classifiers.meta.MultiClassClassifierUpdateable;
import weka.classifiers.meta.MultiScheme;
import weka.classifiers.meta.RandomCommittee;
import weka.classifiers.meta.RandomSubSpace;
import weka.classifiers.meta.RandomizableFilteredClassifier;
import weka.classifiers.meta.RegressionByDiscretization;
import weka.classifiers.meta.Stacking;
import weka.classifiers.meta.Vote;
import weka.classifiers.meta.WeightedInstancesHandlerWrapper;
import weka.classifiers.misc.InputMappedClassifier;
import weka.classifiers.misc.SerializedClassifier;
import weka.classifiers.rules.DecisionTable;
import weka.classifiers.rules.JRip;
import weka.classifiers.rules.OneR;
import weka.classifiers.rules.PART;
import weka.classifiers.rules.ZeroR;
import weka.classifiers.trees.DecisionStump;
import weka.classifiers.trees.HoeffdingTree;
import weka.classifiers.trees.J48;
import weka.classifiers.trees.LMT;
import weka.classifiers.trees.M5P;
import weka.classifiers.trees.REPTree;
import weka.classifiers.trees.RandomForest;
import weka.classifiers.trees.RandomTree;
import weka.classifiers.trees.lmt.LogisticBase;
import weka.core.Instances;
import weka.core.converters.ArffLoader;
import weka.core.SerializationHelper;

public class WekaClassifiers
{
	private static Classifier [] models = { 
			//new J48(), 				// a decision tree
			//new AdaBoostM1(),
			//new BayesNet()
			//new DecisionTable(),	//decision table majority classifier
			//new DecisionStump(),	//one-level decision tree
			//new Logistic(),
			//new LibSVM(),
			new RandomForest()
	};
	
	public static void init()
	{
		ArrayList<Classifier> c = new ArrayList<Classifier>();
		//c.add(new AbstractClassifier());
		c.add(new AdaBoostM1());
		c.add(new AdditiveRegression());
		c.add(new AttributeSelectedClassifier());
		c.add(new Bagging());
		c.add(new BayesNet());
		c.add(new BayesNetGenerator());
		c.add(new BIFReader());
		c.add(new ClassificationViaRegression());
		c.add(new CostSensitiveClassifier());
		c.add(new CVParameterSelection());
		c.add(new DecisionStump());
		c.add(new DecisionTable());
		c.add(new EditableBayesNet()); 
		c.add(new FilteredClassifier());
		c.add(new GaussianProcesses());
		//c.add(new GeneralRegression()); 
		c.add(new HoeffdingTree());
		c.add(new IBk());
		c.add(new InputMappedClassifier());
		//c.add(new IteratedSingleClassifierEnhancer());
		c.add(new IterativeClassifierOptimizer());
		c.add(new J48());
		c.add(new JRip());
		c.add(new KStar());
		c.add(new LinearRegression()); 
		c.add(new LMT());
		//c.add(new LMTNode()); 
		c.add(new Logistic());
		c.add(new LogisticBase());
		c.add(new LogitBoost());
		c.add(new LWL());
		//c.add(new M5Base()); 
		c.add(new M5P());
		//c.add(new M5Rules()); 
		c.add(new MultiClassClassifier());
		c.add(new MultiClassClassifierUpdateable());
		c.add(new MultilayerPerceptron());
		//c.add(new MultipleClassifiersCombiner());
		c.add(new MultiScheme());
		c.add(new NaiveBayes());
		c.add(new NaiveBayesMultinomial());
		//c.add(new NaiveBayesMultinomialText());
		c.add(new NaiveBayesMultinomialUpdateable());
		c.add(new NaiveBayesUpdateable());
		c.add(new OneR());
		//c.add(new ParallelIteratedSingleClassifierEnhancer());
		//c.add(new ParallelMultipleClassifiersCombiner());
		c.add(new PART());
		//c.add(new PMMLClassifier()); 
		//c.add(new PreConstructedLinearModel());
		c.add(new RandomCommittee()); 
		c.add(new RandomForest());
		//c.add(new RandomizableClassifier()); 
		c.add(new RandomizableFilteredClassifier());
		/*
		c.add(new RandomizableIteratedSingleClassifierEnhancer());
		c.add(new RandomizableMultipleClassifiersCombiner());
		c.add(new RandomizableParallelIteratedSingleClassifierEnhancer());
		c.add(new RandomizableParallelMultipleClassifiersCombiner());
		c.add(new RandomizableSingleClassifierEnhancer());
		*/
		c.add(new RandomSubSpace());
		c.add(new RandomTree());
		//c.add(new Regression());
		c.add(new RegressionByDiscretization());
		c.add(new REPTree()); 
		//c.add(new RuleNode());
		//c.add(new RuleSetModel()); 
		c.add(new SerializedClassifier());
		c.add(new SGD());
		c.add(new SGDText());
		c.add(new SimpleLinearRegression());
		c.add(new SimpleLogistic());
		//c.add(new SingleClassifierEnhancer());
		c.add(new SMO());
		c.add(new SMOreg());
		c.add(new Stacking());
		//c.add(new SupportVectorMachineModel());
		//c.add(new TreeModel());
		c.add(new Vote());
		c.add(new VotedPerceptron());
		c.add(new WeightedInstancesHandlerWrapper());
		c.add(new ZeroR());
		models = c.toArray(new Classifier[c.size()]);
	}
	/*
	private static Classifier [] all_models = { 
			AbstractClassifier, 
			AdaBoostM1, 
			AdditiveRegression, 
			AttributeSelectedClassifier, 
			Bagging, 
			BayesNet,
			BayesNetGenerator, 
			BIFReader, 
			ClassificationViaRegression,
			CostSensitiveClassifier,
			CVParameterSelection, 
			DecisionStump, 
			DecisionTable, 
			EditableBayesNet, 
			FilteredClassifier, 
			GaussianProcesses, 
			GeneralRegression, 
			HoeffdingTree, 
			IBk, 
			InputMappedClassifier,
			IteratedSingleClassifierEnhancer, 
			IterativeClassifierOptimizer, 
			J48, 
			JRip,
			KStar, 
			LinearRegression, 
			LMT,
			LMTNode, 
			Logistic, 
			LogisticBase, 
			LogitBoost, 
			LWL, 
			M5Base, 
			M5P, 
			M5Rules, 
			MultiClassClassifier, 
			MultiClassClassifierUpdateable, 
			MultilayerPerceptron, 
			MultipleClassifiersCombiner, 
			MultiScheme, 
			NaiveBayes, 
			NaiveBayesMultinomial, 
			NaiveBayesMultinomialText, 
			NaiveBayesMultinomialUpdateable,
			NaiveBayesUpdateable, 
			OneR, 
			ParallelIteratedSingleClassifierEnhancer, 
			ParallelMultipleClassifiersCombiner, 
			PART, 
			PMMLClassifier, 
			PreConstructedLinearModel, 
			RandomCommittee, 
			RandomForest, 
			RandomizableClassifier, 
			RandomizableFilteredClassifier, 
			RandomizableIteratedSingleClassifierEnhancer,
			RandomizableMultipleClassifiersCombiner, 
			RandomizableParallelIteratedSingleClassifierEnhancer, 
			RandomizableParallelMultipleClassifiersCombiner, 
			RandomizableSingleClassifierEnhancer, 
			RandomSubSpace, 
			RandomTree, 
			Regression, 
			RegressionByDiscretization, 
			REPTree, 
			RuleNode, 
			RuleSetModel, 
			SerializedClassifier, 
			SGD, 
			SGDText, 
			SimpleLinearRegression,
			SimpleLogistic, 
			SingleClassifierEnhancer, 
			SMO, 
			SMOreg, 
			Stacking, 
			SupportVectorMachineModel, 
			TreeModel, 
			Vote, 
			VotedPerceptron, 
			WeightedInstancesHandlerWrapper, 
			ZeroR
	};
	*/
	
	private static int NUM_CLASSIFIERS = models.length;
 
	public static Evaluation classify(Classifier model,
			Instances trainingSet, Instances testingSet) throws Exception 
	{
		Evaluation evaluation = new Evaluation(trainingSet);
		model.buildClassifier(trainingSet);
		evaluation.evaluateModel(model, testingSet);
		return evaluation;
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
		// Load Training Data
		//Instances training_data = read_arff_file("C:\\Users\\Andrew\\Desktop\\iris.arff");
		Instances training_data = read_arff_file("C:\\Users\\Andrew\\Desktop\\NSL-KDD\\KDDTrain+.arff");
		Instances test_data = read_arff_file("C:\\Users\\Andrew\\Desktop\\NSL-KDD\\KDDTest+.arff");
		
		// Cross Validate each one
		Evaluation [] evals = new Evaluation[NUM_CLASSIFIERS];
		
		for (int i = 0; i < NUM_CLASSIFIERS; i++)
		{
			// Set up evaluation
			evals[i] = new Evaluation(training_data);
			
			// set tuning parameters
			CVParameterSelection hi = new CVParameterSelection();
			hi.setClassifier(models[i]);
			hi.setNumFolds(10);
			/*
			String [] o = {"-P P 90 100 2"};
			System.out.println(o[0]);
			hi.setOptions(o);
			*/
			hi.addCVParameter("P 90 110 21");

			long start = System.currentTimeMillis();
			hi.buildClassifier(training_data);
			// Get elapsed time in milliseconds
			long elapsedTimeMillis = System.currentTimeMillis()-start;
			// Get elapsed time in seconds
			double elapsedTimeSec = elapsedTimeMillis/1000.0;
			System.out.println("Time to train in seconds: " + elapsedTimeSec);
			
		    /*
		    	cvParam - the string representation of a scheme parameter. The format is:
				param_char lower_bound upper_bound number_of_steps
				eg to search a parameter -N from 1 to 10 by increments of 1:
				N 1 10 11 
		    */ 
		   
			// write classifier to file
		    System.out.println(models[i].getClass().getSimpleName());
		    writeClassifier(models[i].getClass().getSimpleName() + ".model", hi);
		    
		    // print CV
		    String [] x = hi.getBestClassifierOptions();
		    for (int j = 0; j < x.length; j++)
		    {
		    	System.out.println(x[j]);;
		    }
		   
		    // Get test score 
		    evals[i].evaluateModel(hi, test_data);
			System.out.println(evals[i].pctCorrect());
			double [][] cf = evals[i].confusionMatrix();
			for (double [] row : cf)
			{
				System.out.println(Arrays.toString(row));
			}
		}
		
		// Get Results
		for (int i = 0; i < evals.length; i++)
		{
			System.out.println(evals[i].toSummaryString());
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
    
    public static Classifier loadClassifier(String path) throws Exception
    {
    	Classifier cls = (Classifier) SerializationHelper.read(path);
    	return cls;
    }
}