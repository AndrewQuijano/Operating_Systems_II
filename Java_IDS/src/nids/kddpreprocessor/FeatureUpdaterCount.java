package nids.kddpreprocessor;

public class FeatureUpdaterCount implements FeatureUpdater
{
	public void set_count(ConversationFeatures f, int count) 
	{
		f.set_dst_host_count(count);
	}

	public void set_srv_count(ConversationFeatures f, int srv_count) 
	{
		f.set_dst_host_srv_count(srv_count);
	}

	public void set_serror_rate(ConversationFeatures f, double serror_rate)
	{
		f.set_dst_host_serror_rate(serror_rate);
	}

	public void set_srv_serror_rate(ConversationFeatures f, double srv_serror_rate) 
	{
		f.set_dst_host_srv_serror_rate(srv_serror_rate);
	}

	public void set_rerror_rate(ConversationFeatures f, double rerror_rate) 
	{
		f.set_dst_host_rerror_rate(rerror_rate);
	}

	public void set_srv_rerror_rate(ConversationFeatures f, double srv_rerror_rate) 
	{
		f.set_dst_host_srv_rerror_rate(srv_rerror_rate);
	}

	public void set_same_srv_rate(ConversationFeatures f, double same_srv_rate) 
	{
		f.set_dst_host_same_srv_rate(same_srv_rate);
	}

	public void set_diff_srv_rate(ConversationFeatures f, double diff_srv_rate) 
	{
		f.set_dst_host_diff_srv_rate(diff_srv_rate);
	}

	public void set_dst_host_same_src_port_rate(ConversationFeatures f, double dst_host_same_src_port_rate) 
	{
		f.set_dst_host_same_src_port_rate(dst_host_same_src_port_rate);
	}

	public void set_same_srv_count(ConversationFeatures f, int same_srv_count) 
	{
		f.set_dst_host_same_srv_count(same_srv_count);
	}
}
