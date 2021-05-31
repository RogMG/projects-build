/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package apsql;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 *
 * @author C1 14
 */
public class Conexion {
    protected Connection obtenerConexion(String ip, String pto, String bd, String usr, String pass)
    {
        Connection con = null;
        try
        {
            Class.forName("com.mysql.jdbc.Driver");
            con = DriverManager.getConnection("jdbc:mysql://"+ip+":"+pto+"/"+bd,usr,pass);
        }catch(ClassNotFoundException ex)
        {
            System.out.println("No se encontró driver: "+ex);
        }catch(SQLException ex)
        {
            System.out.println("Error en conexión ó datos de acceso: "+ex.getMessage());
        }        
        return con;
    }
}
