package Handlers;

import org.jnetpcap.packet.PcapPacket;
import org.jnetpcap.packet.PcapPacketHandler;
import org.jnetpcap.protocol.network.Ip4;

public class handler
{
	private Ip4 ip = new Ip4(); // Ip4 header

	public void nextPacket(PcapPacket packet, Object user) 
	{
		if (packet.hasHeader(ip)) 
		{
			final int flags = ip.flags();
			/*
			 * Check if we have an IP fragment
			 */
			if ((flags & Ip4.FLAG_MORE_FRAGMENTS) != 0) 
			{
				bufferFragment(packet, ip);
				/*
				 * record the last fragment
				 */
			} 
			else 
			{
				bufferLastFragment(packet, ip);
			}

			/*
			 * Our crude timeout mechanism, should be implemented as a separate thread
			 */
			timeoutBuffers();
		}
	}
}