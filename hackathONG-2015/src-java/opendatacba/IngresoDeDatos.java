
package opendatacba;
import java.util.*;

public class IngresoDeDatos {

	private static Scanner sc = new Scanner(System.in);
	private static Scanner scEspecial = new Scanner(System.in);
	
	public static int valEntero(String msj){
		
		try {
			if (msj.equals("")==false){ 
				System.out.println(msj); 
			}
			
			int numero=Integer.parseInt(sc.next());
			
			
			return numero;
			
		} catch (NumberFormatException nfe) {
			System.out.println("Ingrese solo números enteros");
			return valEntero(msj);
			
		}
	}
	
	public static int valNaturales(String msj){
		
		try {
			if (msj.equals("")==false){ 
				System.out.println(msj); 
			}
		
			
			int numero=Integer.parseInt(sc.next());
			
			
			
			if(numero<0){
				System.out.println("El número debe ser mayor que 0"); 
				return valNaturales(msj);
			}
		
			
			return numero;
		} catch (NumberFormatException nfe) {
			System.out.println("Ingrese solo números");
			return valNaturales(msj);
			
		}
		
		
	}
	
	public static int valRangoNum(String msj){
		
		try {
			if (msj.equals("")==false){ 
				System.out.println(msj); 
			}
			
			
			int numero=Integer.parseInt(sc.next());
			
			
			
			if(numero<1){
				System.out.println("Ingrese un número mayor a 1"); 
				return valRangoNum(msj);
			}
			
			if(numero>7){
				System.out.println("Ingrese un número menor a 7"); 
				return valRangoNum(msj);
			}
			
			
			return numero;
		} catch (NumberFormatException nfe) {
			System.out.println("Ingrese solo números");
			return valRangoNum(msj);
			
		}
		
	}
	
	public static float valFloat(String msj){
		
		try {
			if (msj.equals("")==false){ 
				System.out.println(msj); 
			}
			
			float numero=Float.parseFloat(sc.next());
			
			
			return numero;
			
		} catch (NumberFormatException nfe) {
			System.out.println("Ingrese solo números enteros");
			return valFloat(msj);
			
		}
	}
	
	public static String valString(String msj){
		
		try {
			
			if (msj.equals("")==false){ 
				System.out.println(msj); 
			}
			
			// se usa otro sc porque el .next devuelve un string que no contempla espacios
			// pero si quiero usa el nextLine con el sc anterior y previamente se ingresó un número
			// queda almacenado el valor de la tecla enter en el sc
			// para solucionar este problema podríamos llamar dos veces al nextLine
			// pero el problema estaría si lo llamo dos veces y anteriormente no se ingresó un número 
			String cadena = scEspecial.nextLine();
			
			
			return cadena;
			
		} catch (NumberFormatException nfe) {
			System.out.println("Error en cadena de texto");
			return valString(msj);
			
		}
	}
}