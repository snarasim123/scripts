/*
 * Copyright 2012-2014 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package testcontainers.data.mongo;

import java.net.ConnectException;
import java.util.List;
import java.util.Optional;

import org.bson.BsonDocument;
import org.bson.Document;
import org.junit.BeforeClass;
import org.junit.FixMethodOrder;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.MethodSorters;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.SpringBootDependencyInjectionTestExecutionListener;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.util.TestPropertyValues;
import org.springframework.context.ApplicationContextInitializer;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.core.NestedCheckedException;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.TestExecutionListeners;
import org.springframework.test.context.jdbc.SqlScriptsTestExecutionListener;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.context.transaction.TransactionalTestExecutionListener;

import testcontainers.data.mongo.controller.MongoDataService;

import static org.junit.Assert.assertTrue;

/**
 * Tests for {@link MongoDataApplication}.
 * 
 */
@RunWith(SpringRunner.class)
@SpringBootTest(classes = MongoDataService.class)
@FixMethodOrder(MethodSorters.NAME_ASCENDING)
@ContextConfiguration(initializers = {MongoApplicationTests.Initializer.class})
@TestExecutionListeners({
         SpringBootDependencyInjectionTestExecutionListener.class
        ,TransactionalTestExecutionListener.class
		,SqlScriptsTestExecutionListener.class
})
@ComponentScan(basePackages = "testcontainers.data.mongo")
public class MongoApplicationTests {


	@Autowired
	MongoDataService controller;

	public static MongoContainer container = new MongoContainer(); 

	private static Optional<String> ip = Optional.empty();
	private static Optional<String> uri = Optional.empty();
	private static Optional<String> connectString = Optional.empty();

	static class Initializer implements ApplicationContextInitializer<ConfigurableApplicationContext> {
		public void initialize(ConfigurableApplicationContext configurableApplicationContext) {

			TestPropertyValues.of(
				"spring.output.ansi.enabled=always"
				,"serverbase="+ip.get()
				,"spring.data.mongodb.uri=" + connectString.get()
				,"spring.data.mongodb.database=testdb"
				,"spring.application.name=mongo-testcontainer-example"
			).applyTo(configurableApplicationContext.getEnvironment());
		}
	}

	@BeforeClass
    public static void setUpBeforeClass() throws Exception {
        try {
			ip = container.getIp();
			System.out.println("<--- Mongo Ip ---> "+ ip.get().toString());
			uri=container.getURI();
			System.out.println("<--- Mongo URI ---> "+uri);
			connectString=Optional.of(uri.get() +"/testdb?authSource=admin");
			System.out.println("<--- Mongo Connect String ---> "+connectString.get());
        } 	catch (Exception ex){
			System.out.println("Error "+ ex.getMessage());
				throw ex;
        	}

    }

	@Test
	public void testSimple() throws Exception {
		try {
			controller.create("test","user");

			MongoClientHelper helper = new MongoClientHelper(uri.get(),"Customer", "testdb");
			helper.init();
			BsonDocument bson = BsonDocument.parse("{\"firstName\": \"test\"}");
			List<Document> docs = helper.getCurrentCollection(bson);
			assertTrue(docs.size()==1);
			assertTrue(docs.get(0).get("lastName").equals("user"));

		}
		catch (IllegalStateException ex) {
			if (serverNotRunning(ex)) {
				return;
			}
		}
	}

	private boolean serverNotRunning(IllegalStateException ex) {
		@SuppressWarnings("serial")
		NestedCheckedException nested = new NestedCheckedException("failed", ex) {
		};
		if (nested.contains(ConnectException.class)) {
			Throwable root = nested.getRootCause();
			if (root.getMessage().contains("Connection refused")) {
				return true;
			}
		}
		return false;
	}

}
