package nids;

import java.util.ArrayList;
import java.util.List;

import org.jnetpcap.Pcap;
import org.jnetpcap.PcapIf;

/* The purpose of this class is ONLY to sniff packets and generate a PCAP from it. */
public class Sniffer 
{
	public static boolean start()
	{
		List<PcapIf> alldevs = new ArrayList<PcapIf>();
		final StringBuilder errbuf = new StringBuilder();

		int r = Pcap.findAllDevs(alldevs, errbuf);  
		if (r != Pcap.OK || alldevs.isEmpty()) 
		{
			System.err.printf("Can't read list of devices, error is %s", errbuf.toString());
			return false;  
		}
		else
		{
			return true;
		}
	}
}
