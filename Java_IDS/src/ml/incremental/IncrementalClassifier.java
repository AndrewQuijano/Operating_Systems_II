package ml.incremental;

import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ArffLoader;
import weka.classifiers.bayes.NaiveBayesUpdateable;

import java.io.File;

/**
 * This example trains NaiveBayes incrementally on data obtained
 * from the ArffLoader.
 *
 * @author FracPete (fracpete at waikato dot ac dot nz)
 */
public class IncrementalClassifier 
{
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
		ArffLoader loader = new ArffLoader();
		loader.setFile(new File(args[0]));
		Instances structure = loader.getStructure();
		structure.setClassIndex(structure.numAttributes() - 1);

		// train NaiveBayes
		NaiveBayesUpdateable nb = new NaiveBayesUpdateable();
	    /*
	     * List of all updatable classifiers
	     * 
	     * 1- HoeffdingTree, 
	     * 2- IBk 
	     * 3- KStar
	     * 4- LWL 
	     * 5- MultiClassClassifierUpdateable
	     * 6- NaiveBayesMultinomialText
	     * 7- NaiveBayesMultinomialUpdateable
	     * 8- NaiveBayesUpdateable
	     * 9- SGD
	     * 10- SGDText
	     */
		
		nb.buildClassifier(structure);
		Instance current;
		while ((current = loader.getNextInstance(structure)) != null)
		{
			nb.updateClassifier(current);
		}
		// output generated model
		System.out.println(nb);
	}
}