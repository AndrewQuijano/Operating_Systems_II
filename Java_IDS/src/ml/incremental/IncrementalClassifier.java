package ml.incremental;

import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ArffLoader;
import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.UpdateableClassifier;
import weka.classifiers.bayes.NaiveBayesMultinomialUpdateable;
import weka.classifiers.bayes.NaiveBayesUpdateable;
import weka.classifiers.functions.SGD;
import weka.classifiers.lazy.IBk;
import weka.classifiers.lazy.KStar;
import weka.classifiers.lazy.LWL;
import weka.classifiers.meta.MultiClassClassifierUpdateable;
import weka.classifiers.trees.HoeffdingTree;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

public class IncrementalClassifier 
{
	private static UpdateableClassifier [] clf;
	private static Evaluation [] evaluation;
	private static int NUM_CLF = clf.length;
	private static final int CAPACITY = 10000;
	
	public static void init()
	{
		ArrayList<UpdateableClassifier> c = new ArrayList<UpdateableClassifier>();
		c.add(new NaiveBayesUpdateable());
		c.add(new HoeffdingTree());
		c.add(new NaiveBayesUpdateable());
		c.add(new HoeffdingTree());
		c.add(new IBk());
		c.add(new KStar());
		c.add(new LWL());
		c.add(new MultiClassClassifierUpdateable());
		c.add(new SGD());
		//c.add(new NaiveBayesMultinomialUpdateable());
		//c.add(new NaiveBayesMultinomialText());
		//c.add(new SGDText());
		clf = c.toArray(new UpdateableClassifier[c.size()]);
		NUM_CLF = clf.length;
		evaluation = new Evaluation[NUM_CLF];
	}
	
	public static void train_incrementally(String filepath) throws Exception
	{
		ArffLoader load = new ArffLoader();
		load.setFile(new File(filepath));
		Instances data = load.getStructure();
		data.setClassIndex(data.numAttributes() - 1);
		Instance current = null;

		for (int i = 0; i < NUM_CLF;i++)
		{
			Classifier x = (Classifier) clf[i];
			x.buildClassifier(data);
			evaluation[i] = new Evaluation(data);
		}
		
		while ((current = load.getNextInstance(data)) != null) 
		{
			for (UpdateableClassifier u: clf)
			{
				u.updateClassifier(current);
			}
		}
	}
	
	public static Instances read_arff_file(String filepath) throws IOException
	{
		ArffLoader loader = new ArffLoader();
		loader.setFile(new File(filepath));
		Instances data = loader.getDataSet();
		data.setClassIndex(data.numAttributes() - 1);
		return data;
	}
	
	// In case I can't read it all in one shot...
	public static Instances read_arff_file_part(String filepath, int start) throws IOException
	{
		ArffLoader loader = new ArffLoader();
		loader.setFile(new File(filepath));
		Instances data = loader.getStructure();
		Instance current = null;
		
		// Do I need to shift my starting index?
		int counter = 0;
		while(counter != start)
		{
			current = loader.getNextInstance(data);
			if (current == null)
			{
				System.err.println("Out of bounds!");
				return null;
			}
			++counter;
		}
		
		// Read my specific amount
		counter = 0;
		while (counter != CAPACITY && (current = loader.getNextInstance(data)) != null)
		{
			data.add(current);
			++counter;
		}
		
		data.setClassIndex(data.numAttributes() - 1);
		return data;
	}
	
	/*
	 * Expects an ARFF file as first argument (class attribute is assumed
	 * to be the last attribute).
	 *
	 * @param args        the commandline arguments
	 * @throws Exception  if something goes wrong
	 */
	public static void main(String[] args) throws Exception 
	{
		init();
		Instances test_data = null;
		try
		{
			test_data = read_arff_file("C:\\Users\\Andrew\\Desktop\\NSL-KDD\\KDDTest+.arff");
			train_incrementally("C:\\Users\\Andrew\\Desktop\\NSL-KDD\\KDDTrain+.arff");
		}
		catch(Exception e)
		{
			
		}
		
		// Get The Training Score of the Model
		for (int i = 0; i < NUM_CLF; i++)
		{
			// Get Test Score
			evaluation[i].evaluateModel((Classifier) clf[i], test_data);
			System.out.println(evaluation[i].pctCorrect());
		}
	}
}