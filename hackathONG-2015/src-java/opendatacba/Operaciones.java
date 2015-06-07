
package opendatacba;

import java.io.File;
import java.sql.ResultSet;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Operaciones {
	

	private static String dirEntrada;	      	    
	
	public static String getDirEntrada() {
		return dirEntrada;
	}
	public static void setDirEntrada(String dirEntrada) {
		Operaciones.dirEntrada = dirEntrada;
	}	
	
	public static String ValidarDirectorios(){
            String salto = "\r\n";
            String validarDirectorios = "";
            if (dirEntrada==null){
                    validarDirectorios = "Falta directorio de entrada." + salto;
            }else{
                    if (dirEntrada.equals("")){
                        validarDirectorios = "Error en directorio de entrada." + salto;
                    }
            }
            
            return validarDirectorios;
	}
	
	public static boolean existeDirectorio(String directorio){
		File dir = new File(directorio);
		if (dir.canRead()==true){
			return true;
		}else{
			return false;
		}
	}
	
        public static String corregirPath(String pathViejo){
		String nuevoPath = pathViejo;
		
		
		String ultimoCaracter = pathViejo.substring(pathViejo.length()-1, pathViejo.length());

		// el cod ascii de esta barra "\" es "92"
		String separador = "" + (char) 92;  
		
		//si el path se ingresó así "C:\Prueba" se modifica para que quede así C:\Prueba\
		if (ultimoCaracter.equals(separador) == false){			
			nuevoPath= pathViejo + separador;
		}

   	
		
		// el cod ascii de esta barra / es "47"

		return nuevoPath;
		
		
	}
        
        
        
        
        
        
        
        
	public static void examinarDirectorio(String directorio){
		//Le paso el directorio de entrada
		File dir = new File(directorio);	
		
		//Cargo en un arreglo de archivos todos los archivos del directorio de entrada
		File[] ficheros=dir.listFiles();
		
		
		
		if(ficheros==null){
			System.out.println("No hay ficheros en el directorio específicado");
		}
		else{
                    MySQL objMySQL ;
                    try {
                        objMySQL = new MySQL();

                    
                        for(int i=0; i<ficheros.length; i++){												

                                if (ficheros[i].isDirectory() == true){

                                        //Si es una carpeta     
                                        System.out.println("Directorio procesado: " + ficheros[i].getPath());
                                        //examinarDirectorio(ficheros[i].getPath());

                                }else{
                                        //Si es un archivo 
                                    System.out.println("Archivo procesado: " + ficheros[i].getName());                                        
                                    if (ficheros[i].getName().toLowerCase().contains(".zip")==true){


                                        String path = ficheros[i].getPath();

                                        String query = 
                                                "INSERT INTO `opendatacba`.`set_3` ( `nombre`, `path`)  "
                                                + "values ('" + ficheros[i].getName() + 
                                                "','" + path  + "')" ;


                                        objMySQL.enviar(query);


                                    }


                                }
                        }	
                    
                    } catch (Exception ex) {
                        Logger.getLogger(Operaciones.class.getName()).log(Level.SEVERE, null, ex);
                    }
		}
	}
	

        public static void cargarTablaLinks(){
        
        
            MySQL oMySQL ;
           
            try {
                oMySQL = new MySQL();
                //traigo los municipios
                ResultSet regMunicipios  = oMySQL.cargarResulset("SELECT `id`, `municipio` FROM  `municipios`");
                //recorro los municipios
                int cont = 0 ;
                
                while(regMunicipios.next()){
                    cont = cont +1;
                    System.out.println(cont);
                    if (cont == 50){
                    int a = 1;
                    }
                    MySQL oMySQL2;
                    oMySQL2 = new MySQL();
                    ResultSet regSet_3  = oMySQL2.cargarResulset("SELECT `id`, `nombre` FROM  `set_3`");                                            
                    
                    //por cada municipio recorro los nombres de archivos levantados del disco duro que los había cargado previemente en la tabla set_3                    
                    while(regSet_3.next()){
                        
                        //cargo en la variable part2 el nombre de localidad obtenido del nombre de archivo del discoDuro separado por -
                        String nombreSet = regSet_3.getString("nombre");
                        String[] partes = nombreSet.split("-");
                        String part2 = "";
                        try{  
                            //controlo errores porque hay dos archivos que no tienen -
                            part2 = partes[1];
                        }
                        catch (Exception ex2)             
                        {                
                            //System.out.println(ex2.getMessage());            
                        }

                        //si no es vacío part2 es porque no hubo errores
                        if (part2.equals("")==false){
                            
                            //paso part2 y el nombre de municipio de la base a mayusculas y le quito espacios
                            part2 = part2.toUpperCase();
                            part2 = part2.trim();
                            
                            String nombreMunicipio = regMunicipios.getString("municipio").toUpperCase();
                            nombreMunicipio = nombreMunicipio.trim();
                            
                            int distancia = LevenshteinDistance.computeLevenshteinDistance(part2, nombreMunicipio);
                            
                            if(distancia < 2){                        
                                oMySQL.enviar(
                                          "INSERT INTO `opendatacba`.`link_3` (`id_municipios`, `id_set_3`) "
                                        + "VALUES ('" +regMunicipios.getInt("id") + "','" +regSet_3.getInt("id") + "') ");
                            }                        
                        }

                    }
                    
                    
                }
                
                
            }  
            catch (Exception ex) 
            {
                System.out.println(ex.getMessage());
            }
                
        }
	
	
	
}