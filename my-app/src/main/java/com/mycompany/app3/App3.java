package com.mycompany.app3;

import java.util.regex.Matcher; 
import java.util.regex.Pattern; 

	
public class App3 {

	private static final Pattern NUMBERS = Pattern.compile("(\\d+)");

	public static void main( String[] args )
    {
		
		System.out.println("\n\n==================================================================================\n\n");

		
		String value;
		value = "239 / 98955: 590 22 9059";
		String line = value.toString();
		Matcher m = NUMBERS.matcher(line);
		System.out.println(m.find());
		
		System.out.println( "Hello World!---31" + " -- " +  m.toString() + " -- " + m.group() );

		System.out.println( "Hello World!---31" );
        
		System.out.println("\n\n==================================================================================\n\n");
        
    }
}
