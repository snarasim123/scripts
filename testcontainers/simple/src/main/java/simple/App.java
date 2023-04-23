package simple;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import javax.sql.rowset.JdbcRowSet;

import org.w3c.dom.UserDataHandler;

/**
 * Hello world!
 */
public final class App {
    private App() {
    }

    public static void main(String[] args) throws Exception {
        System.out.println("Hello Testcontainers World!");

        String jdbcUrl, username, password;
        if (args.length<3)  
            throw new Exception("Insufficient Args");
        jdbcUrl = args[0];
        username = args[1];
        password = args[2];  
        
        Connection sqlServerCon = DriverManager.getConnection(jdbcUrl, username, password);
        printAllRecords(sqlServerCon, "test_table");
    }

    public static List<String> printAllRecords(Connection conn, String tablename) throws SQLException {
        //select * from tablename and print all ...

        Statement stmt = conn.createStatement();
        stmt.execute("select * from "+ tablename + ";");
        ResultSet rowSet = stmt.getResultSet();
        ResultSetMetaData rsmd = rowSet.getMetaData();
        List<String> resultStr = new ArrayList<String>();
        int columnCt = rsmd.getColumnCount();
        while(rowSet.next()){
            StringBuilder sbr = new StringBuilder();
            for(int i=1;i<=columnCt;i++){
                sbr.append(rowSet.getObject(rsmd.getColumnName(i)).toString());
                sbr.append(",");
            }
            resultStr.add(sbr.toString());
        }
        return resultStr;
    }


}
