package simple;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static org.junit.Assert.*;
import org.junit.BeforeClass;
import org.junit.ClassRule;
import org.testcontainers.containers.MSSQLServerContainer;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;



/**
 * test for simple App.
 */
@RunWith(JUnit4.class)
public class AppTest {
    
    @ClassRule
    public static MSSQLServerContainer msSQLContainer =  new MSSQLServerContainer();
    private static Logger log = LoggerFactory.getLogger(AppTest.class);

    public static Connection sqlServerCon;
    public static String sqlServerJdbcUrl;
    public static String sqlServerUsername;
    public static String sqlServerPassword;

    @BeforeClass
    public static void setUpBeforeClass() throws Exception {
        try {
        sqlServerJdbcUrl = msSQLContainer.getJdbcUrl();
        sqlServerUsername = msSQLContainer.getUsername();
        sqlServerPassword = msSQLContainer.getPassword();
        sqlServerCon = DriverManager.getConnection(sqlServerJdbcUrl, sqlServerUsername, sqlServerPassword);
        // System.out.println("######## Sql server connection info ");
        log.info("######## Sql server connection info ");
        log.info("######## Sql server jdbc url "+msSQLContainer.getJdbcUrl());
        log.info("######## Sql server User/pass "+msSQLContainer.getUsername()+"/"+msSQLContainer.getPassword());
        } catch (Exception e) {
            e.printStackTrace();
            throw e;
        }
    }

    @Test
    public void testApp() throws SQLException {
        Statement stmt ;
        try {
            stmt = sqlServerCon.createStatement();
            stmt.execute("CREATE DATABASE test;");
            stmt.execute("CREATE TABLE test.dbo.test_table(id INT  , first_name VARCHAR (50),last_name  varchar(50),email_address varchar(100));");
            System.out.println("Success Creating testcontainer connection/table");
            
        } catch (Exception e) {
            e.printStackTrace();
            throw e;
        }
        assertTrue(App.printAllRecords(sqlServerCon, "test.dbo.test_table").size()==0);
        try {
            stmt.execute("insert into test.dbo.test_table(id, first_name, last_name, email_address) "+
                        " VALUES (1, 'Tom', 'Sawyer', 'tsawyer@marktwain.com');");
            assertTrue(App.printAllRecords(sqlServerCon, "test.dbo.test_table").size()==1);
            log.info(App.printAllRecords(sqlServerCon, "test.dbo.test_table").get(0).toString());
        }catch (SQLException sqlE){
            sqlE.printStackTrace();
            throw sqlE;
        }
    }
}
