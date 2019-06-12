package nids.kddpreprocessor;

public interface FeatureUpdater 
{
	void set_count(ConversationFeatures f, int count);
	void set_srv_count(ConversationFeatures f, int srv_count);
	void set_serror_rate(ConversationFeatures f, double serror_rate);
	void set_srv_serror_rate(ConversationFeatures f, double srv_serror_rate);
	void set_rerror_rate(ConversationFeatures f, double rerror_rate);
	void set_srv_rerror_rate(ConversationFeatures f, double srv_rerror_rate);
	void set_same_srv_rate(ConversationFeatures f, double same_srv_rate);
	void set_diff_srv_rate(ConversationFeatures f, double diff_srv_rate);
	void set_dst_host_same_src_port_rate(ConversationFeatures f, double dst_host_same_src_port_rate);
	void set_same_srv_count(ConversationFeatures f, int same_srv_count);
}
