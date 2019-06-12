package nids.kddpreprocessor;

public class StatsPerHost {
	
	//StatsperHost.h
	private FeatureUpdater feature_updater;	// Used to update features in ConversationFeatures object

	// 23/32: Number of conversations to same destination IP
	private int count;				

	// 25/38: Number of conversations that have activated the flag
	// S0, S1, S2 or S3 among conv. in count (23/32)
	private int serror_count;		

	// 27/40: Number of conversations that have activated the flag REJ among 
	// conv. in count (23/32)
	private int rerror_count;		
	
	// 29/34 : Number of conversations for each service (23/32 split by service)
	// Feature 30 can be derived from this: diff_srv_rate = (1 - same_srv_rate)
	// TODO: consider using map<service_t, uint32_t> to save memory
	int [] same_srv_counts = new int [Conversation.NUMBER_OF_SERVICES];
	
	//---------------StatsperHost.cpp-------------------------------
	public StatsPerHost(FeatureUpdater _feature_updater)
	{
		feature_updater = _feature_updater;
		rerror_count = 0;
		same_srv_counts = new int [Conversation.NUMBER_OF_SERVICES];	// zero-initialize
		count = 0;
		serror_count = 0; 
	}
	
	void report_conversation_removal(Conversation conv)
	{
		count--;
		
		// SYN error
		if (conv.is_serror())
		{
			serror_count--;
		}

		// REJ error
		if (conv.is_rerror())
		{
			rerror_count--;
		}

		// Number of conv. per service
		service_t service = conv.get_service();
		same_srv_counts[service]--;
	}

	void report_new_conversation(ConversationFeatures cf)
	{
		Conversation conv = cf.get_conversation();
		service_t service = conv.get_service();

		/*
		 * Set derived window features based on previous conversations in window
		 */
		// Feature 23/32
		feature_updater.set_count(cf, count);

		// Feature 25/38
		double serror_rate = (count == 0) ? 0.0 : (serror_count / (double)count);
		feature_updater.set_serror_rate(cf, serror_rate);

		// Feature 27/40
		double rerror_rate = (count == 0) ? 0.0 : (rerror_count / (double)count);
		feature_updater.set_rerror_rate(cf, rerror_rate);

		// Feature 29/34
		double same_srv_rate = (count == 0) ? 0.0 : (same_srv_counts[service] / (double)count);
		feature_updater.set_same_srv_rate(cf, same_srv_rate);

		// Feature 30
		double diff_srv_rate = (count == 0) ? 0.0 : (1.0 - same_srv_rate);
		feature_updater.set_diff_srv_rate(cf, diff_srv_rate);

		// Part of feature 31/37
		feature_updater.set_same_srv_count(cf, same_srv_counts[service]);

		/*
		 * Include new conversation to stats
		 */
		count++;	

		// SYN error
		if (conv.is_serror())
		{
			serror_count++;
		}

		// REJ error
		if (conv.is_rerror())
		{
			rerror_count++;
		}

		// Number of conv. per service
		same_srv_counts[service]++;
	}

	boolean is_empty()
	{
		return (count == 0);
	}

}
