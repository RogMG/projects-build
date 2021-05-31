/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package dataproccessor;

/**
 *
 * @author Rogelio Martinez
 */
public class DataProccessor {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
       InicioSesion begin = new InicioSesion();
       begin.setVisible(true);
       begin.setTitle("Iniciar Sesión");
    }
    
}
