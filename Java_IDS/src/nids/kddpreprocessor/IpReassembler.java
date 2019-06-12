package nids.kddpreprocessor;

import org.jnetpcap.protocol.network.Ip4.Timestamp;

import nids.kddpreprocessor.Net.ip_field_protocol_t;
import static nids.kddpreprocessor.Net.ip_field_protocol_t.*;

public class IpReassembler 
{
	// Timeout values & timeout check interval
	Config timeouts;
	IntervalKeeper timeout_interval;
	
	/**
	 * Reassembly buffer identification (key for map)
	 * RFC 815 Section 7:
	 * The correct reassembly buffer is identified by an equality of the following 
	 * fields:  the  foreign  and  local  internet  address,  the protocol ID, 
	 * and the identification field.
	 */
	public class IpReassemblyBufferKey 
	{
		int src = 0;
		int dst = 0;
		ip_field_protocol_t proto = PROTO_ZERO;
		int id = 0;
		
		public IpReassemblyBufferKey()
		{
			
		}
		
		IpReassemblyBufferKey();
		
		IpReassemblyBufferKey(IpFragment fragment) 
		{
			this.src = fragment.get_src_ip();
			this.dst = fragment.get_dst_ip();
			this.proto = fragment.get_ip_proto();
			this.id = fragment.get_ip_id();
		}
		
		// Required for map<> key
		boolean less(IpReassemblyBufferKey other)
		{
			if (src < other.src)
				return true;
			if (src > other.src)
				return false;

			// src IPs are equal
			if (dst < other.dst)
				return true;
			if (dst > other.dst)
				return false;

			// dst IPs are equal
			if (id < other.id)
				return true;
			if (id > other.id)
				return false;

			// IDs are equal
			return (proto < other.proto);
		}
	};
	
	IpReassembler::IpReassembler()
	: timeouts()
	, timeout_interval(timeouts.get_conversation_check_interval_ms())
	{
	}

	IpReassembler::IpReassembler(Config &timeouts)
	: timeouts(timeouts)
	, timeout_interval(timeouts.get_conversation_check_interval_ms())
	{
	}

	Packet reassemble(IpFragment frag)
	{
		// Remove timed out reassembly buffers
		Timestamp now = frag.get_end_ts();
		check_timeouts(now);

		// Check whether packet is part of fragmented datagram
		boolean is_fragmented = (frag.get_ip_flag_mf() || frag.get_ip_frag_offset() != 0);

		// If fragmented forward to correct reassembly buffer
		if (is_fragmented)
		{
			return forward_to_buffer(frag);
		}

		// Not fragmented, nothing to do 
		return frag;
	}

	IpDatagram forward_to_buffer(IpFragment frag)
	{
		IpReassemblyBufferKey key(frag);
		IpReassemblyBuffer *buffer = nullptr;

		// Find or insert with single lookup: 
		// http://stackoverflow.com/a/101980/3503528
		// - iterator can will also used to remove buffer for reassembled datagram
		BufferMap::iterator it = buffer_map.lower_bound(key);
		if (it != buffer_map.end() && !(buffer_map.key_comp()(key, it->first)))
		{
			// Key already exists; update lb->second if you care to
			buffer = it->second;
		}
		else 
		{
			// The key does not exist in the map
			// Add it to the map + update iterator to point to new item
			buffer = new IpReassemblyBuffer();
			it = buffer_map.insert(it, BufferMap::value_type(key, buffer));
		}

		// Call IP reassembly algorithm
		IpDatagram datagram = buffer.add_fragment(frag);

		// If new IP datagram reassembled, destroy the buffer for it
		// and enqueue datagram to output queue
		if (datagram) 
		{
			buffer_map.erase(it);
			delete buffer;
		}
		return datagram;
	}

	void check_timeouts(Timestamp now)
	{
		// Run no more often than once per timeout check interval
		if (!timeout_interval.is_timedout(now)) 
		{
			timeout_interval.update_time(now);
			return;
		}
		timeout_interval.update_time(now);

		// Maximal timestamps that timedout conversation in given state can have
		Timestamp max_timeout_ts = now - (timeouts.get_ipfrag_timeout() * 1000000);

		// Erasing during iteration available since C++11
		// http://stackoverflow.com/a/263958/3503528
		BufferMap::iterator it = buffer_map.begin();
		while (it != buffer_map.end()) 
		{
			// If buffer is timed out, DROP the incomplete datagram
			if (it.second.get_last_fragment_ts() <= max_timeout_ts) 
			{
				// Erase
				buffer_map.erase(it++);  // Use iterator + post increment
			}
			else 
			{
				++it;
			}
		} 
		// end of while(it..
	}
}
