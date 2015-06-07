package opendatacba;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class MySQL {
    private Connection conector;
    private Statement comando;
    
    public MySQL() throws Exception {
       conectar();
    }
    
    private void conectar() throws Exception {
           Class.forName("com.mysql.jdbc.Driver");
           this.conector = DriverManager.getConnection("jdbc:mysql://localhost/opendatacba", "root", "");
            
          
           this.comando = (Statement) conector.createStatement();                                             
    }
    
    public void desconectar() throws Exception{
           this.comando.close();
           this.conector.close();
    }
    
    public ResultSet cargarResulset(String SQL) throws Exception{  
        return this.comando.executeQuery(SQL);        
    }
    
    public int enviar(String SQL){
        try {        
            return this.comando.executeUpdate(SQL);
            
        } catch (SQLException ex) {
           return 0;
        }
    }

}
