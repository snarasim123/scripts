Testcontainer Example
=====

A simple example to demonstrate the testcontainers.
The application is a simple java application which serves no real functionality.
But the Junit test demonstrates how to use testcontainers for integration tests when
database servers are needed.

The application takes jdbcUrl, username, password as parameters.
Fetches all records from a table and returns to the calling method.

The Junit test demonstrates how to do integration test of this application.
It creates a Mssqlserver testcontainer, creates a database, creates a table,
populates records and calls the method to return the records for assertion.

Few things to note.
------------

  - You need to have docker, a working java development environment to debug the code.

  - src/test/resources/container-license-acceptance.txt File is needed to use MsSql server. 
    If you remove this file, you will see an error from Mssql server.

  - You can change the type of database easily to a different database like Postgress.
    See here for other databases availble from testcontainers - todo.

  - If you need to have a specific user/password for your integration test, create a new
    user using sql demonstrated in the Junit test.