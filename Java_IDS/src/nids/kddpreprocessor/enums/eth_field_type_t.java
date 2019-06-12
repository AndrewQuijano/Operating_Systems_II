package nids.kddpreprocessor.enums;
/*
 * Ethernet type/length field
 */
public enum eth_field_type_t  
{
	TYPE_ZERO(0),
	MIN_ETH2(0x600),
	IPV4(0x800);
	private int value;

	private eth_field_type_t(int value) 
	{
		this.setValue(value);
	}

	public int getValue() 
	{
		return value;
	}

	private void setValue(int value)
	{
		this.value = value;
	}
};
