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
//import weka.classifiers.bayes.NaiveBayesMultinomialText;
//import weka.classifiers.functions.SGDText;
import weka.classifiers.lazy.IBk;
import weka.classifiers.lazy.KStar;
import weka.classifiers.lazy.LWL;
import weka.classifiers.meta.MultiClassClassifierUpdateable;
import weka.classifiers.trees.HoeffdingTree;

import java.io.File;
import java.io.IOException;

public class IncrementalClassifier 
{
	private static UpdateableClassifier [] clf =
	{
		new NaiveBayesUpdateable(), 
		new HoeffdingTree(),
		new IBk(), 
		new KStar(), 
		new LWL(), 
		new MultiClassClassifierUpdateable(),
		new SGD()
	};
	// new NaiveBayesMultinomialUpdateable(), 
	// new NaiveBayesMultinomialText(),
	// new SGDText()
	private static final int NUM_CLF = clf.length;
	private static Evaluation [] evaluation = new Evaluation[NUM_CLF];
	private static final int CAPACITY = 10000;
	
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
		// load data
		Instances training_data = null;
		Instances test_data = null;
		try
		{
			training_data = read_arff_file_part("C:\\Users\\Andrew\\Desktop\\NSL-KDD\\KDDTrain+.arff", 0);
			test_data = read_arff_file("C:\\Users\\Andrew\\Desktop\\NSL-KDD\\KDDTest+.arff");
		}
		catch(IOException io)
		{
			
		}
		
		ArffLoader load = new ArffLoader();
		load.setFile(new File("C:\\Users\\Andrew\\Desktop\\NSL-KDD\\KDDTrain+.arff"));
		Instances data = load.getStructure();
		data.setClassIndex(data.numAttributes() - 1);
		Instance current = null;

		for (int i = 0; i < NUM_CLF;i++)
		{
			for (UpdateableClassifier u: clf)
			{
				Classifier x = (Classifier) u;
				x.buildClassifier(data);
			}
		}
		
		while ((current = load.getNextInstance(data)) != null) 
		{
			for (UpdateableClassifier u: clf)
			{
				u.updateClassifier(current);
			}
		}
		
		// Get The Training Score of the Model
		for (int i = 0; i < NUM_CLF; i++)
		{
			evaluation[i] = new Evaluation(data);
			// Get Test Score
			evaluation[i].evaluateModel((Classifier) clf[i], test_data);
			double incorrect = evaluation[i].incorrect()/test_data.size();
			System.out.println(1.0 - incorrect);
		}
	}
}