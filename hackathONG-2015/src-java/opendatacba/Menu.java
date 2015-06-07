
package opendatacba;

public class Menu {

    public static void menu(){    	    	

            System.out.println("MENÚ");
                         
            int opcion=IngresoDeDatos.valEntero(
                    "Seleccione una opción: " +
                    "\n1.Ingresar directorio de entrada " +                    
                    "\n2.Pasar a Base de datos "+            		
                    "\n3.Cargar tabla link_3 "+ 
                    "\n10.Salir");
            
            ejecutar(opcion);
            menu();           
    }
    
    
    
    
    private static void ejecutar(int seleccionada){
    	
        switch (seleccionada){
				
		        case 1:                	            	
		        	String directorioEntrada = IngresoDeDatos.valString("Ingrese el directorio de entrada: ");            	
		        	directorioEntrada = Operaciones.corregirPath(directorioEntrada); 
		        	
		        	if (Operaciones.existeDirectorio(directorioEntrada)==true){
		        		Operaciones.setDirEntrada(directorioEntrada);	
		        	}
		        	else{
		        		System.out.println("No existe el directorio");
		        		Operaciones.setDirEntrada("");
		        	}
		        		
		        	
		        	                  
		            break;

		                
		        case 2:
		        	
		        	//valido directorios
		        	String validacion = Operaciones.ValidarDirectorios();
		        	if (validacion.equals("")==false){                               
                                    System.out.println(validacion);
                                    //si hay error salgo...
                                    break;
		        	}
		        	
		        
		        	String dirEntrada = Operaciones.getDirEntrada();
		        	
                                //examina el directorio y hace los insert en la tabla set_3
		        	Operaciones.examinarDirectorio(dirEntrada); 


		 
		        	
		        	
		        	
		                              
		            break;
                        case 3:
                            Operaciones.cargarTablaLinks();
                            
                            break;
	
		
		        case 10:
		
		            System.exit(0);
		}
    	
    }    

}
