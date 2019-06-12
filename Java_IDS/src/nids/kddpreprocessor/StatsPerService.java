package nids.kddpreprocessor;

public class StatsPerService 
{
	private FeatureUpdater feature_updater;
	private int srv_count = 0;
	private int srv_serror_count = 0;
	private int srv_rerror_count = 0;
	
	public StatsPerService(FeatureUpdater _feature_updater)
	{
		feature_updater = _feature_updater;
	}

	void report_conversation_removal(Conversation conv)
	{
		srv_count--;
		
		// SYN error
		if (conv.is_serror())
		{
			srv_serror_count--;
		}

		// REJ error
		if (conv.is_rerror())
		{
			srv_rerror_count--;
		}
	}

	void report_new_conversation(ConversationFeatures cf)
	{
		Conversation conv = cf.get_conversation();

		/*
		 * Set derived window features based on previous conversations in window
		 */
		
		// Feature 24
		feature_updater.set_srv_count(cf, srv_count);

		// Feature 26
		double srv_serror_rate = (srv_count == 0) ? 0.0 : (srv_serror_count / (double)srv_count);
		feature_updater.set_srv_serror_rate(cf, srv_serror_rate);

		// Feature 28
		double srv_rerror_rate = (srv_count == 0) ? 0.0 : (srv_rerror_count / (double)srv_count);
		feature_updater.set_srv_rerror_rate(cf, srv_rerror_rate);

		/*
		 * Include new conversation to stats
		 */
		srv_count++;

		// SYN error
		if (conv.is_serror())
		{
			srv_serror_count++;
		}

		// REJ error
		if (conv.is_rerror())
		{
			srv_rerror_count++;
		}
	}

	boolean is_empty()
	{
		return (srv_count == 0);
	}
}