/*
 * Copyright 2012-2013 the original author or authors.
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

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import testcontainers.data.mongo.controller.MongoDataService;


@Configuration
@EnableAutoConfiguration
@ComponentScan(basePackages = "testcontainers.data.mongo")
public class MongoDataApplication implements CommandLineRunner {

	@Autowired
	private MongoDataService controller;

	@Override
	public  void run(String... args) throws Exception {

	}

	public static void main(String[] args) throws Exception {
		SpringApplication.run(MongoDataApplication.class, args);
	}
}
