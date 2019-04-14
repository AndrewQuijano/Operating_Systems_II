package nids;

import java.io.File;
import java.io.IOException;
import java.util.List;

import org.jnetpcap.Pcap;
import org.jnetpcap.packet.PcapPacket;
import org.jnetpcap.util.PcapPacketArrayList;

// Abstract class used for building pre-processors from PCAP data
public abstract class Data_mining 
{
	protected abstract void test_label();
	
	public List<PcapPacket> getPacketList(String file) throws IOException 
	{
		StringBuilder errbuf = new StringBuilder();
		Pcap pcap = Pcap.openOffline(file, errbuf);
		if (pcap == null) 
		{
			throw new IOException(errbuf.toString());
		}
		final PcapPacketArrayList list = new PcapPacketArrayList((int) new File(file).length()/100);
		pcap.loop(list.size(), list, null);
		pcap.close();
		return list;
	}
}
