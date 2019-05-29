package nids.kddpreprocessor;

public class StatsEngine 
{
	StatsWindowTime<StatsPerHost, StatsPerService> time_window;
	StatsWindowCount<StatsPerHost, StatsPerServiceWithSrcPort> count_window;
	
	StatsEngine(Config config)
	{
		time_window = new StatsWindowTime<StatsPerHost, StatsPerService>(config.get_time_window_size_ms());
		count_window = new StatsWindowCount<StatsPerHost, StatsPerServiceWithSrcPort>(config.get_count_window_size());
	}
	
	ConversationFeatures calculate_features(Conversation conv)
	{
		ConversationFeatures cf = new ConversationFeatures(conv);

		// Set time window features & to time window
		time_window.add_conversation(cf);

		// Set count window features & to count window
		count_window.add_conversation(cf);

		return cf;
	}
}
